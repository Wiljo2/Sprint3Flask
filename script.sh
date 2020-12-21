#!/bin/bash
echo "Starting my app."
cd  /home/ubuntu/Sprint3Flask
. myentorno/bin/activate
gunicorn --workers=20 -b 0.0.0.0:443 --keyfile=llaveprivada.pem wsgi:application