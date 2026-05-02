#!/usr/bin/env bash
set -e

SHA=$1

cd /home/sabina/catty-reminders-app

git fetch origin

if [ -n "${SHA}" ]; then
    git checkout "${SHA}"
else
    git checkout lab2
    git pull origin lab2
fi

CURRENT_COMMIT=$(git rev-parse HEAD)

/home/sabina/catty-reminders-app/.venv/bin/pip install -r requirements.txt

echo "DEPLOY_REF=${CURRENT_COMMIT}" > .deploy_env

sudo systemctl restart catty-app.service
sleep 2

if systemctl is-active --quiet catty-app.service; then
    echo "Service restarted"
else
    echo "Service failed to restart"
    exit 1
fi

