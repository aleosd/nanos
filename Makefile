default: help

SRC_DIR := ./nanos
DOCS_DIR := ./docs
TESTS_DIR := ./tests
DOCS_SRC := $(DOCS_DIR)/source
DOCS_BUILD := $(DOCS_DIR)/build

ALL_CODE := $(SRC_DIR) $(TESTS_DIR) $(DOCS_SRC)/conf.py

.PHONY: fmt
fmt:  # sort imports and format the projects' source
	ruff check --select I --fix $(ALL_CODE)
	ruff format $(ALL_CODE)

.PHONY: verify
verify:  # lint (check) the project
	ruff format --check $(ALL_CODE)
	ruff check $(SRC_DIR)
	mypy ./nanos --strict

.PHONY: test
test: # run tests with pytest
	coverage run -m pytest $(TESTS_DIR) --showlocals -s
	coverage report -m

.PHONY: build-docs
build-docs: # build the documentation using sphinx
	@rm -rf $(DOCS_BUILD)
	sphinx-apidoc -f -o $(DOCS_SRC)/generated $(SRC_DIR) --separate --no-toc \
		--remove-old --force --templatedir $(DOCS_SRC)/templates
	sphinx-build -M html $(DOCS_SRC) $(DOCS_BUILD)

.PHONY: help
help: # Show help for each of the Makefile recipes.
	@grep -E '^[a-zA-Z0-9 -]+:.*#'  Makefile | sort | while read -r l; do printf "\033[1;32m$$(echo $$l | cut -f 1 -d':')\033[00m:$$(echo $$l | cut -f 2- -d'#')\n"; done
