#!/bin/sh -e

# Wrap the `optipng` command to provide a `--dry-run` option
# =============================================================================

# Usage: ./bin/optipng.sh [-d|--dry-run] DOCS_DIR ASSETS_DIR

# POSIX locale
LC_ALL=C
export LC_ALL

# ANSI formatting
RED='\x1b[31m'
RESET='\x1b[0m'

OPTIPNG_LOCK_DIR=.docops/lock/optipng

dry_run=0
for arg in "$@"; do
    case "${arg}" in
    -d | --dry-run)
        dry_run=1
        shift
        ;;
    -*)
        echo "ERROR: Unknown option: ${arg}"
        exit 1
        ;;
    *) ;;
    esac
done

mkdir -p "${OPTIPNG_LOCK_DIR}"
tmp_errors="$(mktemp)"
find . -type f -name '*.png' | while read -r file; do
    sig_file="${OPTIPNG_LOCK_DIR}/${file}.md5sum"
    sig_dir="$(dirname "${sig_file}")"
    mkdir -p "${sig_dir}"
    if md5sum --check --quiet "${sig_file}" 2>/dev/null; then
        continue
    fi
    if test "${dry_run}" = 0; then
        echo "Compressing: ${file}"
        optipng -quiet -strip all "${file}"
        md5sum "${file}" >"${sig_file}"
    else
        echo "${file}" >>"${tmp_errors}"
    fi
done

# Clean the cache
tmp_file="$(mktemp)"
(
    cd "${OPTIPNG_LOCK_DIR}"
    find . -type f | sed 's,\.md5sum$,,' >"${tmp_file}"
)
while read -r file; do
    if test ! -f "${file}"; then
        rm -v "${file}"
    fi
done <"${tmp_file}"
rm -f "${tmp_file}"

find "${OPTIPNG_LOCK_DIR}" -type d -empty -delete

status_code=0
if test -s "${tmp_errors}"; then
    printf 'Missing or out-of-date optipng lock file:\n\n'
    sed -E "s,^(.*),  ${RED}\1${RESET}," <"${tmp_errors}"
    status_code=1
fi
rm -f "${tmp_errors}"
exit "${status_code}"
