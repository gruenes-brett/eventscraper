#!/bin/bash

PROJECT_DIR=$(pwd)

echo "VirtualHost will be installed to point to $PROJECT_DIR."

echo "Please enter the port where the service should be accessible on:"
read HTTP_PORT

VHOST_FILE=$PROJECT_DIR/event-scraper-vhost.conf
cat event-scraper-vhost-template.conf | sed s~XpathX~$PROJECT_DIR~g | sed s~XportX~$HTTP_PORT~g > $VHOST_FILE
echo "$VHOST_FILE written"

TARGET=/etc/apache2/conf-enabled/event-scraper-vhost.conf
echo "Linking $TARGET to $VHOST_FILE"
if test -h $TARGET; then
  sudo rm $TARGET
fi
sudo ln -s -t /etc/apache2/conf-enabled $VHOST_FILE

echo "Reloading apache2"
sudo service apache2 reload
sudo service apache2 status