from setuptools import setup, find_packages

setup(
    name='ebay-api',
    version='0.1',
    packages=find_packages(exclude=("tests", "doc")),
    url='https://github.com/Itayazolay/ebay-api',
    license='',
    author='Itay Azolay',
    author_email='itayazolay@gmai.com',
    description='Make Ebay API great again. '
)
