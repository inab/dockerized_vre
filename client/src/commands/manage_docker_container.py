import subprocess
import argparse

# Function to manage docker containers
def manage_docker_container(action, container_name):
    result = {}

    try:
        if action == "pull":
            # Check if the Docker image is available locally and pull if not
            check_output = subprocess.run(f"docker image inspect {container_name}", shell=True, capture_output=True)
            if check_output.returncode != 0:
                result['message'] = f"Docker image '{container_name}' not found locally. Pulling the image..."
                subprocess.run(f"docker pull {container_name}", shell=True, check=True)
            else:
                result['message'] = f"Docker image '{container_name}' is already available locally."
        elif action == "stop":
            # Stop the Docker container
            subprocess.run(f"docker stop {container_name}", shell=True, check=True)
            result['message'] = f"Docker container '{container_name}' stopped successfully."
        elif action == "remove":
            # Remove the Docker container
            subprocess.run(f"docker rmi {container_name}", shell=True, check=True)
            result['message'] = f"Docker container '{container_name}' removed successfully."
        else:
            result['message'] = f"Invalid action: {action}"
    except Exception as e:
        result['error'] = f"Error managing Docker container: {e}"

    return result

if __name__ == '__main__':
    # Get arguments from the command line using argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--function", help="function to execute (manage_docker_container)", type=str, default='manage_docker_container')
    parser.add_argument("--argument", help="arguments to pass to function", type=str, default='manage_docker_container', nargs='+')
    args = parser.parse_args()

    result = manage_docker_container(*args.argument)
    print(json.dumps(result))


