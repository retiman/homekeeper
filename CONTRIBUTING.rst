============
Contributing
============
This is a guide for contributing.

========
Building
========
Use ``tox`` to build.  See ``tox.ini`` for minimum version.

#.  Invoke ``tox`` to run everything.
#.  Invoke ``tox -e flake8,pylint,check`` to only run lints.
#.  Invoke ``tox -e py35`` to only run tests.

=======
Testing
=======
You may install the package locally for testing.

#.  Invoke ``source .tox/py35/bin/activate`` to activate your virtual environment.
#.  Invoke ``tox --sdistonly`` to build the package.
#.  Invoke ``pip install .tox/dist/*`` to install the package locally.
#.  Test as necessary.

========
Releases
========
The master branch and feature branches should be used for general development.   The release branch should be used for
releases; only tag the release branch when ready to release.

The process for releasing is:

#.  Update the ``homekeeper.__version__`` variable with the new version.
#.  Update the ``CHANGELOG.txt`` with new version information.
#.  Invoke ``tox`` to run the tests and lint.
#.  Invoke ``tox -e check`` to check the package with twine.
#.  Invoke ``git merge master`` on the ``release`` branch to merge changes from ``master``.
#.  Invoke ``git tag -a vx.y.z -m "New release"`` to tag the release.
#.  Invoke ``git push origin release`` to push the changes.
#.  Invoke ``git push --tags origin`` to push the tags.
#.  Invoke ``tox -e publish`` to publish to PyPI.