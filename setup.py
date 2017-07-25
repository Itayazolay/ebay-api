import re

from setuptools import setup, find_packages

requirements = open("requirements.txt").readlines()


def find_version():
    verfile = open('ebayapi/__init__.py', "r").read()
    version_re = r"^__version__ = ['\"]([^'\"]*)['\"]"

    mo = re.search(version_re, verfile, re.M)
    if mo:
        return mo.group(1)
    return "unknown"


setup(
    name='ebay-api',
    version=find_version(),
    packages=find_packages(exclude=("tests", "doc")),
    install_requires=requirements,
    url='https://github.com/Itayazolay/ebay-api',
    license='MIT',
    author='Itay Azolay',
    author_email='itayazolay@gmai.com',
    description='Make Ebay API great again.'
)
