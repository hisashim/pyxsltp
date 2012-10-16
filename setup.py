#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from pyxsltp import __version__

setup(
    name = "pyxsltp",
    version = __version__,
    packages = find_packages(),
    scripts = ['pyxsltp'],
)
