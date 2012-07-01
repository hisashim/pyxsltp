PyXSLTP
=======
PyXSLTP is an XSLT processor extensible with Python.

Usage
-----
Synopsis:

    pyxsltp [options] stylesheet document

Typical usage examples:

    pyxsltp --extension=ext.py style.xsl in.xml > out.xml
    ... | pyxsltp --base-uri=in.xml --extension=ext.py style.xsl - | ...

Requirements
------------
  * Python
  * lxml

Installation
------------
Use binary packages such as .deb or .rpm, if available.

Installation from the source:

    $ tar fxz pyxsltp-x.y.z.tar.gz
    $ cd pyxsltp-x.y.z
    $ sudo make install

Writing Extensions
------------------
See the following for detail:

  * doc/examples/*
  * lxml documentation (<http://lxml.de/extensions.html>)

License
-------
Copyright (c) 2011 Hisashi Morita.
All rights reserved.

This is free software published under X/MIT-style license.
See LICENSE for detail.
