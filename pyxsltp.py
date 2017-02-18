#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys, os, logging
sys.dont_write_bytecode=True
import types
import optparse

import lxml.etree


# meta

__version__ = '0.2.0'

# lib

def apply(xsl_io, xsl_base_uri, doc_io, doc_base_uri,
          stringparams={}, extensions={}, loglevel='WARNING'):
    logging.basicConfig(level=logging.__dict__[loglevel])
    logging.info('Apply style')

    xslt = lxml.etree.parse(xsl_io, base_url=xsl_base_uri)
    transform  = lxml.etree.XSLT(xslt, extensions=extensions)
    doc_parser = lxml.etree.XMLParser(load_dtd=True)
    doc        = lxml.etree.parse(doc_io, parser=doc_parser,
                                  base_url=doc_base_uri)
    def strparam_values(d):
        return dict([(t[0],lxml.etree.XSLT.strparam(t[1])) for t in list(d.items())])

    result_tree = transform(doc, **strparam_values(stringparams))
    xslt_log = transform.error_log
    return (result_tree, xslt_log)

# util

def load_module(modname, io):
    extm = types.ModuleType(modname)
    exec(io.read(), extm.__dict__)
    return extm

def merge_dicts(dict_a, dict_b):
    merged = dict_a.copy()
    for key, val in list(dict_b.items()):
        if val: merged[key] = val
    return merged

def ensure_trailing_sep(path, sep=os.path.sep):
    if path.endswith(sep): return path
    else:                  return path + sep

# ui

APP_NAME    = 'PyXSLTP'
APP_VERSION = __version__
APP_USAGE   = "Usage: %prog [options] stylesheet document\n" \
              "       ... | %prog --base-uri=URI [options] stylesheet -"
DEFAULT_CONF = {'base_uri':     None,
                'verbosity':    'WARNING',
                'ext_scripts':  [],
                'stringparams': {}}

def version_string():
    return "%(app)s %(appv)s\n" \
        "lxml %(lxmlv)s\n" \
        "libxml %(libxmlv)s (compiled %(libxmlcv)s)\n" \
        "libxslt %(libxsltv)s (compiled %(libxsltcv)s)" % \
        {'app': APP_NAME, 'appv': APP_VERSION,
         'lxmlv':     '.'.join(map(str, lxml.etree.LXML_VERSION)),
         'libxmlv':   '.'.join(map(str, lxml.etree.LIBXML_VERSION)),
         'libxmlcv':  '.'.join(map(str, lxml.etree.LIBXML_COMPILED_VERSION)),
         'libxsltv':  '.'.join(map(str, lxml.etree.LIBXSLT_VERSION)),
         'libxsltcv': '.'.join(map(str, lxml.etree.LIBXSLT_COMPILED_VERSION))}

def opts_and_args():
    op = optparse.OptionParser(usage  =APP_USAGE,
                               version=version_string())
    op.add_option("--base-uri",
                  dest = "base_uri",
                  help = "specify document base URI")
    op.add_option("--verbosity",
                  dest = "verbosity",
                  choices = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'],
                  default = 'WARNING',
                  help = "set log level (default: %default)")
    op.add_option("--extension",
                  action='append',
                  dest = "ext_scripts",
                  metavar='EXTENSION',
                  help = "specify extension script(s)")
    op.add_option("--stringparam",
                  action='append',
                  dest = "stringparams",
                  nargs=2,
                  metavar='NAME VALUE',
                  help = "specify stylesheet parameter(s)")
    return op.parse_args()

def runtime_conf(opts, default_conf):
    clc = cmdline_conf = {}
    if opts.base_uri:          clc['base_uri']     = opts.base_uri
    if opts.verbosity:         clc['verbosity']    = opts.verbosity
    if opts.ext_scripts != []: clc['ext_scripts']  = opts.ext_scripts
    if opts.stringparams:      clc['stringparams'] = dict(opts.stringparams)
    return merge_dicts(default_conf, clc)

def doc_io_and_base_uri(doc_fname, base_uri):
    if doc_fname != '-': return (open(doc_fname), base_uri)
    if base_uri:         return (sys.stdin, base_uri)
    cwd = ensure_trailing_sep(os.getcwd())
    logging.warning("doc base URI unspecified, fallback to cwd (%s)" % cwd)
    return                      (sys.stdin, cwd)

def load_extensions(ext_scripts, extensions={}):
    for s in ext_scripts:
        mname = os.path.splitext(os.path.basename(s))[0] # d/f.py => f
        extm = load_module(mname, open(s))
        for k, v in list(extm.extensions.items()): extensions[k]=v
    return extensions

# app

def main(argv):
    (opts, args) = opts_and_args()

    conf = runtime_conf(opts, DEFAULT_CONF)
    logging.basicConfig(level=logging.__dict__[conf['verbosity']])

    if len(args) != 2:
        logging.error("exactly 2 arguments required, but was: %s" % args)
        exit()
    (xsl_fname, doc_fname) = (args[0], args[1])
    (xsl_io, xsl_base_uri) = (open(xsl_fname), xsl_fname)
    (doc_io, doc_base_uri) = doc_io_and_base_uri(doc_fname,
                                                 conf['base_uri'])
    stringparams = conf['stringparams']
    extensions = load_extensions(conf['ext_scripts'])

    (result_tree, xslt_log) = apply(xsl_io, xsl_base_uri,
                                    doc_io, doc_base_uri,
                                    stringparams=stringparams,
                                    extensions=extensions)

    if xslt_log:
        for err in xslt_log:
            msg = '%s: %s (%s): %s\n' \
                % (os.path.basename(sys.argv[0]),
                   err.level_name, err.type_name, err.message)
            sys.stderr.write(msg.encode('utf-8'))
    if result_tree:
        sys.stdout.write(str(result_tree))
    return 1

if __name__ == "__main__":
    main(sys.argv)
