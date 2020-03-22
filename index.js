var express = require('express');
var app = express();

const path = require('path');

const bodyParser = require('body-parser');
const fileUpload = require('express-fileupload');
const sanitizer = require('sanitize')(); //var name = sanitizer.value(req.name, 'string');

const middlewares = [
  bodyParser.urlencoded({extended: true}),
  express.static('public'),
  fileUpload(
    //useTempFiles : true,
    //tempFileDir : '/tmp/'
  ),
];

const routes = require('./routes/routes');
const formRoutes = require('./routes/formRoutes')
app.set('view engine', 'ejs')

app.use(middlewares);

app.use('/', routes);
app.use('/go/', formRoutes);

app.use(function(req, res, next){
	//questa va fatta piu' completa, dividendo i vari errori
  res.render('generic_error.ejs');
});

app.listen(8080);