# commands/data_operations.py
from pathlib import Path
from typing import List
from pymongo import MongoClient
from config import config


data_path=config.data_path
sandbox_path=config.sandbox_path

def send_input(input_directory, task_id):
    """
    Send input data to the specified directory using an API.

    Args:
    - input_directory: The path to the input directory.
    - task_id: The task ID.

    Returns:
    - None
    """
    # Placeholder logic: Assume there is an API endpoint to receive input data
    api_url = f"https://example.com/api/tasks/{task_id}/input"
    response = requests.put(api_url, json={"input_directory": input_directory})
    if response.ok:
        print("Input sent successfully.")
    else:
        print(f"Failed to send input. Status code: {response.status_code}")

def materialize_data(output_directory, materialized_data_directory):
    """
    Materialize data from another API.

    Args:
    - output_directory: The path to the output directory.
    - materialized_data_directory: The path to the materialized data directory.

    Returns:
    - None
    """
    # Placeholder logic: Assume there is an API endpoint to fetch materialized data
    api_url = "https://example.com/api/materialized_data"
    response = requests.get(api_url)
    if response.ok:
        materialized_data = response.json()
        for item in materialized_data:
            filename = item.get("filename")
            data_content = item.get("content")
            
            # Save the materialized data to the specified directory
            materialized_file_path = os.path.join(materialized_data_directory, filename)
            with open(materialized_file_path, "w") as file:
                file.write(data_content)
                
            print(f"Materialized data saved successfully to: {materialized_file_path}")
    else:
        print(f"Failed to fetch materialized data. Status code: {response.status_code}")

def retrieve_output(output_directory, task_id):
    """
    Retrieve output data from the specified directory using an API.

    Args:
    - output_directory: The path to the output directory.
    - task_id: The task ID.

    Returns:
    - None
    """
    # Placeholder logic: Assume there is an API endpoint to get output data
    api_url = f"https://example.com/api/tasks/{task_id}/output"
    response = requests.get(api_url)
    if response.ok:
        output_data = response.json()
        for item in output_data:
            filename = item.get("filename")
            output_content = item.get("content")
            
            # Save the output data to the specified directory
            output_file_path = os.path.join(output_directory, filename)
            with open(output_file_path, "w") as file:
                file.write(output_content)
                
            print(f"Output data retrieved successfully to: {output_file_path}")
    else:
        print(f"Failed to retrieve output. Status code: {response.status_code}")


def list_files(directory):
    """
    List all files in the specified directory.

    Args:
    - directory: The path to the directory.

    Returns:
    - List of file names.
    """
    files = os.listdir(directory)
    return files


