import homekeeper
import setuptools


setuptools.setup(
    name='homekeeper',
    version=homekeeper.__version__,
    license='MIT',
    author='Min Huang',
    author_email='min.huang@alumni.usc.edu',
    url='https://github.com/retiman/homekeeper',
    description='Symlinks your dotfiles from anywhere to your home directory.',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    packages=['homekeeper'],
    install_requires=['click >= 7.1.2'],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Utilities',
    ],
    entry_points="""
        [console_scripts]
            homekeeper = homekeeper.cli:main
    """,
)
