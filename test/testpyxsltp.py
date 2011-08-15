#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, unittest
from StringIO import StringIO
from types import ModuleType

import pyxsltp


class PyXSLTPTestCase(unittest.TestCase):

    def setUp(self):
        self.copy_xsl  = StringIO(open('test/copy.xsl').read())
        self.min_xhtml = StringIO(open('test/min.xhtml').read())
        self.ext_xsl   = StringIO(open('test/ext.xsl').read())
        self.ext_py    = StringIO(open('test/ext.py').read())

    def test_apply(self):
        expected = '<?xml version="1.0"?>\n' \
            '<html xmlns="http://www.w3.org/1999/xhtml" ' \
            'xmlns:xlink="http://www.w3.org/1999/xlink"/>\n'
        expected_log = ''
        (actual_tree, actual_log) = pyxsltp.apply(
            self.copy_xsl, "dummy url",
            self.min_xhtml, "dummy url",
            stringparams={'name': 'value with spaces'}
            )
        self.assertEqual(expected,str(actual_tree))
        self.assertEqual(expected_log,str(actual_log))

    def test_apply_with_extensions(self):
        expected = '<?xml version="1.0"?>\n' \
            '<p>example-func: arg1: Lorem ipsum.</p>\n'
        extm = pyxsltp.load_module('dummy', self.ext_py)
        (actual_tree, actual_log) = pyxsltp.apply(
            self.ext_xsl, "dummy url",
            StringIO('<p>Lorem ipsum.</p>'), "dummy url",
            extensions=extm.extensions)
        self.assertEqual(expected, str(actual_tree))

    def test_load_module(self):
        expected = ModuleType('foo').__name__
        actual = pyxsltp.load_module('foo', StringIO()).__name__
        self.assertEqual(expected, actual)

    def test_merge_dicts(self):
        expected = {'a': 1, 'b': 5, 'c': 10}
        actual = pyxsltp.merge_dicts({'a': 1, 'b': 2}, {'b': 5, 'c': 10})
        self.assertEqual(expected, actual)

    def test_ensure_trailing_sep(self):
        expected = ['foo/', 'bar/']
        actual = map(pyxsltp.ensure_trailing_sep, ['foo', 'bar/'])
        self.assertEqual(expected, actual)

def main(argv):
    suite = unittest.makeSuite(PyXSLTPTestCase, 'test')
    unittest.TextTestRunner().run(suite)

if __name__ == "__main__":
    main(sys.argv)
