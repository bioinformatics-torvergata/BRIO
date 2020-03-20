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


const { body, validationResult, matchedData } = require('express-validator');
const spawn = require("child_process").spawn;


// if there is a file, then ...
//     input_sequences <- file
// else
//     input_sequences <- textbox

// each element in input_sequence.split('>'):
// - len(element) == 2 or 3 (header + seq or header + seq + struct)
// - element[1] --> check length >= MIN_LEN_RNA_SEQ and regular expression like [ACGUTacgut]+ 
// - if exists element[2] --> len(element[2]) == len(element[1]) and regular expression like [\(\)\.]+
// at least 1 valid element

// response code 303 (See Other)

//POST request from input form
/*
	validation - in test
	sanitization - in test
	run scripts - in test
	get to loading
	return output
*/

MAX_INPUT_SIZE = 50000 // bytes/characters

const reg_exp_rna_molecule = new RegExp('^[ACGUTacgut]+$');
const reg_exp_rna_secondary_structure = new RegExp('^[\(\)\.]+$');

var valid_rnas_str = ''

check_rna_sequences = function(value, {req}) {
	if (value.length > MAX_INPUT_SIZE){
		throw new Error('Input too big (' + value.length + ' characters, but the max is ' + MAX_INPUT_SIZE + ')');
	}

	valid_rnas_str = ''
	var not_valid_inputs_str = ''
	var not_valid_rna_molecules_str = ''
	var not_valid_secondary_structures_str = ''

	value.replace(/^>/, '').split('>').forEach(function(header_seq_struct) {
		console.log('----')
		header_seq_struct_list = header_seq_struct.replace(/\n$/, '').split('\n').map(function(val, index){
			return val.replace(/\r$/, '')
		})

		//console.log(header_seq_struct_list)
		//console.log(rna_molecule.test(header_seq_struct_list[1]) + ' - ' + header_seq_struct_list[1])

		if (header_seq_struct_list.length != 2 && header_seq_struct_list.length != 3){
			not_valid_inputs_str +=  '>' + header_seq_struct
			return
		}

		if (!reg_exp_rna_molecule.test(header_seq_struct_list[1])){
			not_valid_rna_molecules_str += '>' + header_seq_struct
			return
		}

		if (header_seq_struct_list.length == 3){
			if (header_seq_struct_list[1].length != header_seq_struct_list[2].length){
				not_valid_secondary_structures_str += '>' + header_seq_struct
				return
			}

			if (!reg_exp_rna_secondary_structure.test(header_seq_struct_list[2])){
				not_valid_secondary_structures_str += '>' + header_seq_struct
				return
			}

			//-------------------------------
			// secondary structure validation
			// ToDo: to improve
			var count = 0
			for (var i = 0; i < header_seq_struct_list[2].length; i++) {
				console.log('count: ' + count)
				if (header_seq_struct_list[2][i] == '('){
					count += 1
				}else if(header_seq_struct_list[2][i] == ')'){
					if (co)
					count -= 1
				}
				if (count < 0){
					break
				}
			}
			//-------------------------------
			
			if (count != 0){
				not_valid_secondary_structures_str += '>' + header_seq_struct
				return
			}
		}

		valid_rnas_str +=  '>' + header_seq_struct
	});

	//console.log('valid_rnas_str:\n' + valid_rnas_str);
	//console.log('not_valid_inputs_str:\n' + not_valid_inputs_str);
	//console.log('not_valid_rna_molecules_str:\n' + not_valid_rna_molecules_str);
	//console.log('not_valid_secondary_structures_str:\n' + not_valid_secondary_structures_str);

	xxx_str = not_valid_inputs_str + not_valid_rna_molecules_str + not_valid_secondary_structures_str
	if (xxx_str == ''){
		return true;
	}else{
		throw new Error('Input sequences are not valid');
	}
};

router.post('/fileInput',
	body('inputRNA', 'The RNA is not valid')
		.custom(check_rna_sequences),
	input_validation_controller.check_email(),

	(req, res) => {
		const errors = validationResult(req);

		if (!errors.isEmpty()){
			res.render('landing', {
				data: req.body,
				errors: errors.mapped()
			});

		}else{ //se non ci sono errori
			console.log(valid_rnas_str)

			res.render('loading',{
				data: '',
				errors: '',
			});
		}
	}
)

router.post('/fileInput2',[

	body('inputRNA')
	.trim()
	.escape()	// It removes HTML characters (ToDo: MAYBE IT IS PROBLEMATIC FOR THE STRUCTURE ALPHABET)
	.isLength({ min: MIN_LEN_RNA_SEQ })
	.withMessage('The RNA has to be at least ' + MIN_LEN_RNA_SEQ + ' ribonucleotides.')
	//.matches([ACGUTacgut]+) 	// ToDo: we need a regular expression+
	.isAlpha()
	.withMessage('The RNA has to contain only valid ribonucleotides.'),


	body('email')
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

router.post('/fileInput2',[

	body('email')
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
