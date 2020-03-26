import re
import sys
import os
import zipfile
import json


folder=sys.argv[1]
code=folder.split('/')[1]
#apro la pag di output del sito
o=open(folder+code+'.php','w')
#####da modificare
with open(folder+"var_POST.json") as json_file:
	data=json.load(json_file)



o.write('<?php echo file_get_contents("html/header.html");?>')
#o.write('<script src="../../jquery.tablesorter.min.js"></script>\n')
o.write('<script>\n$(document).ready(function()\n{\n$("#sequence").tablesorter({\nsortList: [[4,0]],\nheaders: {0:{sorter:false},8:{sorter:false}}\n});\n}\n);\n</script>')
o.write('\n<script>\n$(document).ready(function()\n{\n$("#structure").tablesorter({\nsortList: [[4,0]],\nheaders: {0:{sorter:false},8:{sorter:false}}\n});\n}\n);\n</script>')


#aptro l'out della ricerca
f=open(folder+'/tmp/out_search.txt')
line=f.readline()


#controllo per capire se avevo aperto una tabella in precedenza
previous_table='no'

o.write('\n<br>Click here to download all your results \n')
o.write('\n<a href="../'+code+'.zip" download><button class="btn"><i class="fa fa-download"></i> Download</button></a>\n<br>\n')

o.write('<div class="tab">\n')

if ('type-motifs' not in data.keys())or (data["type-motifs"]=="both"):
	o.write('<button class="tablinks" onclick="openCity(event, \'Paris\')" id="defaultOpen">Sequence</button>\n')
	o.write('<button class="tablinks" onclick="openCity(event, \'London\')">Structure</button>\n')
	o.write('</div>')

elif data['type-motifs']=="only-seq":
	o.write('<button class="tablinks" onclick="openCity(event, \'Paris\')" id="defaultOpen">Sequence</button>\n')
	o.write('</div>')

elif data['type-motifs']=="only-str":
	o.write('<button class="tablinks" onclick="openCity(event, \'London\')" id="defaultOpen">Structure</button>\n')
	o.write('</div>')


while line:

	#scrivo che tipo di tabella vado a costruire (seq o str), scrivo anche la prima linea della tabella
	if re.search('STR',line):
		if previous_table=='yes':
			o.write('</tbody>\n</table>\n</div>\n')
		#o.write('\n<br>Structure motifs\n')
		o.write('<div id="London" class="tabcontent">')
		o.write('<table id="structure" class="out_table">\n<thead>\n<tr>\n<th>Motif</th>\n<th>Region </th>\n<th>Coverage </th>\n<th> oddsratio </th>\n<th> p-value </th>\n<th>Protein </th>\n<th>Domains </th>\n<th>Organism </th>\n<th>Download</th></tr>\n</thead>\n<tbody>\n')
		previous_table='yes'

	elif re.search('NUC',line):
		if previous_table=='yes':
			o.write('</tbody>\n</table>\n</div>\n')
		#o.write('\n<br>Sequences motifs\n')
		o.write('<div id="Paris" class="tabcontent">')
		o.write('<table id="sequence" class="out_table">\n<thead>\n<tr>\n<th>Motif</th>\n<th>Region </th>\n<th>Coverage</th>\n<th> oddsratio </th>\n<th> p-value </th>\n<th>Protein </th>\n<th>Domains </th>\n<th>Organism </th>\n<th>Download</th></tr>\n</thead>\n<tbody>\n')


		previous_table='yes'

	#############riempio la tabella con i dati
	line_vet_0=line.split('\t')
	line_vet=[x for x in line_vet_0 if x!='']
	line_vet.remove('\n')
	#estraggo il nome del file con i risultati della singola ricerca (su un solo modello) da lasciare per download
	if len(line_vet)>1 and re.search('nuc',line_vet[4]):
		which_folder='nuc'
		name_file=line_vet[4].split('.nuc')[0]+'_summary.nuc.txt'
		logo_link='logos/'+line_vet[4].split('.nuc')[0]+'_wl.nuc.png'
		print(logo_link)

	elif len(line_vet)>1:
		which_folder='str'
		name_file=line_vet[4].split('.txt')[0]+'_summary.str.txt'

		logo_link='logos/'+line_vet[4].split('.txt')[0]+'_wl.png'

	#se ho una linea di out_search.txt in cui ci sono anche i dominii (cioe' ho almeno sette elementi nella linea):
	if len(line_vet)>6:
		mot=line_vet[0]
		reg=line_vet[1]
		cov=line_vet[3].split('_')[0].split('|')[0]
		odd=line_vet[3].split('_')[0].split('|')[1]
		pval=str("%.3g" % float(line_vet[3].split('_')[0].split('|')[2]))
		prot=line_vet[5]
		org=line_vet[6]

		#scrivo motivo regione percentuale odds p-value proteina
		o.write('<tr>\n<td><div class=scrollable><img src="'+logo_link+'" width="100%" height="100%" ></div></td>\n<td>'+reg+'</td>\n<td>'+cov+'</td>\n<td><div class=scrollable>'+odd+'</div></td>\n<td><div class=scrollable>'+pval+'</div></td>\n<td><div class=scrollable>'+prot+'</div></td>\n<td>')

		#scrivo i dominii
		for pos in range(7,len(line_vet)):
			dom=line_vet[pos]
			o.write(dom+'<br>')
		#scrivo organismo e download
		o.write('</td>\n<td><div class=scrollable>'+org+'</div></td>\n<td><div class=scrollable><a href="summary_'+which_folder+'/'+name_file+'" target="_blank"><button class="btn"><i class="fa fa-download"></i> Show file</button></a><br><a href="summary_'+which_folder+'/'+name_file+'" download><button class="btn"><i class="fa fa-download"></i> Download</button></a></div></td>\n</tr>')

#	#se ho una linea senza dominii ma solo il nome prot:
#	elif len(line_vet)>1:
#		o.write('<tr>\n<td>'+line_vet[0]+'</td>\n<td>'+line_vet[1]+'</td>\n<td>'+line_vet[3]+'</td>\n<td>'+line_vet[5]+'</td>\n<td> </td>\n<td> </td>\n<td><a href="summary_'+which_folder+'/'+name_file+'" target="_blank">'+name_file+'</a><br><a href="summary_'+which_folder+'/'+name_file+'" download>Download</a></td>\n</tr>')
	line=f.readline()


o.write('</tbody>\n</table>\n</div>\n')

o.write('\n<script>\nfunction openCity(evt, cityName) {\n')
o.write('var i, tabcontent, tablinks;\ntabcontent = document.getElementsByClassName("tabcontent");\n')
o.write('for (i = 0; i < tabcontent.length; i++) {\ntabcontent[i].style.display = "none";\n}\n')
o.write('tablinks = document.getElementsByClassName("tablinks");\n')
o.write('for (i = 0; i < tablinks.length; i++) {\n')
o.write('tablinks[i].className = tablinks[i].className.replace(" active", "");\n}\n')
o.write('document.getElementById(cityName).style.display = "block";\n')
o.write('evt.currentTarget.className += " active";\n}\n')
o.write('document.getElementById("defaultOpen").click();\n</script>\n')

o.write("<?php echo file_get_contents('html/footer.html');?>")
































