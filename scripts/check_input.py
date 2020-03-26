import sys
import os
import re



#file input
inp=open(sys.argv[1])

#folder
folder=sys.argv[2]

#file errore
#error_page=open(folder+'error.php','w')







#funzione che trova e restituisce il tipo di errore
def find_errors(inp,folder):
	#tipo di input (nome+seq, nome+seq+dott-b, nome+seq+dott-b+bear)
	kind_of_file=''

	#elenco dei caratteri bear
	regex='^[abcdefghi=lmnopqrstuvwxyz^!#$%&\'()+234567890>ABCDEFGHIJKLMNOPQRSTUVWYZ~?_|/\\@{}\[\]:]*$'
	
	
	#salvo la len del file in una variabile  per il controllo successivo
	os.system('cat '+folder+'tmp/raw_file_temp.txt | wc -l > '+folder+'tmp/len_input.txt')
	f=open(folder+'tmp/len_input.txt')
	len_input=int(f.readline())
	
	
	




#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONTROLLO IN CHE TIPO DI FILE SONO (nome+seq, nome+seq+dott-b, nome+seq+dott-b+bear) ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


	#faccio una lista (lines) con le prime 4 linee cosi da capire quale tipo di file sto leggendo (nome+seq, nome+seq+dott-b, nome+seq+dott-b+bear)
	l=0
	lines=[]
	while l<=3:
		to_add=inp.readline()
		if to_add!='':
			lines.append(to_add)
		l=l+1
	print (lines)

	print (regex, lines[3])

	print (len(lines))
	if len(lines)<1:
		return 'Invalid input'



		
	#SE HO SOLO SEQ che si verifica se nella quarta riga ho una seq di nt o se la lunghezza==1
	elif re.search('^[ACUGTaucgt]*$', lines[3]) and re.search('^>',lines[2]) or len_input==1:
		kind_of_file='seq'

	#SE HO SEQ E DOTT-B che si verifica se nella quarta riga ho un nome di seq o se la lunghezza == 2
	elif re.search('^>', lines[3]) or len_input==2:
			kind_of_file='dot'

	#SE HO ANCHE IL BEAR (nella quarta riga)
	elif len(lines)==4 and re.search('^>', lines[0]) and re.search('^[ACUGTaucgt]*$', lines[1])!=None and re.search('^[\.\(\)]*$', lines[2])!=None and re.search(regex, lines[3])!=None:
			kind_of_file='bear'
	else: 
		return 'Invalid input'

	

	#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ CONTROLLO CHE TUTTE LE RIGHE SIANO UNIFORMI ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
	print (kind_of_file)
	#controllo (in base al tipo di file) ogni riga
	line=inp.readline()
	if kind_of_file=='seq':
		print ('sono qui')
		pos=0
		while line:
			print (pos%2)
			if pos%2!=0:
				if re.findall('^[ACUGTaucgt]*$', line)==False:
					return 'Error in sequences'
			if pos%2==0:
				if re.findall('^>', line)==False:
					return 'Error in names'
					
			pos=pos+1
			line=inp.readline()


	elif kind_of_file=='dot':
		pos=0
		while line:
			if line[0]=='^>':
				if line[pos+1]!=re.findall('^[ACUGTaucgt]*$', line)==False:
					return 'Error in sequences'
				if line[pos+2]!=re.findall('^[\.\(\)]*$', line):
					return 'Error in dot-bracket'
				if line[pos+3][0]!='^>':
					return 'error in line '+str(pos+3)
				
			pos=pos+1
			line=inp.readline()


	elif kind_of_file=='bear':
		pos=0
		while line:
			if line[0]=='^>':
				if line[pos+1]!=re.findall('^[ACUGTaucgt]*$', line)==False:
					return 'Error in sequences'
				if line[pos+2]!=re.findall('^[\.\(\)]*$', line):
					return 'Error in dot-bracket'
				if line[pos+3]!=re.findall(regex, line):
					
					err_found='yes'
					return 'Error in bear'
				if line[pos+4][0]!='^>':
					return 'error in line '+str(pos+3)
	
	#se arrivo qui, non c'e' errore nell'input
	return ''







#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~scrivo la pagina di errore~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#error_page.write('<?php echo file_get_contents("html/header.html");?>\n')

error=find_errors(inp,folder)
print (error)
#se la stringa di errore non è vuota
#if error!='':
	#file check errore
	#check_page=open(folder+'tmp/check_page.txt','w')
	#check_page.write('yes')
	#check_page.close()

	#error_page.write(error)
#else:
	#file check errore
	#check_page=open(folder+'tmp/check_page.txt','w')
	#check_page.write('no')
	#check_page.close()


#error_page.write('\n<?php echo file_get_contents("html/footer");?>')
#error_page.close()

print (error)














































