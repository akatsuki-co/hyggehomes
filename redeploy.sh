#!/bin/bash

echo Updating Packages
# Update Packages
sudo apt update
sudo apt upgrade

echo downloading Project Dependencies
# Download Project Dependencies
pip3 install -r requirements.txt

echo downloading gunicorn
pip install gunicorn

echo Migrating project...
# Check for changes in the model schema and build the database
python3 manage.py makemigrations && python3 manage.py migrate

# Collect Static files to be used for Production
python manage.py collectstatic

echo Reload NGINX and Gunicorn
sudo systemctl restart nginx
sudo systemctl restart gunicorn


echo Done
