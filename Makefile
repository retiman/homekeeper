PYDOC = /usr/bin/env pydoc
PYLINT = /usr/bin/env pylint
PYTEST = /usr/bin/env pytest
PYTHON = /usr/bin/env python2
PIP = /usr/bin/env pip2
.PHONY = clean deploy doc doc-server install requirements test

all: clean requirements doc test

clean:
	rm -rf build
	rm -rf dist
	rm -rf homekeeper/*.pyc
	rm -rf homekeeper/__pycache__
	rm -rf htmlcov
	rm -rf .cache
	rm -rf .coverage
	rm -rf tests.xml

deploy: clean doc lint test
	${PYTHON} setup.py sdist upload -r homekeeper

debug:
	${PYTEST} --pdb homekeeper

doc:
	${PYDOC} -w homekeeper

doc-server:
	${PYDOC} -p 8080 -w homekeeper

install: clean requirements
	${PIP} install --upgrade .

lint:
	${PYLINT} --rcfile=pylintrc homekeeper

requirements:
	${PIP} install -r requirements.txt

test: lint
	${PYTEST} -v --tb=long --full-trace --junit-xml=tests.xml \
			--cov=homekeeper --cov-report=html homekeeper
