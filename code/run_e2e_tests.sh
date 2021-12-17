#!/usr/bin/env bash

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"

find . -name '*.pyc' -delete

PYTHONPATH=${DIR}/plugins python -m pytest -s "$DIR/e2e_tests"