// Require express module
const express = require('express');

// Require useful stuff
const router = express.Router();


// Require controller modules
var input_validation_controller = require('../controllers/inputValidationController')
//var ciccia_controller = require('../controllers/cicciaController')
//var output_controller = require('../controllers/outputController')


// shortest nuc 3
// shortest str 11
const MIN_LEN_RNA_SEQ = 3


const { check, validationResult, matchedData } = require('express-validator');
const spawn = require("child_process").spawn;


// if there is a file, then ...
//     //check file
// else
//     check input_form
//	   
//	   if sequence --> check regular expression like [ACGUTacgut]+ and min length is the min motif length

//	   if sequence + structure --> check regular expression like [ACGUTacgut]+ and [\(\)\.]+
//	   if structure --> error, the sequence is mandatory with the structure


//check email: IS IT MANDATORY? MAYBE ONLY WITH FILE?

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
	.trim()
	.escape()	// It removes HTML characters (ToDo: MAYBE IT IS PROBLEMATIC FOR THE STRUCTURE ALPHABET)
	.isLength({ min: MIN_LEN_RNA_SEQ })
	.withMessage('The RNA has to be at least ' + MIN_LEN_RNA_SEQ + ' ribonucleotides.')
	//.matches([ACGUTacgut]+) 	// ToDo: we need a regular expression+
	.isAlpha()
	.withMessage('The RNA has to contain only valid ribonucleotides.'),


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
