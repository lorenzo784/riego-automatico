#!/bin/sh

celery -A core worker --loglevel=info --concurrency 1 -E --uid=nobody

