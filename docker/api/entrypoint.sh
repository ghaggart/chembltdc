#!/usr/bin/env bash

#apt-get install gunicorn

pip install markupsafe==2.0.1
python -m pip install --upgrade pip
pip install -r /opt/requirements.txt

cd /opt/api

export FLASK_CONFIG="/opt/api/config.py"

export FLASK_APP=app/__init__.py

flask fab create-admin --username $API_ADMIN_USER --password $API_ADMIN_PASSWORD --firstname admin --lastname admin --email $API_ADMIN_EMAIL

gunicorn --reload --bind 0.0.0.0:5000 wsgi:app

