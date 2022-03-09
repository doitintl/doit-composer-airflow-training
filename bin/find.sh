#!/bin/sh -e

# Print a list of all versionable text files
# =============================================================================

# Usage: ./bin/find.sh [FIND_OPTIONS...]

# POSIX locale
LC_ALL=C
export LC_ALL

find . -type f \
    -not -path './.docops/lock/*' \
    -not -path './.git/*' \
    -not -exec git check-ignore --quiet {} \; \
    -exec grep -qI . {} \; \
    "${@}" \
    -print0 | sort -zn
