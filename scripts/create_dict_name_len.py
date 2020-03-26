import re
import sys

code=sys.argv[1]
folder='users/'+code+'/'

f=open(folder+'tmp/file_input_ready.txt')
line=f.readline()

out=open(folder+'tmp/dict_name_len.txt','w')
pos=0

while(line):
	if re.search('^>',line):
		out.write(line.strip()+'\t')
		pos_name=pos
	if pos==pos_name+1:
		out.write(str(len(line))+'\n')
		
	pos=pos+1
	line=f.readline()


out.close()



























