#!/bin/sh -e

DIR="$(cd "$(dirname "${0}")" >/dev/null 2>&1 && pwd)"

find . -name '*.pyc' -delete

PYTHONPATH=${DIR}/plugins python -m pytest -s "${DIR}/tests"
