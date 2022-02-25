db.createUser(
        {
            user: "admin",
            pwd: "admin",
            roles: [
                {
                    role: "dbOwner",
                    db: "open-vre"
                }
            ]
        },
	{
	   user: "user",
	   pwd: "password",
	   roles: [
		{
		    role: "readWrite",
		    db: "open-vre"
		}
	   ]

	}
);
