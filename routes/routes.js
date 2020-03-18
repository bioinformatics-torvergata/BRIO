//routes.js

const express = require('express');
const spawn = require("child_process").spawn;

const { check, validationResult, matchedData } = require('express-validator');

const router = express.Router();

router.get('/', (req, res) => {
  res.render('landing', {
  	data: {},
  	errors: {},
  });
});

//POST request from input form
/*
	validation - in test
	sanitization - in test
	run scripts - in test
	get to loading
	return output
*/
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

		//python script
		//per come e' attualmente lo lancia comunque, 
		//come si controlla se c'è un errore in maniera corretta?

		const pythonProcess = spawn('python',["scripts/python.py", 
			"abcdeFgH1", 
			"fileProva.txt"
			]);

		pythonProcess.stdout.on('data',(data) => {
			console.log('stdout: ' + data); //test stream python -> node
		});
		pythonProcess.stderr.on('data',(data) => {
			console.error('stderr: ' + data); //test stream python -> node
		});
		pythonProcess.on('close', (code, signal) => {
			console.log('process exited with code: '+code +
			'\nsignal: ' + signal);
		})

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
