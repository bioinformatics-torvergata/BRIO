
import sys
import os

import functions
import re


file_bear=sys.argv[1]
folder=sys.argv[2]
which_rbp=sys.argv[3]

which_motifs=open(sys.argv[4]).readline()


if which_motifs=='only-str':
	functions.make_single_search('only-str', file_bear,folder,which_rbp)
elif  which_motifs=='only-seq':
	functions.make_single_search('only-seq', file_bear,folder,which_rbp)
else:
	functions.make_single_search('only-str',  file_bear,folder,which_rbp)
	functions.make_single_search('only-seq',  file_bear,folder,which_rbp)



		
		
		
		
		
		
		
		
		
		
		











