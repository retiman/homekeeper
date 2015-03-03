PYTHON = /usr/bin/env/python2
PIP = /usr/bin/env pip2
.PHONY = clean deploy install lint requirements test

all: clean requirements doc test

clean:
	rm -rf *.egg-info
	rm -rf build
	rm -rf dist
	rm -rf homekeeper/*.pyc
	rm -rf lib

deploy: clean doc test
	${PYTHON} setup.py sdist upload -r homekeeper

doc:
	pydoc -w homekeeper

doc-server:
	pydoc -p 8080 -w homekeeper

install: clean requirements
	${PIP} install --upgrade .

lint:
	pylint -rn bin/homekeeper
	pylint -rn homekeeper

requirements:
	${PIP} install -r requirements.txt

test: lint
	nosetests
