#!/usr/bin/env python
# coding: utf-8

"""
group old motif files in a more compact way
"""

import re
import os
import sys
import itertools as it


print("please remember that for now,\n\
    eCLIP regex pattern is enforced on human. Remember this if\n\
    new mouse eCLIP data comes along")

hg19_re = re.compile("^.*_hg19_.*$")
mm9_re = re.compile("^.*_mm9_.*$")

hits_re = re.compile("^HITS|^CLIPSeq")
par_re = re.compile("^PAR")
eclip_re = re.compile("^ENC")

d_tech ={
    'eCLIP': eclip_re,
    'HITS': hits_re,
    'PAR': par_re,
}

d_species = {
    'hg19': hg19_re,
    'mm9': mm9_re
}


if len(sys.argv)<3:
    print("please specify the directory where the motifs are stored (1) and one between {seq|str}")
    exit()
#motifFolder = "../BRIO/some_motifs_str/"
motifFolder = sys.argv[1]
seqFlag = (sys.argv[2] == 'seq')
type_ID = "#NT" if seqFlag else "#BEAR"

for filters in it.product(d_tech, d_species):
    print(filters)
    o = open("motifs_{}_{}_{}.txt".format(filters[0], filters[1], sys.argv[2]), 'w')
    for file in os.listdir(motifFolder):
        
        if filters[0] == 'eCLIP':
            """eCLIP has weird name patterns, only for human now"""
            if d_tech[filters[0]].match(file) and filters[1] == 'hg19':
                fpath = os.path.join(motifFolder, file)
                o.write("\n\n#NAME\n")
                o.write(file + "\n\n")
                o.write(f"{type_ID}\n") 
                o.write(open(fpath).read())   
        else:        
            if d_tech[filters[0]].match(file) and d_species[filters[1]].match(file):
                fpath = os.path.join(motifFolder, file)
                o.write("\n\n#NAME\n")
                o.write(file + "\n\n")
                o.write(f"{type_ID}\n")
                o.write(open(fpath).read())   
        

        
    o.close()