#!/bin/bash

apt-get update
apt-get install -y git
git clone https://github.com/inab/openVRE.git  
#for f in openVRE/install/database/*.json; do mongoimport --host my-mongodb --db open-vre --collection vre-collection -file /mongodb/mongo-init.js -u ${MONGO_ADMIN} -p ${MONGO_ADMIN_PASS} --authenticationDatabase admin $f; done
for f in openVRE/install/database/*.json; do mongoimport --host my-mongodb --db openVRE --collection VREcollection -u 'admin' -p 'admin' --authenticationDatabase admin $f; done
