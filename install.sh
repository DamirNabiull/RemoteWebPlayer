#!/bin/sh
sudo apt-get update

sudo apt-get install chromium-driver

sudo apt-get install openssh-server
sudo uwf allow ssh

sudo apt-get install python3.9
sudo apt-get install python3-pip
sudo apt-get install python-selenium python3-selenium
sudo pip3 install -r requirements.txt