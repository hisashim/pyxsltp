#!/usr/bin/python

def upcase(context, str):
    return str.upper()

extensions = {('http://example.org/e', 'upcase'): upcase}
