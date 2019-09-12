#!/bin/sh

help () {
    echo "Usage: $0 <target_environment>"
}

if [ -z "$1" ] || [ "$1" = "-h" ] || [ "$1" = "--help" ]; then
    help
    exit 1
fi

cmd () {
    echo --- "$@"
    "$@"
}

target_env="$1"

set -e

if ! [ -d "${HOME}/node_modules" ]; then
    cmd rm -rf "${HOME}/node_modules" || true
    cmd mkdir -p "${HOME}/node_modules"
fi

cmd rm -rf ./node_modules || true
cmd ln -s "${HOME}/node_modules" .

cmd yarn install --non-interactive --frozen-lockfile
cmd npm install
cmd ./node_modules/.bin/ember build --environment "${target_env}" --output-path dist

echo Done.
