#!/usr/bin/env sh
NAME="celery"

source script/base.sh

FILE_TASK=app.utils.celery_worker.main

exec celery -A ${FILE_TASK} worker