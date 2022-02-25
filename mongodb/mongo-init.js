
dbCollectionName = "vre-collection";


db.createUser(
        {
            user: ${MONGO_ADMIN},
            pwd: ${MONGO_ADMIN_PASS},
            roles: [
                {
                    role: "dbOwner",
                    db: "open-vre"
                }
            ]
        },
	{
	   user: ${MONGO_USER} ,
	   pwd: ${MONGO_PASS},
	   roles: [
		{
		    role: "readWrite",
		    db: "open-vre"
		}
	   ]

	}
);

db.createCollection(dbCollectionName);

