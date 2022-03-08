# =============================================================================
# Build and lint the project
# =============================================================================

.EXPORT_ALL_VARIABLES:

# POSIX locale
LC_ALL = C

# ANSI formatting
BOLD = [1m
RESET = [0m

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
