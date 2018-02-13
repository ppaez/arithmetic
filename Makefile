#
# Publish to web page src directory
#

VERSION = 0.6.2
PW_PATH=~/pw/src/python/arithmetic
RST2HTML = rst2html

all: index.html manual.html

%.html: %.rst
	LC_ALL=es_ES.UTF-8 $(RST2HTML) --report=3 --link-stylesheet --stylesheet-path=../../general.css $< $@

publish: dist/arithmetic-$(VERSION).tar.gz index.html manual.html
	mkdir -v $(PW_PATH)
	cp -avf dist/arithmetic-$(VERSION).tar.gz $(PW_PATH)
	cp -avf index.html manual.html $(PW_PATH)

unpublish: dist/arithmetic-$(VERSION).tar.gz
	rm -vf $(PW_PATH)/*
	rmdir -v $(PW_PATH)
