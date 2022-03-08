#!/bin/sh -e

# Wrap the `misspell` command to ignore paths
# =============================================================================

# https://github.com/client9/misspell

# POSIX locale
LC_ALL=C
export LC_ALL

# ANSI formatting
BLUE='\x1b[34m'
RED='\x1b[31m'
RESET='\x1b[0m'

tmp_errors="$(mktemp)"
misspell -locale US . |
    grep -vE '[^:]+\.css:' |
    grep -vE '[^:]+\.js:' |
    grep -vE '[^:]+\.svg:' \
        >"${tmp_errors}" || true

if test -s "${tmp_errors}"; then
    sed -E "s,^(.*): (.*),  ${BLUE}\1:${RESET} ${RED}\2${RESET}," \
        <"${tmp_errors}"
    rm -f "${tmp_errors}"
    exit 1
fi
