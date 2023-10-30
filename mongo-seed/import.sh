#!/bin/bash

apt-get update
apt-get install -y git rsync

# Import JSON files into MongoDB using environment variables for credentials
for f in /install_data/database/*.json; do
    mongoimport --host ${MONGO_SERVER} \
                --port ${MONGO_PORT} \
                --db ${MONGO_DB} \
               
               # --collection ${MONGO_INITDB_COLLECTION} \
               # --drop \ # With --drop: If the specified collection exists, mongoimport will remove it, effectively dropping the collection along with all its documents. Then it will import the data into a new collection with the specified name.

                -u ${MONGO_INITDB_ROOT_USERNAME} \
                -p ${MONGO_INITDB_ROOT_PASSWORD} \
                --authenticationDatabase admin \
                $f
done

# Copy userdata
rsync -av --delete /install_data/data/userdata /shared_data




