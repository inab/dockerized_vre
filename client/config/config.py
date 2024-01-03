#!/usr/bin/env python
import os

# ----------------------------------------------------------------
# IMPORTANT NOTES TO DEVELOPERS
# 1 - MAKE A COU OF THIS FILE AND REMOVE THE "_template" PART
# 2 - THE .GITIGNORE INCLUDES A PATTERN TO NOT COMMIT THIS FILE, 
# BUT MAKE SURE IT DOES NOT GET INCLUDED IN ANY OF YOUR COMMITS
# ----------------------------------------------------------------

# ----------------------------------------------------------------
# REPLACE THE FOLLOWING VARIABLES WITH YOUR OWN
# ----------------------------------------------------------------
node_name     = 'UB'
#node_name can be "UB","BUCH","GEM","ICRC","KUH","UCL","UMCU","AUMC","VHIR",

sandbox_path     = '/home/openvre/sandbox'
path_to_code  = ''
data_path     = ''
node_user     = 'centre5'
node_password = 'password'
cert_phrase   = 'a-stronger-password'

# ----------------------------------------------------------------
# REPLACE THE FOLLOWING VARIABLES WITH YOUR OWN
# ----------------------------------------------------------------
ssl_active              = True
ssl_central_server_port = 5671
ssl_cafile_path         = '/home/openvre/config/rabbitmq-ca/rootCA_cert.pem'
ssl_client_cert_path    = '/home/openvre/config/rabbitmq-ca/client_cert.pem'
ssl_client_keys_path    = '/home/openvre/config/rabbitmq-ca/client_key.pem'

# ----------------------------------------------------------------
# KEEP THE FOLLOWING VARIABLES WITH THE PROJECT'S VALUES
# ----------------------------------------------------------------
central_server_ip      = 'fl.bsc.es'
central_server_port    = 5671
central_rabbitmq_vhost = 'rabbit_server'
central_flower         = 'flower.fl.bsc.es'
central_flower_port    = 4433

# ----------------------------------------------------------------
# FL EXPERIMENT SETUP VALUES
# ----------------------------------------------------------------
docker_image_name      = 'registry.gitlab.bsc.es/bfp/fl_breast_mg_classification'
github_repo_name       = 'https://github.com/UBFL/FLClient.git'
docker_server_image_name      = 'registry.gitlab.bsc.es/fl/server/dlserver' #'registry.gitlab.bsc.es/fl/dldocker'
path_to_csv   = '/home/socayna/Desktop/CMMD_subset/info.csv'

# Export variables as environment variables
os.environ['CENTRAL_SERVER_IP'] = central_server_ip
os.environ['CENTRAL_SERVER_PORT'] = str(central_server_port)
os.environ['CENTRAL_RABBITMQ_VHOST'] = central_rabbitmq_vhost
os.environ['FLOWER_CENTRAL_SERVER_IP'] = central_flower
os.environ['FLOWER_CENTRAL_SERVER_PORT'] = str(central_flower_port)
os.environ['DOCKER_IMAGE_NAME'] = docker_image_name
os.environ['GITHUB_REPO_NAME'] = github_repo_name
os.environ['SANDBOX_PATH'] = sandbox_path
os.environ['PATH_TO_CODE'] = path_to_code
os.environ['DATA_PATH'] = data_path
os.environ['FLOWER_SSL_CACERT'] = str(ssl_cafile_path)
os.environ['DOCKER_SERVER_IMAGE_NAME'] = docker_server_image_name
os.environ['PATH_TO_CSV'] = path_to_csv



