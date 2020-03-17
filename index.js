var express = require('express');
var app = express();
const bodyParser = require('body-parser');

const middlewares = [
  bodyParser.urlencoded({extended: true}),
];
const routes = require('./routes/routes');

app.set('view engine', 'ejs')

app.use(middlewares);

app.use('/', routes);

app.use(function(req, res, next){
	//questa va fatta un po' piu' completa, dividendo i vari errori
  res.render('generic_error.ejs');
});

app.listen(8080);