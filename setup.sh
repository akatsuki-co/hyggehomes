#!/bin/bash

# Update Packages
sudo apt update
sudo apt upgrade

# Install Python 3, Postgres & NGINX
sudo apt install python3-pip python3-dev python3-venv libpq-dev postgresql postgresql-contrib nginx gunicorn curl

# Create Virtual Environment and Activate it
python3 -m venv ./env
source env/bin/activate

# Download Project Dependencies
pip3 install -r requirements.txt

# Check for changes in the model schema and build the database
python3 manage.py makemigrations && python3 manage.py migrate

# Collect Static files to be used for Production
python manage.py collectstatic
