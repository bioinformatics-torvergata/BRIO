#!/usr/bin/env python
# coding: utf-8

# In[8]:


import re
import os

import itertools as it


# In[27]:


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


# In[28]:


motifFolder = "../BRIO/some_motifs_str/"


# In[37]:




for filters in it.product(d_tech, d_species):
    print(filters)
    o = open("motifs_{}_{}".format(filters[0], filters[1]), 'w')
    for file in os.listdir(motifFolder):
        
        if filters[0] == 'eCLIP':
            if d_tech[filters[0]].match(file):
                fpath = os.path.join(motifFolder, file)
                o.write("\n\n#NAME\n")
                o.write(file + "\n\n")
                o.write("#BEAR\n")
                o.write(open(fpath).read())   
        else:        
            if d_tech[filters[0]].match(file) and d_species[filters[1]].match(file):
                fpath = os.path.join(motifFolder, file)
                o.write("\n\n#NAME\n")
                o.write(file + "\n\n")
                o.write("#BEAR\n")
                o.write(open(fpath).read())   
        

        
    o.close()


# In[ ]:





# In[ ]:




