#send.py
from threading import Lock
from pprint import pprint
import logging
import multiprocessing
import pika
import uuid
import ssl
import argparse
from pathlib import Path
import configparser
from pymongo import MongoClient
from datetime import datetime


class sendEngine():
    def __init__(self, config, mongo_db):

        # RabbitMQ connection parameters
        self.mq_connection = config['RabbitMQ']['mq_connection_string']
        self.parameters = pika.URLParameters(mq_connection)

        self.default_nodes = [node.strip() for node in config.get('Nodes', 'default_nodes', fallback='').split(',')]

        if self.mq_connection.startswith('amqps'):
            self.context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
            self.context.check_hostname = False

            cacertfile = Path(config['RabbitMQ']['cacertfile'])
            certfile = Path(config['RabbitMQ']['certfile'])
            keyfile = Path(config['RabbitMQ']['keyfile'])

            self.context.verify_mode = ssl.CERT_NONE

            if cacertfile.exists():
                self.context.verify_mode = ssl.CERT_REQUIRED
                self.context.load_verify_locations(cafile=str(cacertfile))

            if certfile.exists():
                assert(keyfile.exists())
                self.context.load_cert_chain(str(certfile), keyfile=str(keyfile))

            self.parameters.ssl_options = pika.SSLOptions(context=self.context, server_hostname=None)

            self.executions_collection = mongo_db['executions']
            # Define a lock for thread safety
            self.mongo_lock = Lock()

    def set_execution_id(self):
        # Generate a unique execution for this execution
        self.execution_id = str(uuid.uuid4())

    def register_run(self, execution_info):
        with self.mongo_lock:
            try:
                self.executions_collection.insert_one(execution_info)
                logging.info("Inserted execution data into MongoDB.")
            except Exception as e:
                logging.error(f"Error inserting execution data into MongoDB: {e}")

    def start_call(self, tool_id, task_id, nodes):
        try:
            rpc = RpcClient()

            # Set up the command (task_id and execution_id)
            command = f"{tool_id}:{task_id}:{self.execution_id}"

            # Moved these lines outside the try block
            starting_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

            # Send the command to the specified nodes
            if isinstance(nodes, str):
                nodes = [nodes]

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
                self.register_run({
                    "execution_id": self.execution_id,
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

        # # Register the run in the database
        # self.register_run({
        #     "execution_id": execution_id,
        #     "tool_id": tool_id,
        #     "node": node,
        #     "result": response,
        #     "status": status,
        #     "return_code": return_code,
        #     "starting_time": starting_time,
        #     "finish_time": finish_time
        # })

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


    # Add a log message to indicate the end of processing
    logging.info(f" [x] Finished processing {task_id} on nodes: {nodes}")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--tool_id", help="ID of the tool to run", type=str, required=True)
    parser.add_argument("--task_id", help="ID of the task to run", type=str, required=True)
    parser.add_argument("--config", help="Configuration file. Default:config.ini", default="config.ini")
    parser.add_argument("-n", "--nodes", nargs='+', help="names of the nodes to run the function on", type=str)

    args = parser.parse_args()
    tool_id = args.tool_id

    # Load configurations from config.ini file
    config = configparser.ConfigParser()
    config.read('config.ini')

    # Set up logging
    if config.getboolean('Logging', 'debug'):
        logging_level = logging.DEBUG
    else:
        logging_level = logging.INFO
    logging.basicConfig(filename=config['Logging']['logfile'], level=logging_level, format='%(asctime)s - %(levelname)s: %(message)s')

    # MongoDB connection setup
    mongo_client = MongoClient(config['MongoDB']['mongo_connection_string'])
    mongo_db = mongo_client[config['MongoDB']['mongo_database_name']]

    send_engine = sendEngine(config, mongo_db)

    # if node name provided, run command for these nodes only
    if args.nodes:
        node_list = args.nodes
    else:
        node_list = send_engine.default_nodes

    for node in send_engine.default_nodes:
        # start process start_call
        p = multiprocessing.Process(target=send_engine.start_call, args=(args.tool_id, args.task_id, node_list))
        p.start()

    # Add the following lines for testing
    # logging.basicConfig(level=logging.INFO)

    # Test the start_call function
    # start_call("test_task", ["node1", "node2"])
