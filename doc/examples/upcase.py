#!/usr/bin/python

import sys
sys.dont_write_bytecode=True

def upcase(context, str):
    return str.upper()

extensions = {('http://example.org/e', 'upcase'): upcase}
