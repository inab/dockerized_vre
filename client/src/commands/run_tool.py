import json
import os
import subprocess
import argparse
import requests
from .check_resources import *
from .manage_docker_container import manage_docker_container
from .utils import *
from config import config
import logging
import time
import threading


def fetch_tool_info(tool_id):
    try:
        # Make a request to the endpoint to get the tool information
        response = requests.get(f"https://fl.bsc.es/flmanager/API/v1/tools/{tool_id}")
        tool_info = response.json()
        return tool_info
    except Exception as e:
        print(f"Error fetching tool information: {e}")
        return None


def start_tool(tool_info, task_id, execution_id, logger=None, **kwargs):
    try:
        flower_ssl_cacert = config.ssl_cafile_path
        sandbox_path = config.sandbox_path
        data_path = config.data_path  # Assuming data_path is the desired host path

        # Construct the Docker command
        command = ["docker", "run", "-d"]

        # Set the shared memory size if memory is specified in the tool definition
        memory = tool_info.get("info_from_tasks_collection", {}).get("memory", "")
        if memory:
            command += ["--shm-size=" + memory]

        for volume in tool_info.get("info_from_tasks_collection", {}).get("volumes", []):
            host_path = volume.get("host_path", "")
            container_path = volume.get("container_path", "")

            # Replace variables in host_path and container_path
            host_path = host_path.replace("$SANDBOX_PATH", sandbox_path)
            host_path = host_path.replace("$DATA_PATH", data_path)
            container_path = container_path.replace("$SANDBOX_PATH", sandbox_path)
            container_path = container_path.replace("$DATA_PATH", data_path)

            # Mount the volume in the Docker command
            command += ["-v", f"{host_path}:{container_path}"]

        persistent = tool_info.get("info_from_tasks_collection", {}).get("persistent", "")
        if persistent:
            command += ["-v", f"{sandbox_path}:{sandbox_path}"]

        for var_env, var_value in tool_info.get("info_from_tasks_collection", {}).get("var_envs", {}).items():
            # Replace the value with the environment variable if it starts with '$'
            if var_value.startswith('$'):
                env_variable = var_value[1:]  # Remove the '$' symbol
                env_value = os.environ.get(env_variable, '')
                command += ["-e", f"{var_env}={env_value}"]
            else:
                command += ["-e", f"{var_env}={var_value}"]

        # Handle port mappings
        port_mappings = tool_info.get("info_from_tasks_collection", {}).get("port_mappings", {})
        if port_mappings:
            container_port = port_mappings.get("container_port", "")
            host_port = port_mappings.get("host_port", "")

            if container_port and host_port:
                command += ["-p", f"{host_port}:{container_port}"]

        docker_image_info = tool_info.get("info_from_tasks_collection", {}).get("image", {})
        docker_image_name = docker_image_info.get("url", "")
        docker_image_cmd = docker_image_info.get("cmd", "")

        if not docker_image_name:
            raise ValueError("Docker image name is empty")

        command += [docker_image_name]

        if docker_image_cmd:
            command += docker_image_cmd.split()

        full_command = " ".join(command)

        if logger:
            logger.info(f"Executing Docker command: {full_command}")

        # Start the Docker container
        check = subprocess.run(full_command, shell=True, capture_output=True)

        if check.returncode == 0:
            response = check.stdout.decode().strip()
            container_id = response.strip()

            # Log container start information
            logger.info(f"Tool started successfully for task_id: {task_id}")
            logger.info(f"Container ID: {container_id}")

            # Create a thread to capture Docker logs in the background
            logs_thread = threading.Thread(target=capture_docker_logs, args=(container_id, execution_id, task_id, logger))
            logs_thread.start()

            return container_id

        else:
            # Log error information
            error_message = f"Error starting Docker tool for task_id {task_id}.\nExit code: {check.returncode}\nError output: {check.stderr.decode()}"
            logger.error(error_message)
            logger.error(f"Command: {full_command}")
            return error_message

    except Exception as e:
        # Log exception information
        error_message = f"Error starting Docker tool for task_id {task_id}.\nTraceback: {e}"
        logger.error(error_message)
        return error_message




def run_tool(task_id, execution_id):
    try:
        logger = logging.getLogger("receiver")

        # Perform pre-checks if specified in the tool entry
        tool_info = fetch_tool_info(task_id)
        if tool_info:
            pre_checks_result = pre_checks()
            logger.info(f"Pre-checks result: {pre_checks_result}")

            # Check if Docker image is specified
            docker_image_name = tool_info.get("info_from_tasks_collection", {}).get("image", {}).get("url", "")
            if not docker_image_name:
                # If no Docker image is specified, perform health check and return the result
                health_check_result = pre_checks()  # You can replace pre_checks with the appropriate health check function
                logger.warning("No Docker image specified. Performing health check instead.")
                logger.info(f"Health check result: {health_check_result}")
                return health_check_result

            # Fetch the source code before starting the tool
            source_code_fetch_result = fetch_source_code(tool_info, logger)
            if not source_code_fetch_result:
                return "Error fetching source code. Aborting tool execution."

            # Perform Docker image pull
            manage_docker_container("pull", docker_image_name)
            logger.info(f"Docker image pulled successfully for task_id: {task_id}, docker_image_name: {docker_image_name}")

            # Get the command response
            response = start_tool(tool_info, task_id, execution_id, logger=logger)

            if response:
                # Extract the Docker container ID from the response
                container_id = response.strip()

                logger.info(f"Tool started successfully for task_id: {task_id}")
                logger.info(f"Container ID: {container_id}")

                return container_id
            else:
                return f"Error starting Docker tool for task_id: {task_id}"
        else:
            return f"Error fetching tool information for task_id: {task_id}"
    except Exception as e:
        return f"Error occurred: {e}"

if __name__ == '__main__':
    # Get the task_id from the command line using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_id", help="ID of the task to run", type=str)
    args = parser.parse_args()
    logger.info(f"Running tool for task_id: {args.task_id}")
    run_tool(args.task_id)


