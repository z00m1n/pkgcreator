#!/bin/bash
xmlto xhtml -m style.xsl -o doc --skip-validation quickstart.xml
./xml2wiki.pl < doc/index.html > wiki/quickstart.wiki
