#!/bin/bash

python3 -m bot
source .env

expect << EOF
spawn python3 main.py
expect "Please enter your phone (or bot token): "
send -- "$BOT_TOKEN\r"
expect eof
EOF
cd ../