import shutil
import os
from urllib.parse import urlparse
from config import config
import subprocess
import logging 


def fetch_source_code(tool_info, logger):
    try:
        source_code_info = tool_info.get("info_from_tasks_collection", {}).get("source_code", {})
        source_code_url = source_code_info.get("url", "")
        commit_hash = source_code_info.get("commit_hash", "")
        sandbox_path = config.sandbox_path

        if not source_code_url:
            logger.error("Source code URL is not provided in the tool definition.")
            return False

        # Extract the repository name from the Git URL
        repo_name = os.path.splitext(os.path.basename(urlparse(source_code_url).path))[0]

        source_code_path = os.path.join(sandbox_path, repo_name)

        if os.path.exists(source_code_path):
            # If it exists, perform a git pull to update to the latest commit
            logger.info(f"Source code directory already exists. Performing git pull.")
            subprocess.run(["git", "pull"], cwd=source_code_path, capture_output=True)
        else:
            # If it doesn't exist, perform a git clone
            logger.info(f"Source code directory does not exist. Performing git clone.")
            subprocess.run(["git", "clone", source_code_url, source_code_path], capture_output=True)

        # If a commit hash is provided, perform a git checkout
        if commit_hash:
            logger.info(f"Checking out specific commit: {commit_hash}")
            subprocess.run(["git", "checkout", commit_hash], cwd=source_code_path, capture_output=True)

        return True
    except Exception as e:
        logger.error(f"Error fetching source code: {e}")
        return False





def capture_docker_logs(container_id, execution_id, task_id, logger):
    try:
        # Create a folder for the execution if it doesn't exist
        execution_folder = os.path.join(config.sandbox_path, execution_id)
        os.makedirs(execution_folder, exist_ok=True)

        # Open the logs file for appending with task_id
        docker_logs_file = os.path.join(execution_folder, f"{task_id}_docker_logs.txt")
        with open(docker_logs_file, "a") as log_file:
            log_file.write(f"\n\n[Container ID: {container_id}]\n")

        # Start a background process to continuously capture logs
        logs_command = f"docker logs -f {container_id}"
        process = subprocess.Popen(logs_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, universal_newlines=True)

        # Continuously append logs to the execution logs file until the container stops
        while process.poll() is None:
            logs_output = process.stdout.readline()
            if logs_output:
                with open(docker_logs_file, "a") as log_file:
                    log_file.write(logs_output)

        # Log container exit information
        exit_code = process.returncode
        logger.info(f"Container exited with code: {exit_code}")

    except Exception as e:
        # Log exception information
        logger.error(f"Error capturing Docker logs: {e}")



