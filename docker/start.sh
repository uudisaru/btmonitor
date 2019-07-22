#!/usr/bin/env bash

if [[ ! -f "./servername.txt" ]]; then
    echo "Name of the server must be defined in file servername.txt!"
    exit 1
else
    server=$(cat "./servername.txt")
fi

docker run -d -p 443:443 \
    -v "$(pwd)/letsencrypt/etc:/etc/letsencrypt" \
    -e "server=${server}" \
    --restart unless-stopped \
    btmonitor/btmonitor:v1
