#send.py
from threading import Lock
from pprint import pprint
import logging
import multiprocessing
import pika
import json
import uuid
import ssl
import argparse
from pathlib import Path
import configparser
import os
from pymongo import MongoClient
from datetime import datetime

# Load configurations from config.ini file
config = configparser.ConfigParser()
config.read('config.ini')

# RabbitMQ connection parameters
mq_connection = config['RabbitMQ']['mq_connection_string']
parameters = pika.URLParameters(mq_connection)

# Set up logging
if config.getboolean('Logging', 'debug'):
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO
logging.basicConfig(filename=config['Logging']['logfile'], level=logging_level, format='%(asctime)s - %(levelname)s: %(message)s')

default_nodes = [node.strip() for node in config.get('Nodes', 'default_nodes', fallback='').split(',')]

if mq_connection.startswith('amqps'):
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False

    cacertfile = Path('./rabbitmq/certificates/rootCA_cert.pem')
    certfile = Path('./rabbitmq/certificates/server_cert.pem')
    keyfile = Path('./rabbitmq/certificates/server_key.pem')

    context.verify_mode = ssl.CERT_NONE

    if cacertfile.exists():
        context.verify_mode = ssl.CERT_REQUIRED
        context.load_verify_locations(cafile=str(cacertfile))

    if certfile.exists():
        assert(keyfile.exists())
        context.load_cert_chain(str(certfile), keyfile=str(keyfile))

    parameters.ssl_options = pika.SSLOptions(context=context, server_hostname=None)

# MongoDB connection setup
mongo_client = MongoClient(config['MongoDB']['mongo_connection_string'])
mongo_db = mongo_client[config['MongoDB']['mongo_database_name']]
executions_collection = mongo_db['executions']
# Define a lock for thread safety
mongo_lock = Lock()


class RpcClient:
    def __init__(self):
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        result = self.channel.queue_declare(queue='', exclusive=True)
        self.callback_queue = result.method.queue

        self.channel.basic_consume(
            queue=self.callback_queue,
            on_message_callback=self.on_response,
            auto_ack=True
        )
        self.response = None
        self.corr_id = str(uuid.uuid4())

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body.decode() if body else None

    def call(self, command, node):
        self.response = None
        self.channel.basic_publish(
            exchange='',
            routing_key=node,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=str(command)
        )
        self.connection.process_data_events(time_limit=None)
        return self.response

def register_run(execution_info):
    with mongo_lock:
        try:
            executions_collection.insert_one(execution_info)
            logging.info("Inserted execution data into MongoDB.")
        except Exception as e:
            logging.error(f"Error inserting execution data into MongoDB: {e}")

def start_call(execution_id, task_id, tool_id, nodes):
    try:
        rpc = RpcClient()

        # Set up the command (task_id and execution_id)
        command = f"{tool_id}:{task_id}:{execution_id}"

        # Moved these lines outside the try block
        starting_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        # Send the command to the specified nodes
        for node in nodes:
            response = rpc.call(command, node)

            if response:
                logging.info(f" [.] RESPONSE FROM {node}: {response}")
                status = "success"
                return_code = 0
            else:
                logging.info(f" [.] Empty response from {node}")
                status = "failed"
                return_code = 1

            # Register the run in the database
            register_run({
                "execution_id": execution_id,
                "tool_id": command,
                "node": node,
                "result": response,
                "status": status,
                "return_code": return_code,
                "starting_time": starting_time,
                "finish_time": finish_time
            })

    except Exception as e:
        # Define 'node' here to make it accessible in the except block
        node = "undefined"
        logging.error(f" [!] Exception during execution on node {node}: {e}")
        status = "failed"
        return_code = 1
        response = str(e)

        # Register the run in the database
        register_run({
            "execution_id": execution_id,
            "tool_id": tool_id,
            "node": node,
            "result": response,
            "status": status,
            "return_code": return_code,
            "starting_time": starting_time,
            "finish_time": finish_time
        })

    # Add a log message to indicate the end of processing
    logging.info(f" [x] Finished processing {task_id} on nodes: {nodes}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool_id", help="ID of the tool to run", type=str, required=True)
    parser.add_argument("-n", "--nodes", nargs='+', help="names of the nodes to run the function on", type=str)

    args = parser.parse_args()
    tool_id = args.tool_id

    # Generate a unique execution_id for this execution
    execution_id = str(uuid.uuid4())

    # if node name provided, run command for that node only
    if args.nodes:
        for node in args.nodes:
            start_call(execution_id, tool_id, node)
    else:
        # otherwise, run command for all nodes in the list
        for node in default_nodes:
            # start process start_call
            p = multiprocessing.Process(target=start_call, args=(execution_id, tool_id, node,))
            p.start()

    # Add the following lines for testing
    logging.basicConfig(level=logging.INFO)

    # Test the start_call function
    start_call("test_task", ["node1", "node2"])
