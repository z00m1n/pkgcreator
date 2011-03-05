#/bin/bash
#nroff -man pkgcreator_nroff.1 > pkgcreator.1 --> MAKES FILE INVALID!
cp pkgcreator_nroff.1 pkgcreator.1
gzip -9 pkgcreator.1
mv pkgcreator.1.gz ../../pkgcreator/man/
cp pkgcreator-gtk_nroff.1 pkgcreator-gtk.1
gzip -9 pkgcreator-gtk.1
mv pkgcreator-gtk.1.gz ../../pkgcreator-gtk/man/
