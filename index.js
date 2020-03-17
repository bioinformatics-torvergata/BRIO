var express = require('express');
var app = express();
const bodyParser = require('body-parser');

const middlewares = [
  bodyParser.urlencoded({extended: true}),
  express.static('public'),
];
const routes = require('./routes/routes');

app.set('view engine', 'ejs')

app.use(middlewares);

app.use('/', routes);

app.use(function(req, res, next){
	//questa va fatta piu' completa, dividendo i vari errori
  res.render('generic_error.ejs');
});

app.listen(8080);