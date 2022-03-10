#!/bin/sh
sudo apt-get install python-selenium python3-selenium
sudo pip3 install -r requirements.txt
wget https://chromedriver.storage.googleapis.com/99.0.4844.51/chromedriver_linux64.zip
unzip chromedriver_linux64.zip
./chromedriver