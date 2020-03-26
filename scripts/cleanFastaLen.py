import sys
import re

#file fasta con nome e sequenza
file1=sys.argv[1]
file2=open(sys.argv[2], "w")
file3=open(sys.argv[3], "w")
f1=open(file1).readlines()

for i in range (1, len(f1), 2):
	if len(f1[i])<=3000:
		file2.write(f1[i-1])
		file2.write(f1[i])
		
	else:
		file3.write(f1[i-1])
		file3.write(f1[i])
	

file2.close()
file3.close()
