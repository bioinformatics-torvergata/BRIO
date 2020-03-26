#questo script nella prima parte genera tutti i file presenti nei summary di seq e str (da scaricare)
#nella seconda genera il file summary di tutta la ricerca completa, da usare per fisher obsoleta.... fischer lo calcolo in script/complete_search.py lanciato in precedenza
import os
import re
import functions
import sys


folder=sys.argv[1]

dict_nuc=functions.open_dict('dict/dict_nuc.txt')
dict_str=functions.open_dict('dict/dict_str.txt')

#MOTIVI SEQUENZA
for sequence_search in os.listdir(folder+'out_search_nuc'):
	threshold=dict_nuc[sequence_search.split('_out')[0]+'.nuc.txt']
	f=open(folder+'out_search_nuc/'+sequence_search).readlines()
	o=open(folder+'summary_nuc/'+sequence_search.split('_out')[0]+'_summary_notSorted.nuc.txt','w')
	o.write('name\tmotif\tscore\tlength\tstart\tend\tthreshold\n')
	for line in f:
		#if line.split('\t')[2]>=threshold:
		o.write(line.strip('\n')+'\t'+str(threshold)+'\n')
	o.close()

	os.system('head -n1 '+folder+'summary_nuc/'+sequence_search.split('_out')[0]+'_summary_notSorted.nuc.txt >> '+folder+'summary_nuc/'+sequence_search.split('_out')[0]+'_summary.nuc.txt && tail -n+2 '+folder+'summary_nuc/'+sequence_search.split('_out')[0]+'_summary_notSorted.nuc.txt | sort -k 3,3gr >> '+folder+'summary_nuc/'+sequence_search.split('_out')[0]+'_summary.nuc.txt')
	os.system('rm '+folder+'summary_nuc/'+sequence_search.split('_out')[0]+'_summary_notSorted.nuc.txt')
	
	
	
	
#MOTIVI STRUTTURA	
pos=0
pos_name=-10
dict_len=functions.open_dict(folder+'tmp/dict_name_len.txt')


for sequence_search in os.listdir(folder+'out_search_str'):
	threshold=dict_str[sequence_search.split('_out')[0]+'.txt']
	#risultato della ricerca del motivo (search di beam)
	f=open(folder+'out_search_str/'+sequence_search)
	#output in cui scrivere il summary della rcierca
	o=open(folder+'summary_str/'+sequence_search.split('_out')[0]+'_summary_notSorted.str.txt','w')
	o.write('name\tmotif\tscore\tlength\tstart\tend\tthreshold\n')
	line=f.readline()
	line=f.readline()
	line=f.readline()
	line=f.readline()
	line=f.readline()
	line=f.readline().strip('[INFO]')
	
	while (line != '\n'):
		lenght=dict_len[line[:-1]]
		o.write(line[:-1]+'\t')
		line=f.readline().strip('[INFO]')
		line_vet=line.split('\t')
		o.write(line_vet[0]+'\t'+line_vet[3].strip('\n')+'\t'+str(int(lenght))+'\t'+line_vet[1]+'\t'+line_vet[2]+'\t'+str(threshold)+'\n')
		line=f.readline().strip('[INFO]')
	o.close()
	
	
	os.system('head -n1 '+folder+'summary_str/'+sequence_search.split('_out')[0]+'_summary_notSorted.str.txt >> '+folder+'summary_str/'+sequence_search.split('_out')[0]+'_summary.str.txt && tail -n+2 '+folder+'summary_str/'+sequence_search.split('_out')[0]+'_summary_notSorted.str.txt | sort -k 3,3gr >> '+folder+'summary_str/'+sequence_search.split('_out')[0]+'_summary.str.txt')
	os.system('rm '+folder+'summary_str/'+sequence_search.split('_out')[0]+'_summary_notSorted.str.txt')
	
	
	
	
	
	
	
	
	




