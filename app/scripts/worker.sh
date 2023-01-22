#!/bin/bash -x

celery -A app worker --loglevel=debug --concurrency 1 -E
