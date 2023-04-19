from setuptools import setup, find_packages
import codecs
import os

here = os.path.abspath(os.path.dirname(__file__))

with codecs.open(os.path.join(here, "PYPIREADME.md"), encoding="utf-8") as fh:
    long_description = "\n" + fh.read()

VERSION = '1.1'
DESCRIPTION = 'A python based tool for finding subdomains of a domain.'

# Setting up
setup(
    name='subdomainfinder',
    version=VERSION,
    author='Ankush Bhagat',
    author_email="<ankushbhagatofficial@gmail.com>",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=long_description,
    url='https://github.com/ankushbhagatofficial/subdomain-finder',
    packages=find_packages(),
    py_modules=['subfinder'],
    install_requires=[
        'requests',
        'rich'
    ],
    keywords=['python', 'SecurityTrails', 'API', 'findsubdomain'],
    entry_points={
        'console_scripts': ['subdomainfinder=subdomainfinder.__main__:main'],
    },
    classifiers=[
        "Development Status :: 1 - Planning",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
