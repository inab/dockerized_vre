# api/utils.py
from pathlib import Path
from typing import List
from fastapi import HTTPException

def check_path_exists(path):
    return Path(path).exists()

def list_files_in_directory(directory):
    return [str(file) for file in Path(directory).iterdir() if file.is_file()]


# Add more utility functions as needed

