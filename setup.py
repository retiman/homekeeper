import homekeeper
import setuptools


setuptools.setup(
    author='Min Huang',
    author_email='min.huang@alumni.usc.edu',
    description='Symlinks your dotfiles from anywhere to your home directory.',
    install_requires=['click >= 7.1.2'],
    license='MIT',
    name='homekeeper',
    packages=['homekeeper'],
    platforms=['any'],
    url='https://github.com/retiman/homekeeper',
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
