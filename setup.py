import os

from setuptools import setup

setup(
    author='Min Huang',
    author_email='min.huang@alumni.usc.edu',
    description='Homekeeper can version your dotfiles with Git.',
    long_description=open('README.txt').read(),
    name='homekeeper',
    package_dir={'': 'lib'},
    scripts=['bin/homekeeper'],
    test_suite='homekeeper_test',
    version='2.0.0',
    classifiers=[
      'Development Status :: 4 - Beta',
      'Topic :: Utilities',
    ],
)
