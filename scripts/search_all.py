#!/usr/bin/env python3
import sys
import os
import pickle
import functions






file_bear=sys.argv[1]
folder=sys.argv[2]

#mi salvo in una variabile su quali motivi devo fare la ricerca
which_motifs=open(sys.argv[3]).readline()

if which_motifs=='only-str':
	functions.make_search_all(which_motifs,file_bear,folder)
elif  which_motifs=='only-seq':
	functions.make_search_all(which_motifs,file_bear,folder)
else:
	functions.make_search_all('only-str',file_bear,folder)
	functions.make_search_all('only-seq',file_bear,folder)
	









