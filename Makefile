.DEFAULT_GOAL := help

.venv:
	# creating virtual environment
	@python3 -m venv $@
	# updating package managers
	@$@/bin/pip --no-cache install --upgrade \
		pip \
		setuptools \
		wheel
	@$@/bin/pip --no-cache install -r requirements.txt
	
PYINC := $(shell python3-config --includes)
.PHONY: build
build: ## builds the c++ example extension
	g++ -fpic --shared $(PYINC) hello.cpp -o hello.so


# MISC ---------------------------------------------------------------

.PHONY: help
help: ## help on rule's targets
	@awk --posix 'BEGIN {FS = ":.*?## "} /^[[:alpha:][:space:]_-]+:.*?## / {printf "\033[36m%-25s\033[0m %s\n", $$1, $$2}' $(MAKEFILE_LIST)
