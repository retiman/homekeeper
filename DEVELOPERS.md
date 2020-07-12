Developers
==========
This is a guide for developers.

Building
========
Developers need to set up their own virtual environment first.  Currently only Python 3.5 is supported.
1.  Run `make virtualenv` or something equivalent to set up your virtual environment.
1.  Run `make requirements` or `pip install -r requirements.txt` to install required packages.

Only afterwards should you run `make dist` to build the package or `make test` to only run the tests.

Releases
========
The master branch and feature branches should be used for general development.   The release branch should be used for
releases; only tag the release branch when ready to release.

The process for releasing is:
1.  Ensure the package can be built and all tests pass using `make clean dist`.
1.  Do any local testing via `make install`.
1.  Update the `CHANGELOG.txt`.
1.  Merge changes from `master` onto `release`.
1.  Create an annotated tag via `git tag -a vx.y.z -m "New release"`.
1.  Push the branch and tags `git push origin release` and `git push --tags origin`.
