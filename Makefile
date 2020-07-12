PIP = /usr/bin/env pip
PYDOC = /usr/bin/env pydoc
PYLINT = /usr/bin/env pylint
PYTEST = /usr/bin/env pytest
PYTHON = /usr/bin/env python
TWINE = /usr/bin/env twine
.PHONY = clean deploy dist doc install lint test virtualenv

all: clean dist

clean:
	@echo 'Removing all directories except venv'
	rm -rf dist
	rm -rf homekeeper/.pytest_cache
	rm -rf homekeeper/homekeeper-testlogs.txt
	rm -rf homekeeper.egg-info/
	rm -rf homekeeper.html
	rm -rf homekeeper-testlogs.txt

deploy: dist
	${TWINE} upload --repository pypi dist/*

dist: lint test
	${PYTHON} setup.py sdist

doc:
	${PYDOC} -w homekeeper

install: dist
	${PIP} install dist/*

lint:
	${PYLINT} --rcfile=pylintrc homekeeper

requirements:
	${PIP} install -r requirements.txt

test: lint
	${PYTEST} --verbose --color=auto homekeeper

virtualenv:
	${PYTHON} -m venv venv
	@echo 'Now source activate and pip install -r requirements.txt'
