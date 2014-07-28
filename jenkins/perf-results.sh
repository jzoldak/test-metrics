#!/usr/bin/env bash

PYTHONPATH=.; python -m metrics.perf_stats "$@"
