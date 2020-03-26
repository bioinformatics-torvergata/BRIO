from sys import argv
import re



search=open(argv[1]).readlines()
db=open(argv[2]).readlines()
out=open(argv[3],'w')



for row in search:
	row=row.strip('\n')
	rowS=row.split('\t')
	out.write(row+'\t')
	for line in db:
		line=line.strip('\n')
		line=line.split('\t')
		#rowS[-1] contiene il nome della proteina 
		if rowS[-1].upper()==line[0]:
			out.write(line[-1]+'\t')
			#scrivo i dominii
			for pos in range(len(line)-1):
				if pos>=1:
					out.write(line[pos]+'\t')
			out.write('\n')
			break
	else:
		out.write('\n')

out.close