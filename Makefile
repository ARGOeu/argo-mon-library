PKGNAME := argo-mon-library
SPECFILE := $(PKGNAME).spec

PKGVERSION := $(shell rpm -q --qf '%{VERSION}\n' --specfile $(SPECFILE) 2>/dev/null || \
  grep -s '^Version:' $(SPECFILE) | sed -e 's/Version:[[:space:]]*//')

DIST ?= .el9

TARBALL := $(PKGNAME)-$(PKGVERSION).tar.gz

.PHONY: all srpm rpm dist sources clean
all: rpm

srpm: dist
	rpmbuild -bs $(SPECFILE) \
	  --define "_sourcedir $(PWD)" \
	  --define "_srcrpmdir $(PWD)" \
	  --define "dist $(DIST)"

rpm: dist
	rpmbuild -ba $(SPECFILE) \
	  --define "_sourcedir $(PWD)" \
	  --define "_rpmdir $(PWD)/rpms" \
	  --define "_srcrpmdir $(PWD)" \
	  --define "dist $(DIST)"

dist:
    @echo "PKGVERSION: '$(PKGVERSION)'"
	@echo "TARBALL: '$(TARBALL)'"
	rm -rf dist
	python3 setup.py sdist
	mv -f dist/$(TARBALL) .
	rm -rf dist

sources: dist

clean:
	rm -rf $(TARBALL) rpms *.src.rpm
	rm -f MANIFEST
	rm -rf dist
