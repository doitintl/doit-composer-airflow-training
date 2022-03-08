#!/bin/sh -e

# Wrap the `lintspaces` command to provide extended configuration
# =============================================================================

# Usage: ./bin/lintspaces.sh

# https://github.com/schorfES/node-lintspaces

run_lintspaces() {
    max_newlines="${1}"
    xargs -0 lintspaces \
        --maxnewlines "${max_newlines}" \
        --editorconfig .editorconfig \
        --guessindentation \
        --matchdotfiles \
        </dev/stdin
}

# Python files
./bin/find.sh -name '*.py' |
    run_lintspaces 2

# All other files
./bin/find.sh -not -name '*.py' |
    run_lintspaces 1