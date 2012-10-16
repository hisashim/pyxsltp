#!/usr/bin/python
# -*- coding: utf-8 -*-

from distutils.core import setup
from pyxsltp import __version__

setup(
    name = "pyxsltp",
    version = __version__,
    py_modules = ['pyxsltp'],
    scripts = ['pyxsltp'],
)
