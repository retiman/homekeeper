FLAKE8 = /usr/bin/env flake8
PIP = /usr/bin/env pip
PYDOC = /usr/bin/env pydoc
PYLINT = /usr/bin/env pylint
PYTEST = /usr/bin/env pytest
PYTHON = /usr/bin/env python
TWINE = /usr/bin/env twine
.PHONY = check clean deploy dist doc install lint test virtualenv

all: clean dist

check:
	${TWINE} check dist/*

clean:
	@echo 'Removing all directories except venv'
	rm -rf dist
	rm -rf homekeeper/.pytest_cache
	rm -rf homekeeper/homekeeper-testlogs.txt
	rm -rf homekeeper.egg-info/
	rm -rf homekeeper.html
	rm -rf homekeeper-testlogs.txt

deploy: clean dist
	${TWINE} upload --repository pypi dist/*

dist: lint test
	${PYTHON} setup.py sdist
	${TWINE} check dist/*

doc:
	${PYDOC} -w homekeeper

install: dist
	${PIP} install dist/*

lint:
	${PYLINT} --rcfile=pylintrc homekeeper setup.py
	${FLAKE8} --extend-ignore=E501 homekeeper setup.py

requirements:
	${PIP} install -r requirements.txt

test:
	${PYTEST} --verbose --color=auto homekeeper

virtualenv:
	${PYTHON} -m venv venv
	@echo 'Now source activate and pip install -r requirements.txt'
