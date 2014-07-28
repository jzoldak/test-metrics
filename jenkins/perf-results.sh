#!/usr/bin/env bash

# virtualenv venv
# source ./venv/bin/activate
# pip install -r requirements.txt

python -m metrics.perf_stats "$@"
