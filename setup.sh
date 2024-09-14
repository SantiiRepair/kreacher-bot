#!/bin/bash

PIPER_VERSION="1.2.0"
GO_VERSION=$(<.go-version)

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
        $SUDO /usr/bin/yt-dlp --update-to master
    fi
}

install_speedtest() {
    if [ -z "$(which speedtest)" ]; then
        cd deps/speedtest-cli
        python3 -m PyInstaller --onefile speedtest.py
        $SUDO mv dist/speedtest /usr/bin/speedtest
        rm -rf build dist __pycache__ *.spec
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

install_ntgcalls() {
    LATEST_URL=$(curl -s https://api.github.com/repos/pytgcalls/ntgcalls/releases/latest | grep "browser_download_url" | grep "ntgcalls.linux-x86_64-shared_libs.zip" | cut -d '"' -f 4)
    wget "$LATEST_URL" -O ntgcalls.zip
    mkdir -p shared-output
    unzip ntgcalls.zip -d shared-output

    ntgcalls="shared-output/release/include/ntgcalls.h"
    libntgcalls="shared-output/release/libntgcalls.so"

    if [ -f "$libntgcalls" ] && [ -f "$ntgcalls" ]; then
        mv "$libntgcalls" kreacher/
        mv "$ntgcalls" kreacher/ntgcalls/
    else
        echo "Error: Expected files not found after extracting ntgcalls."
        return 1
    fi

    rm ntgcalls.zip
    rm -rf shared-output
}

if [ "$1" == "--sudo" ]; then
    SUDO="sudo"
else
    SUDO=""
fi

install_deps() {
    {
        $SUDO apt-get update && $SUDO apt-get upgrade -y
        
        $SUDO apt install -y \
            rlwrap \
            build-essential \
            cmake \
            git \
            wget \
            curl \
            gcc \
            sox \
            libsox-fmt-all \
            ffmpeg \
            libx11-dev \
            libssl-dev \
            python3 \
            python3-pip \
            tree    

        python3 -m pip install pyinstaller

        if [ -z "$(command -v go)" ]; then
            wget -O go.tar.gz https://go.dev/dl/go${GO_VERSION}.linux-amd64.tar.gz
            $SUDO rm -rf /usr/local/go && $SUDO tar -C /usr/local -xzf go.tar.gz
            echo "export PATH=\$PATH:/usr/local/go/bin" >> ~/.bashrc
            rm -rf go.tar.gz
        fi
    } > /dev/null 2>&1    
}

install_deps
install_ntgcalls
install_chrome
install_yt_dlp
install_speedtest
install_piper

echo "Successfully installed resources!"
exit 0
