import setuptools
import homekeeper


with open('README.rst', encoding='utf-8') as f:
    long_description = f.read()


setuptools.setup(
    author='Min Huang',
    author_email='min.huang@alumni.usc.edu',
    description='Symlinks your dotfiles from anywhere to your home directory.',
    install_requires=['click >= 7.1.2'],
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    name='homekeeper',
    packages=['homekeeper'],
    platforms=['any'],
    url='https://github.com/retiman/homekeeper',
    version=homekeeper.__version__,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Topic :: Utilities',
    ],
    entry_points="""
        [console_scripts]
            homekeeper = homekeeper.cli:main
    """,
)
