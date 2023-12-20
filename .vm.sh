#!/bin/bash

YT_DLP=$(which yt-dlp)
CHROME_PATH=$(which google-chrome 2>&1)

sudo apt-get update && sudo apt-get upgrade -y

if ! command -v redis-cli >/dev/null 2>&1; then
    sudo apt-get install -y lsb-release curl gpg
    curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
    echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
    sudo apt-get install redis -y
fi

if ! command -v git >/dev/null 2>&1; then
    sudo apt-get install git-all -y
fi

if ! [ -x $CHROME_PATH || -z $CHROME_PATH ]; then
    wget -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
    sudo dpkg -i /tmp/google-chrome.deb; sudo apt-get -fy install
    rm -rf /tmp/google-chrome.deb
fi

if ! command version go >/dev/null 2>&1; then
    wget -O /tmp/go.tar.gz https://go.dev/dl/go1.21.5.linux-arm64.tar.gz
    rm -rf /usr/local/go && tar -C /usr/local -xzf /tmp/go.tar.gz
    echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
fi

if [ -z $YT_DLP ]; then
    sudo cp -r bin/yt-dlp /usr/bin
fi

make install