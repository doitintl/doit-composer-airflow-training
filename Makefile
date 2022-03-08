# =============================================================================
# Build and lint the project
# =============================================================================

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL = C

# ANSI formatting
BOLD = [1m
RESET = [0m

BIN_DIR = ./bin

# $(call print-target)
define print-target
@ printf "\e$(BOLD)make %s\e$(RESET)\n" "$$(echo $@ | sed 's,.stamp,,')"
endef

# Help
# =============================================================================

.DEFAULT_GOAL = help

define print-target-list
@ grep -E '^.PHONY:' $(MAKEFILE_LIST) | grep "#" | \
	sed -E "s,[^:]+: ([a-z-]+) # (.*),  \x1b$(BOLD)make \1\x1b$(RESET)#\2," | \
	column -t -s '#'
endef

.PHONY: help # Print this help message and exit
help:
	@ echo "Usage:"
	@ echo
	$(call print-target-list)

# Wrappers for mdBook
# =============================================================================

# build
# -----------------------------------------------------------------------------

.PHONY: build # Builds the book from its Markdown files
build:
	$(call print-target)
	mdbook build

# clean
# -----------------------------------------------------------------------------

.PHONY: clean # Deletes any temporary build files
clean:
	$(call print-target)
	mdbook clean
	rm -f index.html
	rm -rf .venv

# serve
# -----------------------------------------------------------------------------

# By default, `mdbook serve` resolves `localhost` to the IPv6 address `[::1]`,
# which VS Code doesn't understand.
#
# When we specify the IPv4 address `127.0.0.1`, VS Code recognizes the open
# port and allows the user to preview the book (in VS Code itself or in an
# external browser).

.PHONY: serve # Serves the book at http://localhost:3000/ with live reload
serve:
	$(call print-target)
	mdbook serve -n 127.0.0.1 -p 3000

# test
# -----------------------------------------------------------------------------

.PHONY: test # Tests that the book's Rust code samples compile
test:
	$(call print-target)
	mdbook test

# watch
# -----------------------------------------------------------------------------

.PHONY: watch # Watches the book's files and rebuilds it on changes
watch:
	$(call print-target)
	mdbook watch

# Linting
# =============================================================================

.PHONY: lint # Run a suite of lint checks
lint:

# ec
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/editorconfig-checker/editorconfig-checker

EC = ec

lint: ec
.PHONY: ec
ec:
	$(call print-target)
	$(EC)

# lintspaces
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

LINTSPACES := $(BIN_DIR)/lintspaces.sh

lint: lintspaces
.PHONY: lintspaces
lintspaces:
	$(call print-target)
	$(LINTSPACES)

# prettier
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/prettier/prettier

PRETTIER = prettier --check --ignore-unknown .

lint: prettier
.PHONY: prettier
prettier:
	$(call print-target)
	$(PRETTIER)

# black
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/psf/black

BLACK = black --check .

lint: black
.PHONY: black
black:
	$(call print-target)
	$(BLACK)

# yamllint
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/adrienverge/yamllint

YAMLLINT = yamllint --config-file .yamllint.yaml .

lint: yamllint
.PHONY: yamllint
yamllint:
	$(call print-target)
	$(YAMLLINT)

# shellcheck
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

SHELLCHECK := $(BIN_DIR)/find.sh -name '*.sh' | xargs -0 shellcheck

lint: shellcheck
.PHONY: shellcheck
shellcheck:
	$(call print-target)
	$(SHELLCHECK)

# shfmt
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# https://github.com/mvdan/sh

SHFMT = shfmt -d -p -i 4 .

lint: shfmt
.PHONY: shfmt
shfmt:
	$(call print-target)
	$(SHFMT)

# markdownlint
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

MARKDOWNLINT = markdownlint .

lint: markdownlint
.PHONY: markdownlint
markdownlint:
	$(call print-target)
	$(MARKDOWNLINT)

# cspell
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

CSPELL := $(BIN_DIR)/find.sh | xargs -0 \
	cspell --no-progress --no-summary --config .cspell.json

lint: cspell
.PHONY: cspell
cspell:
	$(call print-target)
	$(CSPELL)

# misspell
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

MISSPELL := $(BIN_DIR)/misspell.sh

lint: misspell
.PHONY: misspell
misspell:
	$(call print-target)
	$(MISSPELL)
