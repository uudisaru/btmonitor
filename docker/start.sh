#!/usr/bin/env bash

if [[ ! -f "./servername.txt" ]]; then
    echo "Name of the server must be defined in file servername.txt!"
    exit 1
else
    server=$(cat "./servername.txt")
    verification_key=$(cat "./servername.txt")
fi

if [[ ! -f "./btmonitor.pub" ]]; then
    echo "API access verification public key must be defined in file btmonitor.pub!"
    exit 1
else
    server=$(cat "./servername.txt")
    verification_key=$(cat "./btmonitor.pub")
fi

docker run -d -p 443:443 \
    -v "$(pwd)/letsencrypt/etc:/etc/letsencrypt" \
    -e "server=${server}" \
    -e "SANIC_PUBLIC_KEY=\"${verification_key}\"" \
    --restart unless-stopped \
    btmonitor/btmonitor:v1
