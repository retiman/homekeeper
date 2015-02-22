PYTHON = /usr/bin/env/python2
PIP = /usr/bin/env pip2
.PHONY = clean deploy install lint requirements test

all: requirements test

clean:
	rm -rf build
	rm -rf dist
	rm -rf *.egg-info
	rm -rf lib

deploy: clean test
	${PYTHON} setup.py sdist upload -r homekeeper

install: clean requirements
	${PIP} install --upgrade .

lint:
	pylint -rn bin/homekeeper
	pylint -rn homekeeper

requirements:
	${PIP} install -r requirements.txt

test: lint
	nosetests
