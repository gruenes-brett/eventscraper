#!/bin/bash

PROJECT_DIR=$(pwd)
HTTP_PORT=5050
HOST=127.0.0.1

source venv/bin/activate

echo -e "VirtualHost will be installed to point to $PROJECT_DIR.\n"

echo -e "The service will be accessible at $HOST:$HTTP_PORT\n"

VHOST_FILE=$PROJECT_DIR/event-scraper-vhost.conf
jinja2 event-scraper-vhost-template.conf -D "base_path=$PROJECT_DIR" -D port=$HTTP_PORT -D host=$HOST > $VHOST_FILE
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
