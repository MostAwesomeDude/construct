#!/usr/bin/env python

from setuptools import find_packages, setup

setup(
    name="construct",
    version="2.04",
    packages=find_packages(),
    license="Public Domain",
    description="a powerful declarative parser for binary data",
    long_description=open("README.rst").read(),
    url="https://github.com/MostAwesomeDude/construct",
    author="Tomer Filiba",
    author_email="tomerfiliba at gmail dot com",
    maintainer="Corbin Simpson",
    maintainer_email="MostAwesomeDude@gmail.com",
)
