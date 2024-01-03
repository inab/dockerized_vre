# api/tools.py
import logging
import uuid
from typing import Optional, List
from fastapi import HTTPException
from api.send import start_call  # Import the start_call function


def get_tool_id_by_name(tool_name: str, tools_collection):
    try:
        #print(f"Searching for tool: {tool_name}")
        tool = tools_collection.find_one({"_id": tool_name})
        #print(f"Found tool: {tool}")
        return tool['_id'] if tool else None
    except Exception as e:
        print(f"Error in get_tool_id_by_name: {e}")
        raise HTTPException(status_code=500, detail=f"Database error: {e}")


def trigger_tool_by_id(tool_id: str, tools_collection, tasks_collection, nodes: Optional[List[str]] = None):
    try:
        #print(f"Received tool_id: {tool_id}")
        tool_info = read_tool(tool_id, tools_collection, tasks_collection)
        #print(f"Retrieved tool_info: {tool_info}")

        # Use the provided nodes or default to the deployment plan's host_list
        deployment_plan = tool_info.get("deployment_plan", {})
        host_list = nodes or [deployment_plan.get("host_list", "default_node")]

        execution_id = str(uuid.uuid4())
        for task in tool_info.get("tasks", []):
            task_id = task.get("task_id")

            # Log the execution details for each node
            for task_node in host_list:
                print(f"Executing task_id={task_id} on node={task_node}")

                # Call start_call with execution_id, task_id, and task_node
                result = start_call(execution_id, task_id, tool_id, [task_node])  # Pass [task_node] as a list

        print(f"Tool execution successful")
        return {"status": "success", "result": result, "tool_info": tool_info, "nodes": host_list}

    except HTTPException as e:
        print(f"HTTPException: {e}")
        return {"status": "failure", "message": str(e)}


def list_tools(tools_collection):
    try:
        tools = list(tools_collection.find())
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

def read_tool(tool_id, tools_collection, tasks_collection):
    try:
        # Check the tools_collection first
        tool = tools_collection.find_one({"_id": tool_id})
        if tool:
            return tool
        else:
            # If not found in tools_collection, check tasks_collection
            task_info = tasks_collection.find_one({"_id": tool_id})
            if task_info:
                return {"info_from_tasks_collection": task_info}
            else:
                raise HTTPException(status_code=404, detail="Tool or Task not found")
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching tool information.")

def list_tasks(tasks_collection):
    try:
        tasks = list(tasks_collection.find())
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching task information.")



def get_tools():
    try:
        tools = list(tools_collection.find())
        return tools
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

def get_tasks():
    try:
        tasks = list(tasks_collection.find())
        return tasks
    except Exception as e:
        print(f"Error fetching tasks: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching task information.")


def get_tool(tool_id):
    try:
        tool = tools_collection.find_one({'id': tool_id})
        if tool:
            return tool
        else:
            raise HTTPException(status_code=404, detail="Tool not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

def get_task(task_id):
    try:
        task = tasks_collection.find_one({'_id': task_id})
        if task:
            return task
        else:
            raise HTTPException(status_code=404, detail="Task not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

def list_hosts(hosts_collection):
    try:
        hosts = list(hosts_collection.find())
        return hosts
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Database error: {e}")

def read_host(host_id, hosts_collection):
    try:
        host = hosts_collection.find_one({"_id": host_id})
        if host:
            return host
        else:
            raise HTTPException(status_code=404, detail="Federated host not found")
    except Exception as e:
        print(f"Database error: {e}")
        raise HTTPException(status_code=500, detail="An error occurred while fetching federated host information.")

# Add more functions related to tools if needed
