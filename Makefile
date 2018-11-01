REQUIREMENTS_FILE=requirements.txt
REQUIREMENTS_OUT=requirements.txt.log

help:
	@echo "This project supports the following targets"
	@echo ""
	@echo " make help - show this text"
	@echo " make all  - ensure that we are in a virtualenv "\
		"and that our requirements"
	@echo "             are installed and install the pre-commit hook"
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


all: setup requirements

lint: virtualenv requirements
	@${VIRTUAL_ENV}/bin/pre-commit run --all

test: unittest functionaltest lint

unittest: virtualenv requirements
	@cd src && ${VIRTUAL_ENV}/bin/tox -e unit

functionaltest: virtualenv requirements
	@cd src && ${VIRTUAL_ENV}/bin/tox -e functional

build:
	@git describe --tags > ./src/repo-info
	@LAYER_PATH=./layers INTERFACE_PATH=./interfaces\
		charm build ./src --force

release: virtualenv lint clean build
	# Maybe add the command to push the build bundle to the store?
	#
	@echo "Charm is build, it can now be pushed to the store"
	@echo "With the command:"
	@echo " charm push ./src"

clean:
	@echo "Cleaning files"
	@rm -r src/.tox

requirements: $(REQUIREMENTS_OUT)

$(REQUIREMENTS_OUT): $(REQUIREMENTS_FILE)
	pip install -r $(REQUIREMENTS_FILE) | tee $(REQUIREMENTS_OUT)

setup: virtualenv
	@${VIRTUAL_ENV}/bin/pre-commit install

# This target is quite important. Using a virtualenv allows python packages to
# be installed separate from the system packages. So installing all packages
# in an virtualenv, ensures that e.g. the editor can use this virtualenv for
# completion tasks.
# It also allows to install specific versions of packages e.d. xenial released
# python packages, while running bionic or comic.
virtualenv:
ifndef VIRTUAL_ENV
	$(error No VIRTUAL_ENV defined)
endif

# The targets below don't depend on a file
.PHONY: all lint test unittest functionaltest build release clean setup virtualenv help
