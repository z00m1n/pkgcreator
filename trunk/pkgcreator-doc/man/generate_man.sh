#/bin/bash
#nroff -man pkgcreator_nroff.1 > pkgcreator.1 --> MAKES INVALID FILE !
cp pkgcreator_nroff.1 pkgcreator.1
gzip -9 pkgcreator.1
chmod 644 pkgcreator.1.gz
mv pkgcreator.1.gz ../../pkgcreator/man/
cp pkgcreator-gtk_nroff.1 pkgcreator-gtk.1
gzip -9 pkgcreator-gtk.1
chmod 644 pkgcreator-gtk.1.gz
mv pkgcreator-gtk.1.gz ../../pkgcreator-gtk/man/
