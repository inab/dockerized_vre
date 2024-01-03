#receiver.py

#!/usr/bin/env python
from pprint import pprint
import pika
import os 
import json
import sys
import pika
import os
import time
import ssl
import logging
from src.commands import *

# LOAD CONFIGURATION
try:
    import config.config as config
except:
    print('[x] Configuration file not found or has an invalid format.')
    sys.exit(1)

credentials = pika.PlainCredentials(
    config.node_user, 
    config.node_password
)

# CREATE RABBITMQ CONNECTION AND QUEUE
if config.ssl_active:
    # Create SSL context
    context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
    context.check_hostname = False
    # Load CA certificate, client certificate, and client key
    context.load_verify_locations(cafile = config.ssl_cafile_path)
    context.load_cert_chain(
        certfile = config.ssl_client_cert_path, 
        keyfile = config.ssl_client_keys_path
    )
    # Set up connection parameters
    ssl_options = pika.SSLOptions(context, config.central_server_ip)
    params = pika.ConnectionParameters(
        host = config.central_server_ip,
        port = config.ssl_central_server_port,
        virtual_host = config.central_rabbitmq_vhost,
        ssl_options = ssl_options,
        credentials = credentials
    )
else:
    params = pika.ConnectionParameters(
        host = config.central_server_ip,
        port = config.ssl_central_server_port,
        virtual_host = config.central_rabbitmq_vhost,
        heartbeat = 600,
        blocked_connection_timeout = 300,
        credentials = credentials
    )
connection = pika.BlockingConnection(params)

# Create channel
channel = connection.channel()

# Declare queue
queue_name = config.node_name
channel.queue_declare(queue=queue_name)

# Define logger and initialize
def setup_logger():
    logger = logging.getLogger("receiver")
    logger.setLevel(logging.DEBUG)

    log_file = "receiver.log"
    fh = logging.FileHandler(log_file)
    fh.setLevel(logging.DEBUG)

    # Create a console handler and set its level to WARNING to avoid duplicate logs
    ch = logging.StreamHandler()
    ch.setLevel(logging.WARNING)

    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s", datefmt="%Y-%m-%d %H:%M:%S")
    fh.setFormatter(formatter)
    ch.setFormatter(formatter)

    logger.addHandler(fh)
    logger.addHandler(ch)

    logger.propagate = False

    return logger

logger = setup_logger() 


def on_request(ch, method, props, body):
    logger.info("[.] Received a message")

    try:
        # Extracting tool_id from the body
        print(body.decode('utf-8'))
        tool_id, task_id, execution_id = map(str, body.decode('utf-8').split(':'))
        logger.info(f'[.] Received command for tool_id: {tool_id}, task_id: {task_id}, execution_id: {execution_id}')

        response = None  # Initialize response to None
        command_message = None  # Initialize command_message to None

        try:
            logger.debug(f"[DEBUG] Running task_id: {task_id}, execution_id: {execution_id}")
            result = run_tool(task_id, execution_id)
            if isinstance(result, tuple):
                response, command_message = eval(result)
            else:
                response = result  # It's an error response
                command_message = None
            logger.debug(f"[DEBUG] Ran task_id: {task_id}, execution_id: {execution_id}")

            logger.debug(f"[DEBUG] Processed response for task_id: {task_id}")

            if isinstance(response, bytes):
                response = response.decode('utf-8')  # Decode bytes to string
            elif isinstance(response, dict):
                response = json.dumps(response)  # Convert dictionary to JSON string
            elif isinstance(response, tuple):
                response = response[0]
            elif isinstance(response, str):
                response = response.encode('utf-8')
            elif response is None:
                response = json.dumps({"message": f"Command not found for task_id: {task_id}"})
            logger.info(f"RESPONSE: {response}, {command_message}")
        except Exception as e:
            response = {"error": "Error raised when running the tool"}
            logger.exception(f'[x] Got error: {e}')

        try:
            if isinstance(response, str):
                response = response.encode('utf-8')
            response_message = {"response": response.decode('utf-8'), "command_message": command_message}
            ch.basic_publish(
                exchange='',
                routing_key=props.reply_to,
                properties=pika.BasicProperties(correlation_id=props.correlation_id),
                body=json.dumps(response_message).encode('utf-8')
            )
            ch.basic_ack(delivery_tag=method.delivery_tag)
            logger.info(f"[.] Done processing task_id: {task_id}, execution_id: {execution_id}")
        except Exception as e:
            logger.exception("Error when publishing the response")

    except Exception as ex:
        logger.exception("Unhandled exception in on_request: %s", ex)

    logger.info("[.] Awaiting for requests")


def run_receiver():
    logger.info(f"[.] Receiver process ID: {os.getpid()}")

    try:
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=on_request)
        logger.info("[.] Awaiting for requests")
        channel.start_consuming()

    except pika.exceptions.StreamLostError as e:
        logger.error("SSL connection lost. Reconnecting...")
        # Sleep for a while before attempting to reconnect
        time.sleep(5)
        run_receiver()

    except Exception as e:
        logger.exception("Start receiver not working")

if __name__ == "__main__":
    run_receiver()







