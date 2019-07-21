#!/usr/bin/env bash

set -e

# Init API key
if [[ ! -f "./btmonitor.pub" ]]; then
    echo -n "Password for API access key:"
    read -s password
    openssl genrsa -aes256 -out btmonitor.key -passout pass:$password
    openssl rsa -in btmonitor.key -outform PEM -pubout -out btmonitor.pub -passin pass:$password
fi

# Build frontend
if [[ ! -d "../frontend" ]]; then
    cd ../btmonitor-ui

    if [[ ! -d ".git" ]]; then
        git submodule init
        git submodule update
    fi

    cd ..
    mkdir frontend

    docker build -t btmonitor/frontbuild:v1 -f docker/Dockerfile.node .
    docker run -it --rm \
        -v "$(pwd)/frontend:/usr/src/app/frontend" \
        btmonitor/frontbuild:v1
    cd docker
fi

# Fetch letsencrypt certificate
echo -n "Host for the certificate:"
read host

if [[ ! -d "./letsencrypt" ]]; then
    mkdir -p ./letsencrypt/etc
    mkdir -p ./letsencrypt/lib

    docker run -it --rm --name certbot \
        -v "letsencrypt/etc:/etc/letsencrypt" \
        -v "letsencrypt/lib:/var/lib/letsencrypt" \
        certbot/certbot \
        certonly --manual --preferred-challenges dns-01 --agree-tos -d "${host}" \
        --server https://acme-v02.api.letsencrypt.org/directory
fi

export SANIC_PUBLIC_KEY=$(<btmonitor.pub)
# docker build --build-arg host=${host} -t btmonitor/btmonitor:v1 -f Dockerfile ..
