import sys
import os
import re
import functions


file_bear=sys.argv[1]
folder=sys.argv[2]
file_dom=sys.argv[3]

#apro il faile che mi dice se devo fare la ricerca su str, seq, o entrambi
which_motifs=open(sys.argv[4]).readline()


##################SOLO STR
if which_motifs=='only-str':
	functions.make_search_domains( 'only-str',file_bear,folder,file_dom)

##################SOLO SEQ
elif which_motifs=='only-seq':
	functions.make_search_domains( 'only-seq',file_bear,folder,file_dom)
	
###################ENTRAMBI
else:
	functions.make_search_domains( 'only-str', file_bear,folder,file_dom)
	functions.make_search_domains( 'only-seq',file_bear,folder,file_dom)



























