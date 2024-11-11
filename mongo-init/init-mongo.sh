#!/bin/bash

# Check if the initialization has already been performed
if [ -f /data/db/.init_done ]; then
  echo "Initialization already done. Skipping."
else
  # Create the init-mongo.js script with environment variables
  cat <<EOF > /docker-entrypoint-initdb.d/init-mongo.js
db = db.getSiblingDB('admin');

if (db.system.users.find({ user: "$MONGODB_USERNAME" }).count() === 0) {
  db.createUser({
    user: "$MONGODB_USERNAME",
    pwd: "$MONGODB_PASSWORD",
    roles: [
      {
        role: "readWrite",
        db: "$MONGODB_DATABASE"
      }
    ]
  });
}
db = db.getSiblingDB('$MONGODB_DATABASE'); 
if (db.getCollectionNames().indexOf('files') === -1) {
  db.createCollection('files'); 
  print('Collection "files" created.');
} else {
  print('Collection "files" already exists.');
}
EOF

  # Create a flag file to indicate that initialization is done
  touch /data/db/.init_done
fi

# Execute the original entrypoint script
exec /usr/local/bin/docker-entrypoint.sh mongod --auth

# Cleanup: Remove the init-mongo.js script
rm -f /docker-entrypoint-initdb.d/init-mongo.js