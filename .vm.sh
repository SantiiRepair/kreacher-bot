#!/bin/bash

sudo apt-get update && sudo apt-get upgrade -y

if ! command -v redis-cli >/dev/null 2>&1; then
    sudo apt-get install -y lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
    sudo apt-get update && sudo apt-get install redis -y
fi

if ! command --version google-chrome >/dev/null 2>&1; then
    wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i /tmp/google-chrome-stable_current_amd64.deb; sudo apt-get -fy install
    rm -rf /tmp/google-chrome-stable_current_amd64.deb
fi