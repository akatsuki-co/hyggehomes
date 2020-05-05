#!/bin/bash

read -p "Did you create the .env file for your settings?"
read -p "What is your public IP?: "  IP

PROJECT=$(basename "$PWD")
USER=$(logname)

echo Updating Packages
# Update Packages
sudo apt update
sudo apt upgrade

echo Installing Python3, Postgres, NGINX and gunicorn
# Install Python 3, Postgres & NGINX
sudo apt install python3-pip python3-dev python3-venv libpq-dev postgresql postgresql-contrib nginx curl

echo creating virtual environment...
# Create Virtual Environment and Activate it
python3 -m venv ./env
echo activating virtual environment
source env/bin/activate

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

echo Configuring Gunicorn Socket file...
sudo cat > /etc/systemd/system/gunicorn.socket << EOF
[Unit]
Description=gunicorn socket

[Socket]
ListenStream=/run/gunicorn.sock

[Install]
WantedBy=sockets.target
EOF

echo Configuring Gunicorn Service file
sudo cat > /etc/systemd/system/gunicorn.service << EOF
[Unit]
Description=gunicorn daemon
Requires=gunicorn.socket
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=/home/$USER/$PROJECT
ExecStart=/home/$USER/$PROJECT/env/bin/gunicorn \\
          --access-logfile - \\
          --workers 3 \\
          --bind unix:/run/gunicorn.sock \\
          backend.wsgi:application

[Install]
WantedBy=multi-user.target
EOF

echo Start and enable Gunicorn socket
sudo systemctl start gunicorn.socket
sudo systemctl enable gunicorn.socket

echo Check status of gunicorn
sudo systemctl status gunicorn.socket

echo Checking the existence of gunicorn.sock
file /run/gunicorn.sock

echo Configure NGINX file
sudo cat > /etc/nginx/sites-available/$PROJECT << EOF
server {
    listen 80;
    server_name $IP;

    location = /favicon.ico { access_log off; log_not_found off; }
    location /static/ {
        root /home/$USER/$PROJECT;
    }

    location /media/ {
        root /home/$USER/$PROJECT;
    }

    location / {
        include proxy_params;
        proxy_pass http://unix:/run/gunicorn.sock;
    }
}
EOF

echo Enable the file by linking to the sites-enabled dir
sudo ln -s /etc/nginx/sites-available/$PROJECT /etc/nginx/sites-enabled

echo Testing NGINX config...
sudo nginx -t

echo Restarting NGINX...
sudo systemctl restart nginx


echo Allowing normal traffic on port 80
sudo ufw allow 'Nginx Full'

echo Reload NGINX and Gunicorn
sudo systemctl restart nginx
sudo systemctl restart gunicorn


echo Done
