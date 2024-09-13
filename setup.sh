#!/bin/bash

PIPER_VERSION="1.2.0"
FFMPEG_VERSION="7.0.2"
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

install_ffmpeg() {
    wget https://ffmpeg.org/releases/ffmpeg-${FFMPEG_VERSION}.tar.xz -O deps/ffmpeg.tar.xz 
    mkdir -p deps/ffmpeg && tar -xf deps/ffmpeg.tar.xz -C deps/ffmpeg --strip-components=1 && cd deps/ffmpeg
    ./configure --enable-gpl --enable-nonfree --enable-libx264 --enable-libx265 --enable-libfdk-aac --enable-libmp3lame --enable-libopus --enable-libvorbis --enable-libvpx --enable-openssl
    make -j$(nproc) && sudo make install && cd ../..
    rm -rf deps/ffmpeg.tar.xz 
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
            autoconf \
            automake \
            build-essential \
            cmake \
            git \
            libass-dev \
            libfdk-aac-dev \
            libfreetype6-dev \
            libmp3lame-dev \
            libopus-dev \
            libtheora-dev \
            libtool \
            libvorbis-dev \
            libx264-dev \
            libx265-dev \
            libvpx-dev \
            pkg-config \
            texinfo \
            wget \
            yasm \
            curl \
            gcc \
            libx11-dev \
            libssl-dev \
            libcurl4-openssl-dev \
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

if ! command -v ffmpeg &> /dev/null; then
    install_ffmpeg
fi

install_ntgcalls
install_chrome
install_yt_dlp
install_speedtest
install_piper

echo "Successfully installed resources!"
exit 0
