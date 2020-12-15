# BRIO
BRIO webserver - Helmer-Citterich Lab

To lunch the server in background: 
	forever start index.js 
	
## Important things

* first time after git clone:
	npm cache clean --force
	rm -rf node_modules package-lock.json
	npm install

* docs
	* errorCodes : table of common error codes

* .gitignore : paths that must **NOT** be committed (like results or specific test data)

* routes
	* routes : handles request to / 
	* formRoutes : handles post requests to /go/

* scripts : python scripts and such. 

* public
	* css : contains bootstrap CSS (for now the JS is loaded via CDN)
