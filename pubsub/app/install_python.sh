#!/bin/bash -xe

# We have not installed the software
cd python 
sudo apt-get install python3
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
pip install --trusted-host pypi.python.org -r requirements.txt
rm get-pip.py.*
