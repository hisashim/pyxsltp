#!/usr/bin/python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
setup(
    name = "pyxsltp",
    version = open('VERSION').read(),
    packages = find_packages(),
    scripts = ['pyxsltp'],
)
