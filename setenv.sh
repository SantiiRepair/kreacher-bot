#!/bin/bash

Cyan="\033[0;36m"

KWD=$(pwd)
GOPATH=$(which go)
YT_DLP=$(which yt-dlp)
REDIS=$(which redis-cli)
PIPER_TTS=$(which piper)
SPEEDTEST=$(which speedtest)
CHROME_PATH=$(which google-chrome-stable)

if [ "$1" == "--local" ]; then

    sudo apt-get update && sudo apt-get upgrade -y
    sudo apt-get install -y curl \
                         gcc \
                         build-essential \
                         git-all \
                         poppler-utils \
                         postgresql \
                         python3 \
                         python3-pip \
                         ffmpeg \
                         tree

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

    if [[ -z $YT_DLP && -z $SPEEDTEST && -z $PIPER_TTS ]]; then
        cd temp

        wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp
        sudo mv yt-dlp /usr/bin/yt-dlp
        sudo chmod +rwx /usr/bin/yt-dlp

        wget -O speedtest.py https://github.com/sivel/speedtest-cli/blob/master/speedtest.py?raw=true
        pip3 install nuitka
        python3 -m nuitka speedtest.py
        sudo mv speedtest.bin /usr/bin/speedtest
        rm -rf speedtest.py *.build
        
        wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
        sudo tar -C /usr/local -xzf piper_amd64.tar.gz
        echo "export PATH=$PATH:/usr/local/piper" >> ~/.bashrc
        rm -rf piper_amd64.tar.gz

        cd $KWD
    fi

    echo -e "\n${Cyan}Successfully installed resources!"
    exit 0

else

    apt-get update && apt-get upgrade -y
    apt-get install -y curl \
                         gcc \
                         build-essential \
                         git-all \
                         poppler-utils \
                         python3 \
                         python3-pip \
                         ffmpeg \
                         tree

    if [ -z $CHROME_PATH ]; then
        wget -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        dpkg -i /tmp/google-chrome.deb; apt-get -fy install
        rm -rf /tmp/google-chrome.deb
    fi

    if [[ -z $YT_DLP || -z $SPEEDTEST || -z $PIPER_TTS ]]; then
        cd temp
        
        if [ -z $YT_DLP ]; then
            wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp
            mv yt-dlp /usr/bin/yt-dlp
            chmod +rwx /usr/bin/yt-dlp
        fi

        if [ -z $SPEEDTEST ]; then
            wget -O speedtest.py https://github.com/sivel/speedtest-cli/blob/master/speedtest.py?raw=true
            pip3 install nuitka
            python3 -m nuitka speedtest.py
            mv speedtest.bin /usr/bin/speedtest
            rm -rf speedtest.py *.build
        fi

        if [ -z $PIPER_TTS ]; then
            wget https://github.com/rhasspy/piper/releases/download/v1.2.0/piper_amd64.tar.gz
            tar -C /usr/local -xzf piper_amd64.tar.gz
            echo "export PATH=$PATH:/usr/local/piper" >> ~/.bashrc
            rm -rf piper_amd64.tar.gz
        fi

        cd $KWD
    fi
    
    echo -e "\n${Cyan}Successfully installed resources!"
    exit 0
fi
