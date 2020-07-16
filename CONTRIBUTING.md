Contributing
============
This is a guide for contributing.

Building
========
Use `tox` to build.  See `tox.ini` for minimum version.

1.  Invoke `tox` to run everything.
1.  Invoke `tox -e flake8,pylint,check` to only run lints.
1.  Invoke `tox -e py35` to only run tests.

Testing
=======
You may install the package locally for testing.

1.  Invoke `source .tox/py35/bin/activate` to activate your virtual environment.
1.  Invoke `tox --sdistonly` to build the package.
1.  Invoke `pip install .tox/dist/*` to install the package locally.
1.  Test as necessary.

Releases
========
The master branch and feature branches should be used for general development.   The release branch should be used for
releases; only tag the release branch when ready to release.

The process for releasing is:
1.  Update the `homekeeper.__version__` variable with the new version.
1.  Update the `CHANGELOG.txt` with new version information.
1.  Invoke `tox` to run the tests and lint.
1.  Invoke `tox -e check` to check the package with twine.
1.  Invoke `git merge master` on the `release` branch to merge changes from `master`.
1.  Invoke `git tag -a vx.y.z -m "New release"` to tag the release.
1.  Invoke `git push origin release` to push the changes.
1.  Invoke `git push --tags origin` to push the tags.
1.  Invoke `tox -e publish` to publish to PyPI.