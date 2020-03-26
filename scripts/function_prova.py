#!/usr/bin/env python3
import re
import os
import cgi
import cgitb; cgitb.enable()
import matplotlib
matplotlib.use( 'Agg' )
import pylab
import scipy.stats as stats





#funzione che apre un file di due colonne (una con la chiave l'altra col valore) e genera un dizionario
def open_dict(dic_file):
	dictionary={}
	f=open(dic_file,'r').readlines()
	
	for line in f:
		line_spl=line.split('\t')
		dictionary[line_spl[0]]=float(line_spl[1])
	return dictionary

		


		


# funzione che prende in input un file di sequenze foldate  e un motivo
# lancia il file search (che cerca il motivo nelle sequenze e restitusce lo score)
#salva l'output in un nuovo file
def run_search(motif_folder, motif,file_bear,file_out, which_motifs, folder):
	if which_motifs=='str':
		os.system('java -jar script/search1.2.jar '+motif_folder+motif+' '+file_bear+' > '+file_out)
	elif which_motifs=='nuc':
		os.system('python3 script/Search_nt.py '+motif_folder+motif+' '+file_bear+' '+file_out)

		
		
#funzione che dall'output della run_search, calcola la percentuale di sequenze che hanno uno score maggiore a quello che si trova nel dizionario assegnato al motivo
#il motivo e lo stesso di prima
def perc_seq_motif(motif,inp_search,dic,which_motifs):
	#num seq col motivo
	major=0
	#num seq senza motivo
	minor=0
	tot=0
	threshold=dic[motif]
	
	f=open(inp_search,'r').readlines()
	if which_motifs=='str':
		for line in f:
			line = line.split('\t')
			if len(line)>2:
				tot=tot+1
				val=float(line[3].strip('\n'))
				if val>threshold:
					major=major+1
				
	if which_motifs=='nuc':
		for line in f:
			tot=tot+1
			val=float(line.split('\t')[2])
			if val>threshold:
				major=major+1
	
	if tot==0:
		perc=0
	else:
		perc=float(major)/tot*100	
		minor=tot-major
	return (perc,major,minor)


		
		
		
def Search_motif_name(file_bench):
	f=open(file_bench)
	line=f.readline()
	pssm=[]
	while(line):
		if line=="#PSSM\n":
			pssm.append(line.split())
			while (line[0:6] != "#score"):
				line=f.readline()
				pssm.append(line.split())

		line=f.readline()

	m=[el[0] for el in pssm[1:-2]]
	motif_name=''.join(m)
	return motif_name


#questa funzione, da usare dopo aver usato run_search, mette in un vettore le percentuali di start dei motivi sulle seq
#partendo da un file da cui ricavare la lunghezza seq, che e' fatto di due colonne una col nome e una con la lunghezza,
#e dall'out della funz run_search
def create_perc_start_vet_STR(file_name_len, run_single_search):
	#apro il file che contiene nome seq e len seq
	f=open(file_name_len)
	line_dict_name_len=f.readline()
	#apro il file risultante dal search di beam STR
	g=open(run_single_search)
	line_run=g.readline()
	pos_line_run=0
	pos_name=0
	dict_nome_start={}
	#faccio un ciclo che genera il dizionario nome seq, posizione di start del motivo  che salvo in dict_nome_start
	while line_run:
		line_run=line_run.strip('[INFO]')
		if re.search('^>',line_run):
			pos_name=pos_line_run
			name=line_run.strip('\n')
		if pos_name!=0 and pos_line_run==pos_name+1:
			dict_nome_start[name]=line_run.split('\t')[1]
		
		pos_line_run=pos_line_run+1
		line_run=g.readline()
	#faccio un ciclo che genera una lista con i numeri da usare nell'istogramma che si chiama vet_perc
	vet_perc=[]
	while line_dict_name_len:
		name_seq=line_dict_name_len.split('\t')[0]
		len_seq=line_dict_name_len.split('\t')[1].strip('\n')
		for key in dict_nome_start:
			if key==name_seq:
				start=dict_nome_start.get(key)
				perc_start= (float(start)/float(len_seq))*100
				vet_perc.append(perc_start)
				break
		line_dict_name_len=f.readline()
	return (vet_perc)

#la versione per la ricerca sui nuc
#questa funzione, da usare dopo aver usato run_search, mette in un vettore le percentuali di start dei motivi sulle seq


def create_perc_start_vet_NUC(run_single_search):
	vet_perc=[]
	#apro il file risultante dal search di beam STR
	f=open(run_single_search)
	line_run=f.readline()
	while line_run:
		start_motif=line_run.split('\t')[4]
		len_seq=line_run.split('\t')[3]
		perc_start= (float(start_motif)/float(len_seq))*100
		vet_perc.append(perc_start)
		
		line_run=f.readline()

	return (vet_perc)
	
	
	
	

#questa funzione prende un vettore di percentuali di inizio motivo (out della funz create_perc_start_vet), il path della cartella ('users/code/hist_nuc'o'users/code/hist_str')
# e nome dell'immagine di outpt
# genera un istogramma
def create_histogram(dict_motif_perc,which_motifs,folder):

	for key in dict_motif_perc:
		pylab.xlim(0,100)
		pylab.hist(dict_motif_perc[key], bins=50)
		if which_motifs=='only-seq':
			pylab.savefig(folder+'hist_nuc/'+key.split('txt')[0]+'hist.nuc.png')
		elif which_motifs=='only-str':
			pylab.savefig(folder+'hist_str/'+key.split('txt')[0]+'hist.str.png')
		pylab.close()
	
'''
def create_histogram(vet_perc,folder, name_out):
	for perc in vet_perc:
		pylab.xlim(0,100)
		pylab.hist(perc, bins=50)
		pylab.savefig('da_buttare.png')
		#pylab.savefig(folder+'/'+name_out)
		pylab.close()
'''	

#questa funzione crea il file che contiene modello, tot_seq_col_motivo, tot_seq_senza_motivo
#questo file verra' usato per il test fisher
#la funzione prende in input l'output della ricerca (attenzione, vuole il path completo dalla web root) e il nome del file summary
#lo lancio alla fine dello script make_summary.py
def create_summary_file(out_search,summary_file):
	f=open(out_search)
	d_line=f.readline()
	out=open(summary_file,'w')
	out.write('file_name	model	rna_with_motif	rna_without_motif\n')
	while (d_line):
		line=d_line.split('\t')
		line_vet=[x for x in line if x!='']
		if len(line_vet)<=2:
			out.write(d_line)
		else:
			#scrivo nome modello maggiori e minori
			to_write=line_vet[4]+'\t'+line_vet[0]+'\t'+line_vet[3].split('_')[1]+'\t'+line_vet[3].split('_')[2]+'\n'
			out.write(to_write)
		d_line=f.readline()
	
	


#################################################        FUNZIONE PER SEARCH_ALL                 #########################################
#funzione che prende in input una cartella con i motivi da cercare e lancia le precedenti due funzioni, scrivendo l'output su un file
#inoltre lancia la funzione create_perc_start_vet su ogni ricerca del motivo e salva le percentuali di strt complessive su un vettore(mi serve per fare 
#l'istogramma)


def make_search_all(which_motifs,file_bear,folder):

#SE CERCO SOLO STR	
	if which_motifs=='only-str':
		for motif in os.listdir('motifs_str'):
			file_out=folder+'out_search_str/'+motif.split('.')[0]+'_out_search.str.txt'
            #os.system('cp -R /home/sangiovanni/public_html/brio/motifs_logo/str/ '+folder+'logos/')
			run_search('motifs_str/', motif, file_bear,file_out,'str',folder)
			
			
			
		
#SE CERCO SOLO SEQ
	elif which_motifs=='only-seq':
		for motif in os.listdir('motifs_nuc/'):
			file_out=folder+'out_search_nuc/'+motif.split('.')[0]+'_out_search.nuc.txt'
            #os.system('cp -R /home/sangiovanni/public_html/brio/motifs_logo/nuc/ '+folder+'logos/')
			run_search('motifs_nuc/', motif, file_bear,file_out,'nuc',folder)
			
			
			
			


#########################################################		FUNZIONI PER LA RICERCA SU DOMINII		############################################################################################



#questa funzione apre la il file che contiene i nomi dei dominii e genera una lista di nomi dei dominii
def create_list_of_dom(dirty_dom_file):
	dom=[]
	#apro il file con i nomi del dominio
	dirty_dom=open(dirty_dom_file).readlines()[1:-1]
	for dirty_line in dirty_dom:
		line=dirty_line.strip().split('\'')[1]
		dom.append(line)
   #ritorna lista unica di elementi nella textarea dei domini
	return list(set(dom))


#crea una lista con i nomi dei motivi su cui fare la ricerca partendo dalla lista dei dominii e dal file che associa ogni dominio ai nomi dei files di ricerca
def create_list_of_makeSearch (list_of_doms, association_dom_search_file):
	association=open(association_dom_search_file).readlines()
	make_search_0=[]
	for single_dom in list_of_doms:	
		for dirty_line in association:
			line=dirty_line.split('\t')
			if line[0]==single_dom:
				make_search_0=make_search_0+line[1:]
	
				
	make_search=[x for x in make_search_0 if x != "\n"]
	return sorted(set(make_search))




#funzione che fa la ricerca dei motivi sulle sequenze che mette l'utente in input
def make_search_domains(which_motifs, file_bear,folder,file_dom):

	#salvo in una lista i dominii su cui fare la ricerca
	dom=create_list_of_dom(file_dom)
	
####SOLO STR	
	if which_motifs=='only-str':
		#salvo i motivi in una variabile
		motifs=os.listdir('motifs_str')
		#creo una lista con i nomi dei files su cui fare la ricerca
		make_search_str=create_list_of_makeSearch (dom, 'dict/dict_dom_searchMotifs_str.txt')
		for single_search in make_search_str:
			for motif in motifs:
				if single_search==motif:
					file_out=folder+'out_search_str/'+motif.split('.')[0]+'_out_search.str.txt'
                    file_name_logo=motif.split('.txt')[0]
                    print(file_name_logo)
                    #os.system('cp /home/sangiovanni/public_html/brio/motifs_logo/str/'+file_name_logo+'* '+folder+'logos/')
					run_search('motifs_str/', motif, file_bear,file_out,'str',folder)

####SOLO NUC
	elif which_motifs=='only-seq':
		#salvo i motivi in una variabile
		motifs=os.listdir('motifs_nuc')
		#creo una lista con i nomi dei files su cui fare la ricerca
		make_search_nuc=create_list_of_makeSearch (dom, 'dict/dict_dom_searchMotifs_nuc.txt')
		for single_search in make_search_nuc:
			for motif in motifs:
				if single_search==motif:
					file_out=folder+'out_search_nuc/'+motif.split('.')[0]+'_out_search.nuc.txt'
                    file_name_logo=motif.split('.txt')[0]
                    print(file_name_logo)
                    #os.system('cp /home/sangiovanni/public_html/brio/motifs_logo/str/'+file_name_logo+'* '+folder+'logos/')
					run_search('motifs_nuc/', motif, file_bear,file_out,'nuc',folder)
		

#####################################################		FUNZIONI PER LA RICERCA SU SINGOLA RBP		####################################################################

def make_single_search(which_motifs,file_bear,folder,rbp_file):
	
	
	#apro il file che contiene il nome della singola rbp
	rbp=open(rbp_file).readlines()
	
######SOLO STR
	if which_motifs=='only-str':
		#salvo i motivi in una variabile
		motifs=os.listdir('motifs_str')
		#creo una lista con i nomi dei files su cui fare la ricerca
		make_search_str=create_list_of_makeSearch (rbp, 'dict/dict_RBP_searchMotifs_str.txt')
		for single_search in make_search_str:
			for motif in motifs:
				if single_search==motif:
					file_out=folder+'out_search_str/'+motif.split('.')[0]+'_out_search.str.txt'
					run_search('motifs_str/', motif, file_bear,file_out,'str',folder)
				
				
		
#######SOLO NUC
	elif which_motifs=='only-seq':
		#salvo i motivi in una variabile
		motifs=os.listdir('motifs_nuc')
		#creo una lista con i nomi dei files su cui fare la ricerca
		make_search_nuc=create_list_of_makeSearch (rbp, 'dict/dict_RBP_searchMotifs_nuc.txt')
		for single_search in make_search_nuc:
			for motif in motifs:
				if single_search==motif:
					file_out=folder+'out_search_nuc/'+motif.split('.')[0]+'_out_search.nuc.txt'
					run_search('motifs_nuc/', motif, file_bear,file_out,'nuc',folder)
				
	



	

#legge tutti i file di output delle run, calcola fisher e restituisce cose da scrivere nel file di output finale(quasi, mancano i dominii).
def make_complete_search(code,which_motifs, bool_bg):
	
	to_write=""
	#dizionario per compleate search
	if which_motifs == 'str':
		dict_=open_dict('dict/dict_str.txt')

	else:
		dict_=open_dict('dict/dict_nuc.txt')
		
	
		
	#lista con tutti i motivi su cui ho fatto la ricerca
	lista_out_search=os.listdir('users/'+code+'/out_search_'+which_motifs+'/')
	
	for motif in lista_out_search:
		if re.search('nuc', motif):
			motif_key=motif.split('_out_')[0]+'.nuc.txt'
		else:
			motif_key=motif.split('_out_')[0]+'.txt'
		
		file_out_RunSearch='users/'+code+'/out_search_'+which_motifs+'/'+motif		
		perc,major,minor=perc_seq_motif(motif_key, file_out_RunSearch, dict_, which_motifs)
		
		
		if bool_bg=='T':
			file_out_RunSearch='users/'+code+'/bg/out_search_'+which_motifs+'/'+motif
			perc_bg,major_bg,minor_bg=perc_seq_motif(motif_key, file_out_RunSearch, dict_, which_motifs)
		
		else:
			#creo dizionario per bg: chiave=nome, lista=[major, minor]
			f=open('summary_AutoBg.txt')
			line=f.readline()
			dict_bg={}
			while (line):
				dict_bg[line.split()[0]]=[int(line.split()[2]),int(line.split()[3])]
				line=f.readline()
			
			
			major_bg=dict_bg[motif_key][0]
			minor_bg=dict_bg[motif_key][1]
		
		#calcolo fisher test
		oddsratio, pvalue = stats.fisher_exact([[major, major_bg], [minor, minor_bg]])
		
		motif_name=Search_motif_name('motifs_'+which_motifs+'/'+motif_key)
		regione=str(motif_key.split('_')[-3])
		n_motif=str(motif_key.split('_')[-2])
		RBP_name=str(motif_key.split('_')[1])
		#scrivo modello, regione, numero motivo, perc|oddsratio|p-value, nome del file con i risultati (che potra' essere scaricato), nome rbp
		to_write+=motif_name+"\t"+regione+"\t"+n_motif+"\t"+str(round(perc,2))+"|"+str(round(oddsratio,2))+"|"+str(pvalue)+"\t"+motif_key+"\t"+RBP_name+"\n"
		
	return to_write











