#!/usr/bin/python
#creato da noise
#pulisce le energie dell'output di RNAfold
from __future__ import print_function

import sys

file=sys.argv[1]
f=open(file)

line=f.readline()

while(line):
	print(line.strip())
	line = f.readline()
	print(line.strip())
	line = f.readline()
	print(line.split()[0].strip())
	line = f.readline()

