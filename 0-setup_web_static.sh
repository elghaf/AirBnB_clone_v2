#!/usr/bin/env bash
# This bash script sets a webserver to answer requestes for static webpages

# The first step is to update the packages already on the webserver
sudo apt-get update

# The second step is to install Nginx
sudo apt-get -y install nginx
sudo ufw allow 'Nginx HTTP'

# The third step is to create the folders below if they do not exist
#   * '/data'
#   * '/data/web_static/'
#   * '/data/web_static/releases/'
#   * '/data/web_static/releases/test/'
#   * '/data/web_static/shared/'
sudo mkdir -p /data/
sudo mkdir -p /data/web_static/
sudo mkdir -p /data/web_static/releases/
sudo mkdir -p /data/web_static/shared/
sudo mkdir -p /data/web_static/releases/test/

# The fourth step is to create a fake index HTML file saved as '/data/web_static/releases/test/index.html'
 sudo touch /data/web_static/releases/test/index.html
sudo echo "<html>
  <head>
  </head>
  <body>
    Holberton School
  </body>
</html>" | sudo tee /data/web_static/releases/test/index.html
# The fifth step is to create a symbolic link for '/data/web_static/current' and
# '/data/web_static/releases/test/'
sudo ln -s -f /data/web_static/releases/test/ /data/web_static/current

# The sixth step is to give recursive ownership of '/data/' folder to ubuntu and GROUP
sudo chown -R ubuntu:ubuntu /data/

# The seventh step is to update the configuration of Nginx to serve static web pages from '/data/web_static/current/'
# to 'hbnb_static' (ex: https://nomaetinosa.tech/hbnb_static)
sudo sed -i '/listen 80 default_server/a location /hbnb_static { alias /data/web_static/current/;}' /etc/nginx/sites-enabled/default

# The eighth stop is to Restart Nginx
sudo service nginx restart
