SVNVERSION=svn`svnversion | cut -f 1 -d :`
RELEASE=`cat RELEASE`
VERSION=$(RELEASE)$(SVNVERSION)

all: pkgcreator_deb pkgcreator-gtk_deb

doc:
	cd pkgcreator-doc/ && ./generate_quickstart.sh

man:
	cd pkgcreator-doc/man && ./generate_man.sh

build_dir:
	mkdir -p build/

pkgcreator_deb: build_dir man
	sudo pkgcreator -c pkgcreator/pkgcreator.yaml
	sudo mv pkgcreator/dist/pkgcreator-0.1.deb build/pkgcreator-$(VERSION).deb

pkgcreator-gtk_deb: build_dir man
	sudo pkgcreator -c pkgcreator-gtk/pkgcreator-gtk.yaml
	sudo mv pkgcreator-gtk/dist/pkgcreator-gtk-0.1.deb build/pkgcreator-gtk-$(VERSION).deb

install: pkgcreator_deb pkgcreator-gtk_deb
	sudo dpkg -i build/pkgcreator-$(VERSION).deb
	sudo dpkg -i build/pkgcreator-gtk-$(VERSION).deb

upload:
	./googlecode_upload.py -p pkgcreator -u leandro.mattioli -w `googlecodepasswd` -l Featured,Type-Package build/pkgcreator-$(VERSION).deb \
	-s 'pkgcreator console application (Ubuntu 10.10 Installer)'
	./googlecode_upload.py -p pkgcreator -u leandro.mattioli -w `googlecodepasswd` -l Featured,Type-Package build/pkgcreator-gtk-$(VERSION).deb \
	-s 'GTK editor for pkgcreator (Ubuntu 10.10 Installer)'
