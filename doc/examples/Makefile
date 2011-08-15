#!/usr/bin/make

PYXSLTP = pyxsltp
XSLTPROC= xsltproc --nodtdattr --nonet

OUT     = lorem.upcase.xsltproc.xhtml lorem.upcase.pyxsltp.xhtml

all: $(OUT)

lorem.upcase.xsltproc.xhtml: lorem.xhtml
	$(XSLTPROC) upcase.xsl $< > $@

lorem.upcase.pyxsltp.xhtml: lorem.xhtml
	$(PYXSLTP) --extension=upcase.py upcase.xsl $< > $@

clean:
	-rm -f $(OUT)

.PHONY: all clean
