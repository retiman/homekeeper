import homekeeper
import setuptools


setuptools.setup(
    author='Min Huang',
    author_email='min.huang@alumni.usc.edu',
    description='Symlinks your dotfiles from anywhere to your home directory.',
    long_description_type='text/markdown',
    long_description=open('README.txt', encoding='utf-8').read(),
    name='homekeeper',
    packages=['homekeeper'],
    install_requires=['click >= 7.1.2'],
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
