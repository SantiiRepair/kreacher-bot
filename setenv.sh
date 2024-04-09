#!/bin/bash

Cyan="\033[0;36m"
CWD=$(pwd)

GO_VERSION="1.22.1"
PIPER_VERSION="1.2.0"

install_chrome() {
    if [ -z "$(which google-chrome-stable)" ]; then
        wget -O /tmp/google-chrome.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
        $SUDO dpkg -i /tmp/google-chrome.deb; $SUDO apt-get -fy install
        rm -rf /tmp/google-chrome.deb
    fi
}

install_yt_dlp() {
    if [ -z "$(which yt-dlp)" ]; then
        wget https://github.com/yt-dlp/yt-dlp/releases/latest/download/yt-dlp
        $SUDO mv yt-dlp /usr/bin/yt-dlp
        $SUDO chmod +rwx /usr/bin/yt-dlp
    fi
}

install_speedtest() {
    if [ -z "$(which speedtest)" ]; then
        wget -O speedtest.py https://github.com/sivel/speedtest-cli/blob/master/speedtest.py?raw=true
        pyinstaller --onefile speedtest.py
        $SUDO mv dist/speedtest /usr/bin/speedtest
        $SUDO chmod +rwx /usr/bin/speedtest
        rm -rf speedtest.py build dist __pycache__ *.spec
    fi
}


install_piper() {
    if [ -z "$(which piper)" ]; then
        wget https://github.com/rhasspy/piper/releases/download/v${PIPER_VERSION}/piper_amd64.tar.gz
        $SUDO tar -C /usr/local -xzf piper_amd64.tar.gz
        echo "export PATH=$PATH:/usr/local/piper" >> ~/.bashrc
        rm -rf piper_amd64.tar.gz
    fi
}

if [ "$1" == "--sudo" ]; then
    SUDO="sudo"
else
    SUDO=""
fi

$SUDO apt-get update && $SUDO apt-get upgrade -y
$SUDO apt-get install -y curl \
                         gcc \
                         build-essential \
                         libx11-dev \
                         git-all \
                         python3 \
                         python3-pip \
                         ffmpeg \
                         tree
                         
python3 -m pip install pyinstaller

if [ "$1" == "--sudo" ]; then
    $SUDO apt-get install -y postgresql

    if [ -z "$(which redis-cli)" ]; then
        $SUDO apt-get install -y lsb-release gpg
        curl -fsSL https://packages.redis.io/gpg | $SUDO gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
        echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | $SUDO tee /etc/apt/sources.list.d/redis.list
        $SUDO apt-get install redis -y
    fi

    if [ -z "$(command -v go)" ]; then
        wget -O go.tar.gz https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
        $SUDO rm -rf /usr/local/go && $SUDO tar -C /usr/local -xzf go.tar.gz
        echo "export PATH=$PATH:/usr/local/go/bin" >> ~/.bashrc
        rm -rf go.tar.gz
    fi
fi

install_chrome
install_yt_dlp
install_speedtest
install_piper

echo -e "\n${Cyan}Successfully installed resources!"
cd $CWD
exit 0
