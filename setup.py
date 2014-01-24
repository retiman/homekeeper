import homekeeper
import setuptools

setuptools.setup(
    author='Min Huang',
    author_email='min.huang@alumni.usc.edu',
    description='Homekeeper can version your dotfiles with Git.',
    long_description=open('README.txt').read(),
    name='homekeeper',
    packages=['homekeeper'],
    scripts=['bin/homekeeper'],
    test_suite='homekeeper.test',
    version=homekeeper.version,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Topic :: Utilities',
    ],
)
