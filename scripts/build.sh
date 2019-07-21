#!/usr/bin/env bash

ROOT="$( cd "$( dirname "${BASH_SOURCE[0]}" )/.." >/dev/null 2>&1 && pwd )"

rm -rf $ROOT/frontend

cd $ROOT/btmonitor-ui

if [[ ! -d ".git" ]]; then
    git submodule init
    git submodule update
fi

${ROOT}/scripts/build_ui.sh
