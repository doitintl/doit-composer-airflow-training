#!/bin/sh -e

# Bootstrap the devcontainer for use with mdBook
# =============================================================================

# Usage: ./.devcontainer/bootstrap.sh

RUST_URL='https://sh.rustup.rs'
MDBOOK_URL='https://github.com/rust-lang/mdBook.git'

CARGO_ENV="${HOME}/.cargo/env"

# Install rust
if ! command -v cargo >/dev/null; then
    # https://doc.rust-lang.org/book/ch01-01-installation.html
    curl --proto '=https' --tlsv1.2 "${RUST_URL}" -sSf | sh
fi

# Source the Cargo environment file
if test -f "${CARGO_ENV}"; then
    # shellcheck disable=SC1090
    . "${CARGO_ENV}"
fi

# Install mdBook
if ! command -v mdbook >/dev/null; then
    # https://rust-lang.github.io/mdBook/guide/installation.html
    cargo install --git "${MDBOOK_URL}" mdbook
fi

echo 'Bootstrapped successfully!'
