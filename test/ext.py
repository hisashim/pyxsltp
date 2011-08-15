#!/usr/bin/python

def example_func(context, arg1, arg2 = None):
    return 'example-func: arg1: %s' % (arg1,)

extensions = {('http://example.org/e', 'example-func'): example_func}
