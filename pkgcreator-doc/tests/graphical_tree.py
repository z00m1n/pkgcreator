#!/usr/bin/env python
#-*- coding: utf-8 -*-
import sys
import os.path
import subprocess

lines = subprocess.check_output(["tree", "-f", "-n", "-S", "--noreport"]).split("\n")[1:]
#Generating tree
tree = []
for l in lines:
	if l:
		level = (l.index('\xc4\xc4') - 1) / 4
		filename = l.split('\xc4\xc4 ')[-1]
		tree.append((level, filename))

#Drawing tree
