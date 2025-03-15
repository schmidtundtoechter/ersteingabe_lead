#!/bin/bash

sudo chmod 666 /var/run/docker.sock
sudo chown -R frappe:frappe /workspace
rsync -avP /workspace-local/development/ /workspace/development/

if [ -d /home/frappe/.ssh-mount ]; then
    echo "### STEP 5.5 Copy ssh keys"
    rsync -avP /home/frappe/.ssh-mount/ /home/frappe/.ssh/
    find ~/.ssh -type f -exec chmod 600 {} \;
    find ~/.ssh -type d -exec chmod 700 {} \;
fi

ERPNEXT_VERSION=15

echo "### STEP 6 Initialize frappe bench with frappe version ${ERPNEXT_VERSION} and Switch directory"
cd /workspace/development
bench init --skip-redis-config-generation --frappe-branch version-${ERPNEXT_VERSION} frappe-bench
cd frappe-bench

echo "### STEP 7 Setup hosts"
# We need to tell bench to use the right containers instead of localhost. Run the following commands inside the container:
bench set-config -g db_host mariadb
bench set-config -g redis_cache redis://redis-cache:6379
bench set-config -g redis_queue redis://redis-queue:6379
#bench set-config -g redis_socketio redis://redis-socketio:6379
bench set-config -g redis_socketio redis://redis-cache:6379
# For any reason the above commands fail, set the values in common_site_config.json manually.
#{
#  "db_host": "mariadb",
#  "redis_cache": "redis://redis-cache:6379",
#  "redis_queue": "redis://redis-queue:6379",
#  "redis_socketio": "redis://redis-socketio:6379"
#}

echo "### STEP 8 Create a new site"
# sitename MUST end with .localhost for trying deployments locally.
# MariaDB root password: 123
bench new-site d-code.localhost --no-mariadb-socket 

echo "### STEP 9 Set bench developer mode on the new site"
bench --site d-code.localhost set-config developer_mode 1
bench --site d-code.localhost clear-cache   

echo "### STEP 10 Install ERPNext"
bench get-app --branch version-${ERPNEXT_VERSION} --resolve-deps erpnext
bench --site d-code.localhost install-app erpnext

echo "### STEP 11 Start Frappe bench"
echo "Now go to /workspace/development/frappe-bench/ and run bench start"
echo "Then open your browser and go to http://d-code.localhost:8000"
