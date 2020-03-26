#questo script genera un primo file di output (mancano i dominii) che sichiama tmp/out-search_no_domains.txt 
#e che verra cancellato una volta che sara presente il file di output finale con i dominii.
#in questo file c'e scritto, per ogni ricerca eseguita (per ogni file presente in out_search_nuc e out_search_str) una riga

#la riga contiene il summary della ricerca cioe' modello, regione, numero motivo (m1,m2 o m3... questa info non verrà mostrata all'utente),
# perc|oddsratio|p-value, nome del file con i risultati (che potra' essere scaricato), nome rbp

import sys
import os
import functions


code=sys.argv[1]
f=open('users/'+code+'/tmp/search_out_no_domains.txt', 'a')

#apro il faile che mi dice se devo fare la ricerca su str, seq, o entrambi
which_motifs=open(sys.argv[2]).readline()

#controllo 
if 'bg' in os.listdir('users/'+code+"/"):
	bool_bg='T'
else:
	bool_bg='F'


##################SOLO STR
if which_motifs=='only-str':
	f.write('###############STR###############\n')
	f.write(functions.make_complete_search(code,'str', bool_bg))

##################SOLO SEQ
elif which_motifs=='only-seq':
	f.write('###############NUC###############\n')
	f.write(functions.make_complete_search(code,'nuc', bool_bg))
	
###################ENTRAMBI
else:
	f.write('###############STR###############\n')
	f.write(functions.make_complete_search(code,'str', bool_bg))
	f.write('###############NUC###############\n')
	f.write(functions.make_complete_search(code,'nuc', bool_bg))
	
	
f.close()

