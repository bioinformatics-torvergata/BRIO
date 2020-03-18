###QUESTO E' UNO SCRIPT DI PROVA
"""
	riceve argv da node
	crea cartella
	crea file
	comunica se non riesce a creare la cartella
"""

import sys 
import os 

resultsRoot = "results" 

userFolder = sys.argv[1] #create something like fixed length random string
filePath = sys.argv[2] 


#creating user directory
try:
	os.mkdir(os.path.join(resultsRoot,userFolder))
except OSError:
	dataToSendBack = "Creation of the directory {} failed".format(userFolder)
	print(dataToSendBack, file=sys.stderr)
	#no need to flush the stderr, for it is not buffered
	sys.exit(2) ##needed to let the stderr flush correctly?
else:
	dataToSendBack = "Successfully created the directory {} ".format(userFolder)
	print(dataToSendBack)
	sys.stdout.flush()



#writing file
with open(os.path.join(resultsRoot,userFolder, filePath), 'w') as f: 
	f.write("Hello World!") 

#signaling to parent if ok
dataToSendBack = "il test e' andato bene"
print(dataToSendBack)
sys.stdout.flush() ##get back data to Node

