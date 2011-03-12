DOCBOOK_SCHEMA=/usr/share/xml/docbook/schema/rng/5.0/docbook.rng
CSSTIDY_PARAMS  = --compress_colors=true --compress_font=true --lowercase_s=true
CSSTIDY_PARAMS += --remove_bslash=true --remove_last_\;=true --sort_properties=true
CSSTIDY_PARAMS += --sort-selectors=false --template=high

all:
	#xmllint --relaxng  $(DOCBOOK_SCHEMA) --noout quickstart.xml
	#xmlto -m styles/xsl/style.xsl -o html --skip-validation xhtml quickstart.xml
	cat styles/css/*.css | csstidy - doc$(CSSTIDY_PARAMS) html/style.css
	#tidy -utf8 -i -m html/index.html

wiki:
	@echo "Disabled..."
	#./xml2wiki.pl < doc/index.html > wiki/quickstart.wiki

man:
	cd man; \
	cp pkgcreator_nroff.1 pkgcreator.1; \
	gzip -9 pkgcreator.1; \
	chmod 644 pkgcreator.1.gz; \
	mv pkgcreator.1.gz ../../pkgcreator/man/; \
	cp pkgcreator-gtk_nroff.1 pkgcreator-gtk.1; \
	gzip -9 pkgcreator-gtk.1; \
	chmod 644 pkgcreator-gtk.1.gz; \
	mv pkgcreator-gtk.1.gz ../../pkgcreator-gtk/man/; \
