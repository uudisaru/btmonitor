#!/usr/bin/env bash

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"
cd $ROOT/btmonitor-ui

yarn
yarn build
cp -r ./build $ROOT/frontend

