from setuptools import setup

setup(
    author='Min Huang',
    author_email='min.huang@alumni.usc.edu',
    description='Homekeeper can version your dotfiles with Git.',
    long_description=open('README.txt').read(),
    name='homekeeper',
    package_dir={'': 'lib'},
    py_modules=['homekeeper'],
    scripts=['bin/homekeeper'],
    test_suite='homekeeper_test',
    version='2.1.7',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
    ],
)
