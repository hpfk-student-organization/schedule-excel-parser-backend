#!/usr/bin/env sh

DIR=/app

ASGI_MODULE=app.main

echo "Starting $NAME as $(whoami)"

# Activate the virtual environment
cd $DIR

export PYTHONPATH=$DIR:$PYTHONPATH