#!/bin/bash

pip3 install --no-deps -U pytgcalls==3.0.0.dev24 tgcalls==3.0.0.dev6 && pip3 install -r requirements.txt
wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
sudo dpkg -i google-chrome-stable_current_amd64.deb; sudo apt-get -fy install
rm -rf google-chrome-stable_current_amd64.deb; sudo apt-get update