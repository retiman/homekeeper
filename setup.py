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
    version=homekeeper.__version__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
    ],
)
