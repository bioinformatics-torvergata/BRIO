#script lanciato dopo aver completato tutta la ricerca dei motivi
#prende in input il codice utente e il tipo di motivi selezionati
#genera gli istogrammi nella cartella hist

import functions
import sys
import os

code=sys.argv[1]
which_motifs=open(sys.argv[2]).readline()

#diz che avra' come chiave il nome del motivo (più precisamente il nome del file di output del search di beam) e come valore la lista delle posizioni in cui il motivo è stato trovato
dict_motif_perc_nuc={}
dict_motif_perc_str={}

if which_motifs=='only-str':
	for out_run_single_search in os.listdir('users/'+code+'/out_search_str'):
		#questa funzione genera il vettore con le percentuali di inizio del motivo su tutte le seq,
		#prende in input il file che contiene per ogni nome di rna la sua lunghezza e il file di output della run_search del motivo
		vet_perc = functions.create_perc_start_vet_STR('users/'+code+'/tmp/dict_name_len.txt', 'users/'+code+'/out_search_str/'+out_run_single_search)
		#riempio il diz
		dict_motif_perc_str[out_run_single_search]=vet_perc
	#creo istogramma
	functions.create_histogram(dict_motif_perc_str,'only-str','users/'+code+'/')
		
elif which_motifs=='only-seq':	
	for out_run_single_search in os.listdir('users/'+code+'/out_search_nuc'):
		#questa funzione genera il vettore con le percentuali di inizio del motivo su tutte le seq,
		#prende in input solo il file di output della run_search del motivo (la lunghezza sta in quel file)
		vet_perc = functions.create_perc_start_vet_NUC('users/'+code+'/out_search_nuc/'+out_run_single_search)
		#riempio il diz
		dict_motif_perc_nuc[out_run_single_search]=vet_perc
	#creo istogramma
	functions.create_histogram(dict_motif_perc_nuc,'only-seq','users/'+code+'/')
		
else:
	#copio i due cicli precedenti
	for out_run_single_search in os.listdir('users/'+code+'/out_search_str'):
		#questa funzione genera il vettore con le percentuali di inizio del motivo su tutte le seq,
		#prende in input il file che contiene per ogni nome di rna la sua lunghezza e il file di output della run_search del motivo
		vet_perc = functions.create_perc_start_vet_STR('users/'+code+'/tmp/dict_name_len.txt', 'users/'+code+'/out_search_str/'+out_run_single_search)
		#riempio il diz
		dict_motif_perc_str[out_run_single_search]=vet_perc
	


	for out_run_single_search in os.listdir('users/'+code+'/out_search_nuc'):
		#questa funzione genera il vettore con le percentuali di inizio del motivo su tutte le seq,
		#prende in input solo il file di output della run_search del motivo (la lunghezza sta in quel file)
		vet_perc = functions.create_perc_start_vet_NUC('users/'+code+'/out_search_nuc/'+out_run_single_search)
		#riempio il diz
		dict_motif_perc_nuc[out_run_single_search]=vet_perc
		
	#creo istogramma
	functions.create_histogram(dict_motif_perc_str,'only-str','users/'+code+'/')
	functions.create_histogram(dict_motif_perc_nuc,'only-seq','users/'+code+'/')
		
print(dict_motif_perc_nuc)
print(dict_motif_perc_str)