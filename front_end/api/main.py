# api/main.py
import argparse
import os
import subprocess
from pathlib import Path
import asyncio
from fastapi import FastAPI, HTTPException, Query
from pymongo import MongoClient
from api.send import start_call
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi import Depends
import configparser
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.security import OAuth2PasswordBearer
from typing import List
from typing import Optional
from api.tools import *
from api.utils import *
import logging
import requests

config = configparser.ConfigParser()
config.read("config.ini")

BASE_PATH = config.get("API", "prefix", fallback="/flmanager/API/v1")

# Set up FastAPI instance with openapi_prefix
app = FastAPI(
    title="API Documentation",
    description="This is the documentation for the API",
    version="1.0",
    openapi_url=f"{BASE_PATH}/openapi.json",
    openapi_prefix=None,  # Set openapi_prefix to None to remove the base path
)

if config.getboolean('Logging', 'debug'):
    logging_level = logging.DEBUG
else:
    logging_level = logging.INFO

# Set up logging
logging.basicConfig(ilename=config['Logging']['logfile'], level=logging_level, format='%(asctime)s - %(levelname)s: %(message)s')

# Enable Swagger UI
app.add_route(
    f"{BASE_PATH}/docs",
    get_swagger_ui_html(openapi_url=f"{BASE_PATH}/openapi.json", title="API Documentation"),
)
app.add_route(
    f"{BASE_PATH}/redoc",
    get_redoc_html(openapi_url=f"{BASE_PATH}/openapi.json", title="API Documentation"),
)

# Serve Swagger UI and ReDoc static files
app.mount(f"{BASE_PATH}/docs/static", StaticFiles(directory="api/static"), name="docs_static")

# Read OAuth configuration from config.ini

enable_oauth = config.getboolean("OAuth", "enable_oauth", fallback=False)
keycloak_url = config.get("OAuth", "keycloak_url", fallback="")
client_id = config.get("OAuth", "client_id", fallback="")
client_secret = config.get("OAuth", "client_secret", fallback="")
# Set up OAuth2 password bearer scheme
#oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/flmanager/API/v1/token")
optional_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/flmanager/API/v1/token", auto_error=False)

# MongoDB connection
mongo_connection_string = config.get("MongoDB", "mongo_connection_string", fallback="")
mongo_database_name = config.get("MongoDB", "mongo_database_name", fallback="FLdb")

# Set up MongoDB connection
client = MongoClient(mongo_connection_string)
db = client[mongo_database_name]
tools_collection = db["tools"]
tasks_collection = db["tasks"]
hosts_collection = db["hosts"]

# Store information about running jobs
running_jobs = {}

# API Endpoint: Get access token
@app.post("/flmanager/API/v1/token", response_model=str)
async def get_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    try:
        token_url = f"{keycloak_url}/protocol/openid-connect/token"
        payload = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "password",
            "username": form_data.username,
            "password": form_data.password,
        }
        logging.debug(token_url)
        logging.debug(payload)

        response = requests.post(token_url, data=payload)
        response_json = response.json()
        logging.debug(response_json)
        if "access_token" not in response_json:
            raise HTTPException(status_code=401, detail="Invalid credentials")

        return response_json["access_token"]

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Failed to get access token")


# Dependency function to validate OAuth token
def validate_oauth_token(token: str):
    try:
        introspection_endpoint = f"{keycloak_url}/protocol/openid-connect/token/introspect"
        introspection_payload = {
            "token": token,
            "client_id": client_id,
            "client_secret": client_secret,
        }
        logging.debug(introspection_endpoint)
        logging.debug(introspection_payload)

        introspection_response = requests.post(introspection_endpoint, data=introspection_payload)
        introspection_json = introspection_response.json()
        logging.debug(introspection_json)

        # Check if the token is valid
        if not introspection_json.get("active"):
            raise HTTPException(status_code=401, detail="Invalid authentication token")

        # Token is valid
        return True

    except requests.exceptions.RequestException:
        raise HTTPException(status_code=500, detail="Failed to validate authentication token")

# Modify the function to directly check the configuration
async def optional_oauth_token(token: str = Depends(optional_oauth2_scheme)):
    if enable_oauth:
        # If OAuth is enabled, validate the token
        return validate_oauth_token(token)
    else:
        # If OAuth is not enabled, return True without validation
        return True

# CRUD operations for tools
@app.get(f"{BASE_PATH}/tools", summary="List Tools", description="Get information about the available tools.")
def list_tools_endpoint(oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")
    return list_tools(tools_collection)

@app.get(f"{BASE_PATH}/tools/{{tool_id}}", summary="Read Tool", description="Get information about a specific tool.")
def read_tool_endpoint(tool_id, oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")
    return read_tool(tool_id, tools_collection, tasks_collection)

@app.get(f"{BASE_PATH}/tools/tasks", summary="List Tasks", description="Get information about the available tasks.")
def list_tasks_endpoint(oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")
    return list_tasks(tasks_collection)

# Trigger Tool endpoint
@app.get(f"{BASE_PATH}/tools/job/{{tool_name}}", summary="Trigger Tool", description="Trigger a specific tool.")
def trigger_tool_endpoint(tool_name: str, nodes: Optional[List[str]] = None, oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")

    try:
        print(f"Received tool_name: {tool_name}")
        tool_id = get_tool_id_by_name(tool_name, tools_collection)
        print(f"Found tool: {tool_id}")
        print(f"Tool ID: {tool_id}")

        if tool_id is not None:
            result = trigger_tool_by_id(tool_id, tools_collection, tasks_collection, nodes)
            return {"status": "success", "result": result}
        else:
            raise HTTPException(status_code=404, detail="Tool not found")
    except HTTPException as e:
        print(e)
        return {"status": "failure", "message": str(e)}


# CRUD operations for hosts
@app.get(f"{BASE_PATH}/hosts", summary="List Federated Hosts", description="Get information about all federated hosts.")
def list_hosts_endpoint(oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")
    return list_hosts(hosts_collection)


@app.get(f"{BASE_PATH}/hosts/health", summary="Health Check", description="Perform a basic health check on the system.")
def health_endpoint(nodes: Optional[List[str]] = Query(None, description="List of nodes for health check"),
                    oauth_token: bool = Depends(optional_oauth_token)):
    try:
        tool_id = get_tool_id_by_name("health-check", tools_collection)

        if tool_id is not None:
            result = trigger_tool_by_id(tool_id, tools_collection, tasks_collection, nodes)
            logging.info(f"Health check result: {result}")
            return {"status": "success", "message": "Health check passed.", "result": result}
        else:
            raise HTTPException(status_code=404, detail="Tool not found")
    except HTTPException as e:
        print(e)
        return {"status": "failure", "message": str(e)}

@app.get(f"{BASE_PATH}/hosts/{{host_id}}", summary="Read Federated Host", description="Get information about a specific federated host.")
def read_host_endpoint(host_id: str, oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")
    return read_host(host_id, hosts_collection)


# CRUD operations for data
@app.get(f"{BASE_PATH}/data/files", summary="List User's Available Files", description="Get a list of user's available files as URIs.")
def list_user_files_endpoint(oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")
    return list_user_files()

@app.get(f"{BASE_PATH}/data/file/{{file_id}}", summary="Retrieve File Entry", description="Retrieve the file entry, defining its location, metadata, etc.")
def retrieve_file_entry_endpoint(file_id: str, oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")
    return retrieve_file_entry(file_id)

@app.get(f"{BASE_PATH}/data/file/{{file_id}}/access", summary="Retrieve File Access URI", description="Returns a URI used to fetch the bytes of the file (computational nodes only).")
def retrieve_file_access_uri_endpoint(file_id: str, oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")
    return retrieve_file_access_uri(file_id)

@app.put(f"{BASE_PATH}/data/file/{{file_path}}", summary="Create New File Entry", description="Creates a new file entry.")
def create_new_file_entry_endpoint(file_path: str, oauth_token: bool = Depends(optional_oauth_token)):
    if not oauth_token:
        raise HTTPException(status_code=401, detail="OAuth token validation failed")
    return create_new_file_entry(file_path)



# Function to get the OpenAPI documentation
@app.get(
    f"{BASE_PATH}/docs",
    tags=["docs"],
    summary="API Documentation",
    description="Retrieve the OpenAPI JSON document, which describes the API's structure and operations.",
)

def get_openapi_endpoint():
    return get_openapi(app)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="port to run the API on, default 5000", type=int, default=5000)
    args = parser.parse_args()

    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=args.port, log_level="debug")


