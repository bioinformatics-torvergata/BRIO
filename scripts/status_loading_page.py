#import rhinoscriptsyntax as rs
import json
import sys
import functions
import os
import subprocess
from pathlib import Path



code=sys.argv[1]
name_out=sys.argv[2]
bool_bg=sys.argv[3]

with open('users/'+code+'/var_POST.json', 'r') as f:
	post = json.load(f)


#controllo ricerca
def check_perc(bool_bg, post):

	##############################tot contiene il totale dei files su cui fare la ricerca (viene moltiplicato per 3 perche 
	#per ogni file su cui fare la ricerca viene generato un file con l'output del search BEAM (in out_search_nuc/str) e un secondo file (in summary_nuc/str) con il summary della ricerca (da far vedere all'utente) e gli istogrammi
	
	if 'selected_RBP' in post.keys():
		if post['selected_RBP'][0]=='Select_all':
			####all motifs###
			print('prova1')
			if 'type-motifs' in post.keys():
				if post['type-motifs']=='only-seq':
					tot=len(os.listdir('motifs_nuc/'))*3
				elif post['type-motifs']=='only-str':
					tot=len(os.listdir('motifs_str/'))*3
				else:
					tot=(len(os.listdir('motifs_nuc/'))+len(os.listdir('motifs_str/')))*3
		else:
			####BBP####
			if post['selected_RBP']!='':
				list_rbps=post['selected_RBP']
				if 'type-motifs' in post.keys():
					if post['type-motifs']=='only-seq':
						list_files=functions.create_list_of_makeSearch(list_rbps, 'dict/dict_RBP_searchMotifs_nuc.txt')
						tot=len(list_files)*3
					elif post['type-motifs']=='only-str':
						list_files=functions.create_list_of_makeSearch(list_rbps, 'dict/dict_RBP_searchMotifs_str.txt')
						tot=len(list_files)*3
					else:
						list_files=functions.create_list_of_makeSearch(list_rbps, 'dict/dict_RBP_searchMotifs_nuc.txt')
						list_files=functions.create_list_of_makeSearch(list_rbps, 'dict/dict_RBP_searchMotifs_str.txt')
						tot=(len(list_files)+len(list_files))*3
		
	
	
	else:
		###domini###
		if 'selected_domains' in post.keys() and post['selected_domains']!='' and 'selected_RBP' not in post.keys():
			list_dom=post['selected_domains']
			if 'type-motifs' in post.keys():
				if post['type-motifs']=='only-seq':
					list_files=functions.create_list_of_makeSearch(list_dom, 'dict/dict_dom_searchMotifs_nuc.txt')
					tot=len(list_files)*3
				elif post['type-motifs']=='only-str':
					list_files=functions.create_list_of_makeSearch(list_dom, 'dict/dict_dom_searchMotifs_str.txt')
					tot=len(list_files)*3
					
				else: #se l'utente non ha scelto il tipo di motivi, faccio la ricerca su entrambi
					list_files_nuc=functions.create_list_of_makeSearch(list_dom, 'dict/dict_dom_searchMotifs_nuc.txt')
					list_files_str=functions.create_list_of_makeSearch(list_dom, 'dict/dict_dom_searchMotifs_str.txt')
					tot=(len(list_files_nuc)+len(list_files_str))*3
		

				
	#print(tot)
	
	#####################################################
	###############################se ho il bg
	done=0
	perc=0
	
	#se e presente bg, allora considero solo cartelle out_search_str e/o _nuc e non i summary.
	if bool_bg=='T':
		tot=tot+(tot/3)
	
	
	
	
	while done<tot:
		if bool_bg=='T':
			if 'type-motifs' in post.keys():
				if post['type-motifs']=='only-seq':
					done=(len(os.listdir('users/'+code+'/out_search_nuc/'))+len(os.listdir('users/'+code+'/bg/out_search_nuc/')))+(len(os.listdir('users/'+code+'/summary_nuc/')))+len(os.listdir('users/'+code+'/hist_nuc/'))
				if post['type-motifs']=='only-str':
					done=(len(os.listdir('users/'+code+'/out_search_str/'))+len(os.listdir('users/'+code+'/bg/out_search_str/')))+(len(os.listdir('users/'+code+'/summary_str/')))+len(os.listdir('users/'+code+'/hist_str/'))
				else:
					done1=(len(os.listdir('users/'+code+'/out_search_nuc/'))+len(os.listdir('users/'+code+'/out_search_str/'))+len(os.listdir('users/'+code+'/bg/out_search_nuc/'))+len(os.listdir('users/'+code+'/bg/out_search_str/')))+len(os.listdir('users/'+code+'/hist_nuc/'))+len(os.listdir('users/'+code+'/hist_str/'))
					done2=(len(os.listdir('users/'+code+'/summary_nuc/'))+len(os.listdir('users/'+code+'/summary_str/')))
					done=done1+done2
	
		
		#################controllo i file gia fatti
		else:
			if 'type-motifs' in post.keys():
				if post['type-motifs']=='only-seq':
					done=len(os.listdir('users/'+code+'/out_search_nuc/'))+len(os.listdir('users/'+code+'/summary_nuc/'))+len(os.listdir('users/'+code+'/hist_nuc/'))
				if post['type-motifs']=='only-str':
					done=len(os.listdir('users/'+code+'/out_search_str/'))+len(os.listdir('users/'+code+'/summary_str/'))+len(os.listdir('users/'+code+'/hist_str/'))
				else:
					done=(len(os.listdir('users/'+code+'/out_search_nuc/'))+len(os.listdir('users/'+code+'/out_search_str/')))+len(os.listdir('users/'+code+'/summary_nuc/'))+len(os.listdir('users/'+code+'/summary_str/'))+len(os.listdir('users/'+code+'/hist_nuc/'))+len(os.listdir('users/'+code+'/hist_str/'))

		
		perc=int((float(done)/tot*100))
		
		#print(done)
		#print (tot)
		#print ('\n')		
		
		if perc >=50 and perc<100:
			os.system('echo "'+str(perc)+'%, Output elaboration... Please Wait! "> '+ name_out)
		elif perc >=100:
		
			perc=100
			os.system('echo "'+str(perc)+'"> '+ name_out)
			
		else:
			os.system('echo "'+str(perc)+'%, Data elaboration " > '+ name_out)




check_perc(bool_bg, post)


