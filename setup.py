import homekeeper
import setuptools

setuptools.setup(
    author='Min Huang',
    author_email='min.huang@alumni.usc.edu',
    description='Homekeeper can version your dotfiles with Git.',
    long_description=open('README.txt').read(),
    name='homekeeper',
    packages=['homekeeper'],
    version=homekeeper.__version__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
    ],
    entry_points="""
        [console_scripts]
            homekeeper = homekeeper.cli:main
    """,
)
