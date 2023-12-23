#!/bin/bash

Cyan="\033[0;36m"

GOPATH=$(which go)
YT_DLP=$(which yt-dlp)
REDIS=$(which redis-cli)
SPEEDTEST=$(which speedtest)
CHROME_PATH=$(which google-chrome-stable)

if [ "$1" == "--local" ]; then

    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y curl git-all poppler-utils postgresql ffmpeg tree 

    if [ -z $REDIS ]; then
        sudo apt-get install -y lsb-release gpg
        curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
        echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | sudo tee /etc/apt/sources.list.d/redis.list
        sudo apt-get install redis -y
    fi

    if [ -z $CHROME_PATH ]; then
        wget -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        sudo dpkg -i /tmp/google-chrome.deb; sudo apt-get -fy install
        rm -rf /tmp/google-chrome.deb
    fi

    if [ -z $GOPATH ]; then
        wget https://go.dev/dl/go1.21.5.linux-amd64.tar.gz
        sudo rm -rf /usr/local/go && sudo tar -C /usr/local -xzf go1.21.5.linux-amd64.tar.gz
        echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
        rm -rf go1.21.5.linux-amd64.tar.gz
    fi

    if [[ -z $YT_DLP && -z $SPEEDTEST ]]; then
        sudo cp -r bin/* /usr/bin
        yt-dlp --update-to master
    fi

    echo -e "\n${Cyan}Successfully installed resources!"
    exit 0

else

    apt-get update && apt-get upgrade -y
    apt-get install -y curl git-all poppler-utils ffmpeg tree 

    if [ -z $CHROME_PATH ]; then
        wget -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        dpkg -i /tmp/google-chrome.deb; apt-get -fy install
        rm -rf /tmp/google-chrome.deb
    fi

    if [[ -z $YT_DLP && -z $SPEEDTEST ]]; then
        cp -r bin/* /usr/bin
        yt-dlp --update-to master
    fi
    
    echo -e "\n${Cyan}Successfully installed resources!"
    exit 0
fi
