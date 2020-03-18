//routes.js

const express = require('express');

const spawn = require("child_process").spawn;

const { check, validationResult, matchedData } = require('express-validator');

const router = express.Router();

//POST request from input form
/*
	validation - in test
	sanitization - in test
	run scripts - in test
	get to loading
	return output
*/
router.post('/textInput',[

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

		if (!errors.isEmpty()){
			res.render('landing', {
				data: req.body,
				errors: errors.mapped()
			});

		}else{ //se non ci sono errori

			res.render('loading',{
				data: '',
				errors: '',
			});

		//python script
			const pythonProcess = spawn('python',["scripts/python.py", 
				"folderProvaText", 
				"fileTextProva.txt"
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
		}

		const data = matchedData(req);
		console.log('Sanitized', data);
	});

router.post('/fileInput',[

	//check file

	//check email
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

	//callback della post
	
		const errors = validationResult(req);
		if (!errors.isEmpty()) {
			res.render('landing', {
				data: req.body,
				errors: errors.mapped()
			});

		}else{ //se non ci sono errori

			res.render('loading',{
				data: '',
				errors: '',
			});

		//python script
			const pythonProcess = spawn('python',["scripts/python.py", 
				"folderProvaUpload", 
				"fileuploadedProva.txt"
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
		}

		const data = matchedData(req);
		console.log('Sanitized', data);
	});

module.exports = router;
