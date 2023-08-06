#!/bin/bash

source .env

expect << EOF
spawn python3 -m
expect "Please enter your phone (or bot token): "
send -- "$BOT_TOKEN\r"
expect eof
EOF
cd ../