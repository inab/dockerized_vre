FROM mongo:3.6.21


CMD for f in install/database/*.json; do mongoimport --host my-mongodb --db open-vre --collection vre-collection $f; done
