var express = require('express');
var app = express();

app.set('view engine', 'ejs')

app.get('/', function(req, res) {
  	res.render('landing.ejs');
});

app.get('/documentation', function(req, res) {
  	res.render('documentation.ejs');
});

app.get('/about', function(req, res) {
    	res.render('about.ejs');

});

app.get('/downloads', function(req, res) {
    	res.render('downloads.ejs');

});

app.get('/results/:uid', function(req, res) {
	//questa dovra' gestire i contenuti creati dallo script
    	res.render('results.ejs', {uid: req.params.uid});

});

app.get('/loading', function(req, res) {
	//questa dovra' attendere fino alla fine della creazione dei risultati
    	res.render('loading.ejs')
});

app.use(function(req, res, next){
	//questa va fatta un po' piu' completa, dividendo i vari errori
  res.render('generic_error.ejs');
});

app.listen(8080);