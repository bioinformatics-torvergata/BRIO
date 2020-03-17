//routes.js

const express = require('express');

const { check, validationResult, matchedData } = require('express-validator');

const router = express.Router();

router.get('/', (req, res) => {
  res.render('landing', {
  	data: {},
  	errors: {},
  });
});

router.post('/',[

	check('inputRNA')
	.isLength({min:1})
	.withMessage('There is a problem with your input')
	.trim(), //sanitizers

	check('email')
	.isEmail()
	.withMessage('That email does not look right')
	.bail() //sanitizers. 
	/*Bail stops if any previous check failed (to avoid 
	normalizing an empty email which returns "@") 
	*/
	.trim()
	.normalizeEmail()

	], (req, res) => {
		const errors = validationResult(req);
		res.render('landing', {
			data: req.body,
			errors: errors.mapped()
		});

		const data = matchedData(req);
		console.log('Sanitized', data);
	});


router.get('/documentation', (req, res) => {
  res.render('documentation');
});

router.get('/about', (req, res) => {
  res.render('about');
});

router.get('/downloads', (req, res) => {
  res.render('downloads');
});

router.get('/loading', (req, res) => {
	  //questa dovra' attendere fino alla fine della creazione dei risultati

  res.render('loading');
});

router.get('/results/:uid', (req, res) => {
		//questa dovra' gestire i contenuti creati dallo script

  res.render('results', {uid:req.params.uid});
});


module.exports = router;
