#!/usr/bin/env sh
NAME="api"

source script/base.sh

# Start your Django Unicorn
exec uvicorn ${ASGI_MODULE}:app \
  --host 0.0.0.0 \
  --port 8000 \
  --log-level=debug