// Require modules
const express = require('express');

var input_validation_controller = require('../controllers/inputValidationController')
//var ciccia_controller = require('../controllers/cicciaController')
//var output_controller = require('../controllers/outputController')

// Useful stuff
const router = express.Router();

// shortest RNA sequence in the dataset: 3 nt
// shortest RNA structure in the dataset: 11 nt
const MIN_LEN_RNA_SEQ = 3
const MAX_INPUT_SIZE = 50000 // bytes/characters

const { body, validationResult, matchedData } = require('express-validator');
const spawn = require("child_process").spawn;

var valid_rnas_str = ''
var not_valid_inputs_str = ''
var not_valid_rna_molecules_str = ''
var not_valid_secondary_structures_str = ''

var valid_rnas_background_str = ''
var not_valid_inputs_background_str = ''
var not_valid_rna_molecules_background_str = ''
var not_valid_secondary_structures_background_str = ''

_check_rna_sequences = function(input_rna_sequences_str, input_name_str) {
	var valid_rnas_xxx_str = ''
	var not_valid_inputs_xxx_str = ''
	var not_valid_rna_molecules_xxx_str = ''
	var not_valid_secondary_structures_xxx_str = ''

	if (input_rna_sequences_str.replace(/^>/, '').length == 0){
		throw new Error(input_name_str + ' is empty.');
	}
	if (input_rna_sequences_str.length > MAX_INPUT_SIZE){
		throw new Error(input_name_str + ' is too big (' + input_rna_sequences_str.length + ' characters, but the max is ' + MAX_INPUT_SIZE + ')');
	}

	// The '>' symbol will be re-added for each input RNA
	input_rna_sequences_str.replace(/^>/, '').split('>').forEach(function(header_seq_struct) {
		header_seq_struct_list = header_seq_struct.replace(/\n$/, '').split('\n').map(function(val, index){
			return val.replace(/\r$/, '')
		})

		// (header + rna_seq) or (header + rna_seq + rna_sec_struct)
		if (header_seq_struct_list.length != 2 && header_seq_struct_list.length != 3){
			not_valid_inputs_xxx_str +=  '>' + header_seq_struct
			return
		}

		if (
			!input_validation_controller.check_rna_sequence(header_seq_struct_list[1]) ||
			header_seq_struct_list[1].length < MIN_LEN_RNA_SEQ
		){
			not_valid_rna_molecules_xxx_str += '>' + header_seq_struct
			return
		}

		// if (header + rna_seq + rna_sec_struct)
		if (header_seq_struct_list.length == 3){
			// if length(rna_seq) != length(rna_sec_struct)
			if (header_seq_struct_list[1].length != header_seq_struct_list[2].length){
				not_valid_secondary_structures_xxx_str += '>' + header_seq_struct
				return
			}

			if (!input_validation_controller.check_rna_secondary_structure(header_seq_struct_list[2])){
				not_valid_secondary_structures_xxx_str += '>' + header_seq_struct
				return
			}
		}

		valid_rnas_xxx_str +=  '>' + header_seq_struct
	});
	
	return [valid_rnas_xxx_str, not_valid_inputs_xxx_str, not_valid_rna_molecules_xxx_str, not_valid_secondary_structures_xxx_str]
};

check_user_input_handler = function(value, {req}) {
	[valid_rnas_str, not_valid_inputs_str, not_valid_rna_molecules_str, not_valid_secondary_structures_str] = _check_rna_sequences(
		req.files && req.files.fileRNA ? req.files.fileRNA.data.toString('utf8') : value, 'Input' + (req.files && req.files.fileRNA ? ' file' : '')
	)

	const not_valid_rnas_str = not_valid_inputs_str + not_valid_rna_molecules_str + not_valid_secondary_structures_str
	if (not_valid_rnas_str == ''){
		return true
	}else{
		throw new Error(not_valid_rnas_str.replace(/^>/, '').split('>').length + ' invalid RNA molecule(s) in the input' + (req.files && req.files.fileRNA ? ' file.' : '.'));
	}
}

check_user_background_handler = function(value, {req}) {
	[valid_rnas_background_str, not_valid_inputs_background_str, not_valid_rna_molecules_background_str, not_valid_secondary_structures_background_str] = ['', '', '' , '']
	if (req.files && req.files.fileBackground){
		[valid_rnas_background_str, not_valid_inputs_background_str, not_valid_rna_molecules_background_str, not_valid_secondary_structures_background_str] = _check_rna_sequences(
			req.files.fileBackground.data.toString('utf8'), 'Background'
		)

		const not_valid_rnas_background_str = not_valid_inputs_background_str + not_valid_rna_molecules_background_str + not_valid_secondary_structures_background_str
		if (not_valid_rnas_background_str == ''){
			return true
		}else{
			throw new Error(not_valid_rnas_background_str.replace(/^>/, '').split('>').length + ' invalid RNA molecule(s) in the background file.');
		}
	}else{
		return true
	}
}

router.post('/fileInput',
	body('inputRNA').trim().custom(check_user_input_handler),
	body('fileBackground').custom(check_user_background_handler),
	input_validation_controller.check_email_handler(),
	(req, res) => {
		/*
		//Decide where to put business logic (cicciaController?
		const pythonProcess = spawn('python', ["scripts/python.py", 
			"folderProvaText", 
			"fileTextProva.txt"
		]);
		*/

		const pythonProcess = spawn('python', ["scripts/_completeWithDotBracketAndBEAR.py", 
			valid_rnas_str, 
		]);
		pythonProcess.stdout.on('data',(data) => {
			console.log('stdout:\n' + data); //test stream python -> node
		});
		/*pythonProcess.stderr.on('data',(data) => {
			console.error('stderr: ' + data); //test stream python -> node
		});
		pythonProcess.on('close', (code, signal) => {
			console.log('scripts/_completeWithDotBracketAndBEAR.py exited with code: '+code +
			'\nsignal: ' + signal);
		})*/
		

		const errors = validationResult(req);

		res.render(errors.isEmpty() ? 'loading' : 'landing',
		{
			inputRNA: req.body.inputRNA,
			email: req.body.email,
			inputRNA_processed: {
				'valid_rnas': valid_rnas_str,
				'not_valid_inputs': not_valid_inputs_str,
				'not_valid_rna_molecules': not_valid_rna_molecules_str,
				'not_valid_secondary_structures': not_valid_secondary_structures_str
			},
			inputBackground_processed: {
				'valid_rnas': valid_rnas_background_str,
				'not_valid_inputs': not_valid_inputs_background_str,
				'not_valid_rna_molecules': not_valid_rna_molecules_background_str,
				'not_valid_secondary_structures': not_valid_secondary_structures_background_str
			},
			errors: errors.mapped(),
		});
	}
)

// Take useful stuff and remove
/*

body('inputRNA')
.trim()
.escape()
.isLength({ min: MIN_LEN_RNA_SEQ })
.withMessage('The RNA has to be at least ' + MIN_LEN_RNA_SEQ + ' ribonucleotides.')
//.matches([ACGUTacgut]+) 	// ToDo: we need a regular expression+
.isAlpha()
.withMessage('The RNA has to contain only valid ribonucleotides.')


body('email')
.isEmail()
.withMessage('That email does not look right')
.bail() //sanitizers. 
//Bail stops if any previous check failed (to avoid 
//normalizing an empty email which returns "@") 

.trim()
.normalizeEmail()

(req, res) => {
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
	}

	const data = matchedData(req);
	console.log('Sanitized', data);
}
*/

module.exports = router;