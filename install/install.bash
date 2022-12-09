#!/bin/bash

sudo apt update

apt install python3 -y

apt install python3-pip -y

pip3 install flask

pip3 install pymongo

pip3 install jinja2

pip3 install flask_login

wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -

sudo apt-get install gnupg

echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list

echo "deb http://security.ubuntu.com/ubuntu focal-security main" | sudo tee /etc/apt/sources.list.d/focal-security.list

sudo apt-get install libssl1.1

sudo apt-get update

sudo apt-get install -y mongodb-org

sudo systemctl daemon-reload

sudo systemctl start mongod

sudo systemctl enable mongod

cp web.service /etc/systemd/system

sudo systemctl daemon-reload

sudo systemctl enable web

sudo systemctl start web



