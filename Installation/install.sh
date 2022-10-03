#!/bin/sh
sudo apt-get update -y

sudo apt-get install python3-pip

sudo apt-get install chromium-driver -y

sudo apt-get install vlc -y

sudo apt-get install openssh-server -y
sudo uwf allow ssh -y

sudo apt-get install python3.9 -y
sudo apt-get install python3-pip -y
sudo apt-get install python-selenium python3-selenium -y

sudo pip3 install -r requirements.txt
sudo pip3 install --upgrade requests
