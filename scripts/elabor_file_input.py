#questo programma prende un file di sequenze di rna, lancia tutti gli eseguibili 
#per ottenere, per ogni sequenza, il codice in dott braket e bear

import sys
import os
import re

file_seq=sys.argv[1]
folder=sys.argv[2]


#controllo che ci sia un maggiore in prima posizione in quello che l'utente scrive nella textarea
if re.search('^>', open(file_seq).readline()):
	#genero una lista con le prime quattro righe dell input per il controllo successivo
	file = open(file_seq,"r")
	l=0
	lines=[]

	while l<=3:
		lines.append(file.readline())
		l=l+1
	file.close()
	

	#salvo la len del file in una variabile  per il controllo successivo
	os.system('cat '+folder+'tmp/raw_file_temp.txt | wc -l > '+folder+'tmp/len_input.txt')
	f=open(folder+'tmp/len_input.txt')
	len_input=int(f.readline())
	#os.system('rm '+folder+'tmp/len_input.txt')
	

	
	#######1 metto tutto maiusc ###################################################################
	os.system('ruby script/convert.rb '+file_seq+' '+folder+'tmp/file_seq_maiusc.txt')
	#os.chmod(folder+'tmp/file_seq_maiusc.txt', 0777)
	

	
	
	#######2 limito la lunghezza ###################################################################
	file_seq_maiusc=open(folder+'tmp/file_seq_maiusc.txt').read()
	conta=(file_seq_maiusc.count('>'))
	
	if conta>=1000:
		#lancio programma che leva le seq con len > 500
		os.system('python3 script/cleanFastaLen500.py '+folder+'tmp/file_seq_maiusc.txt '+folder+'tmp/file_seq_limit '+folder+'tmp/file_seq_dismiss.txt')

	else:
		#lancio il programma che leva le seq con len > 3000
		os.system('python3 script/cleanFastaLen.py '+folder+'tmp/file_seq_maiusc.txt '+folder+'tmp/file_seq_limit.txt '+folder+'tmp/file_seq_dismiss.txt')
		


#####SE HO SOLO SEQ
	#che si verifica se nella quarta riga ho una seq di nt o se la lunghezza==1
	if (re.findall('^[ACUGTaucgt]*$', lines[3][:-1])!='None' and re.search('^>',lines[2])) or len_input==1:
		
		#3)foldo l'rna con RNAfold##################################################################################
		os.system('RNAfold --noPS < '+folder+'tmp/file_seq_limit.txt > '+folder+'tmp/file_foldato_energies.txt')
	
		#4)devo levare il parametro dell'energia minima##############################################################
		os.system('python3 script/cleanEnergies.py '+folder+'tmp/file_foldato_energies.txt > '+folder+'tmp/file_foldato.txt')
	
		#5)devo aggiungere la notazione bear#########################################################################
		os.system('java -jar script/BearEncoder_new.jar '+folder+'tmp/file_foldato.txt '+folder+'tmp/file_input_ready.txt')
		
		#rimuovo i files generati nei vari punti che non mi servono 
		os.system('rm '+folder+'tmp/file_seq_maiusc.txt '+folder+'tmp/file_seq_limit.txt '+folder+'tmp/file_foldato_energies.txt '+folder+'tmp/file_foldato.txt')


	
		
#####SE HO SEQ E DOTT-B
	#che si verifica se nella quarta riga ho un nome di seq o se la lunghezza == 2
	elif re.search('^>', lines[3]) or len_input==2:
	
		#5) aggiungo il bear######################################################################################
		os.system('java -jar script/BearEncoder_new.jar '+folder+'tmp/file_seq_limit.txt '+folder+'tmp/file_input_ready.txt')
		
	
		#rimuovo i files generati nei vari punti che non mi servono
		#os.system('rm '+folder+'tmp/file_seq_maiusc.txt '+folder+'tmp/file_seq_limit.txt')		
		
		
####SE HO SEQ DOTT-B E BEAR
	else:
		os.system('mv '+folder+'tmp/file_seq_limit.txt '+folder+'tmp/file_input_ready.txt')
		#os.system('rm '+folder+'tmp/file_seq_maiusc.txt')


	
	
	
	
	
	
	
	
	
	
	
	
	
