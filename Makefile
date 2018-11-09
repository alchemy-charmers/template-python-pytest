ifndef JUJU_REPOSITORY
	JUJU_REPOSITORY := $(shell pwd)
	$(warning Warning JUJU_REPOSITORY was not set, defaulting to $(JUJU_REPOSITORY))
endif

help:
	@echo "This project supports the following targets"
	@echo ""
	@echo " make help - show this text"
	@echo " make submodules - make sure that the submodules are up-to-date"
	@echo " make lint - use pre-commit to ensure consistent layout"
	@echo " make test - run the functional test, unittests and lint"
	@echo " make unittest - run the tests defined in the unittest "\
		"subdirectory"
	@echo " make functionaltest - run the tests defined in the "\
		"functional subdirectory"
	@echo " make release - build the charm using the virtualenv"
	@echo " make clean - remove unneeded files"
	@echo ""
	@echo " the following targets are meant to be used by the Makefile"
	@echo " make requirements - installs the requirements"
	@echo " make setup - install the pre-commit hook"
	@echo " make virtualenv - check that a virtualenv is active"

submodules:
	@echo "Cloning submodules"
	@git submodule update --init --recursive

lint:
	@-if [ -x `which pre-commit` ] ; then echo "Running pre-commit as linter";	pre-commit run --all || exit 0 ; fi
	@echo "Running flake8"
	@flake8 ./src

test: unittest functionaltest lint

unittest:
	@cd src && tox -e unit

functionaltest:
	@cd src && tox -e functional

build:
	@echo "Building charm to base directory $(JUJU_REPOSITORY)"
	@git describe --tags > ./src/repo-info
	@LAYER_PATH=./layers INTERFACE_PATH=./interfaces\
		JUJU_REPOSITORY=$(JUJU_REPOSITORY) charm build ./src --force

release: lint clean build
	# Maybe add the command to push the build bundle to the store?
	#
	@echo "Charm is build, it can now be pushed to the store"
	@echo "With the command:"
	@echo " charm push ./src"

clean:
	@echo "Cleaning files"
	@if [ -d src/.tox ] ; then rm -r src/slave/.tox ; fi
	@if [ -d src/.pytest_cache ] ; then rm -r src/slave/.pytest_cache ; fi

# The targets below don't depend on a file
.PHONY: lint test unittest functionaltest build release clean help \
	submodules
