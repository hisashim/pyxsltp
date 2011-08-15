#!/usr/bin/make

## variables

# metadata

PRODUCT  = pyxsltp
VERSION  = $(shell cat VERSION)
DATE     = $(shell dev/date.sh)
REVISION = $(shell dev/revstr.sh)
PACKAGE  = $(PRODUCT)
DEBREV   = $(shell head -n 1 debian/changelog \
                   | cut -d' ' -f 2 | sed 's/(\(.*\)-\(.*\))/\2/')

# programs

PYTHON   = python2.6 -B -Wall
TAR_XVCS = tar --exclude=".svn" --exclude=".git" --exclude=".hg"
PBUILDER = cowbuilder
PBOPTS   = --hookdir=pbuilder-hooks \
           --bindmounts "/var/cache/pbuilder/result"
DEBBUILDOPTS=

# directories and files

DESTDIR  = /usr/local
bindir   = $(DESTDIR)/bin
datadir  = $(DESTDIR)/share

TESTLOGS = $(foreach t,\
                     $(wildcard test/test*.py),\
                     $(t:test/test%.py=test%py.log))

DIST     = README LICENSE VERSION Makefile ChangeLog dev/ \
           pyxsltp.py setup.py

RELEASE  = $(PRODUCT)-$(VERSION)
SNAPSHOT = $(PRODUCT)-$(DATE)-$(REVISION)

DEB      = $(PACKAGE)_$(VERSION)-$(DEBREV)
DEBORIG  = $(PACKAGE)_$(VERSION).orig

## targets

all: test

.PHONY: all test install uninstall dist snapshot mostlyclean clean \
        deb pbuilder-build pbuilder-login pbuilder-test

# testing

test:   $(TESTLOGS)

test%py.log: test/test%.py
	PYTHONPATH=.:$$PYTHONPATH $(PYTHON) $< 2>&1 | tee $@

# installation

install: pyxsltp README LICENSE ChangeLog
	@if [ ! -d $(bindir) ]; then \
	  mkdir -p $(bindir); \
	fi
	@if [ ! -d $(datadir)/doc/$(PACKAGE) ]; then \
	  mkdir -p $(datadir)/doc/$(PACKAGE); \
	fi
	cp -Ppv pyxsltp $(bindir)/pyxsltp
	cp -Ppv README LICENSE ChangeLog $(datadir)/doc/$(PACKAGE)

uninstall:
	-rm -f $(bindir)/pyxsltp
	-rm -fr $(datadir)/doc/$(PACKAGE)

pyxsltp: pyxsltp.py
	cat $< | sed "s/'DEVELOPMENT_VERSION'/'$(VERSION)'/" > $@

# source package

dist:   $(RELEASE).tar.gz

snapshot: $(SNAPSHOT).tar.gz

$(RELEASE) $(SNAPSHOT): $(DIST)
	mkdir -p $@
	($(TAR_XVCS) -cf - $(DIST)) | (cd $@ && tar xpf -)

ChangeLog:
	dev/changelog.sh > $@

%.tar.gz: %
	tar -zcf $@ $<

# debian package

deb:    $(DEB)_all.deb

$(DEB)_all.deb: pbuilder-build
	cp /var/cache/pbuilder/result/$@ ./

pbuilder-build: $(DEB).dsc
	sudo $(PBUILDER) --build $< -- $(PBOPTS)

pbuilder-login:
	sudo $(PBUILDER) --login $(PBOPTS)

pbuilder-test: $(DEB)_all.deb
	sudo cowbuilder --execute pbuilder-hooks/test.sh $< -- $(PBOPTS)

$(DEB).dsc: $(RELEASE).tar.gz
	tar fxz $<
	($(TAR_XVCS) -cf - debian) | (cd $(RELEASE) && tar xpf -)
	cp $< $(DEBORIG).tar.gz
	(cd $(RELEASE) && pdebuild --pbuilder $(PBUILDER) $(DEBBUILDOPTS); cd -)

# cleaning

mostlyclean:
	-rm -f $(TESTLOGS) pyxsltp
	-rm -fr $(SNAPSHOT) $(RELEASE)
	-rm -f $(DEB)_*.build
	-rm -fr debian/$(PACKAGE)

clean: mostlyclean
	-rm -f ChangeLog
	-rm -f $(SNAPSHOT).tar.gz $(RELEASE).tar.gz
	-rm -f $(DEB).dsc $(DEBORIG).tar.gz $(DEB).diff.gz $(DEB)_*.deb \
	       $(DEB)_*.changes
