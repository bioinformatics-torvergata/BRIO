// Require modules
const express = require('express');
const crypto = require("crypto");

var input_validation_controller = require('../controllers/inputValidationController')
//var ciccia_controller = require('../controllers/cicciaController')
//var output_controller = require('../controllers/outputController')

// Useful stuff
const router = express.Router();

// shortest RNA sequence in the dataset: 3 nt
// shortest RNA structure in the dataset: 11 nt
const MIN_LEN_RNA_SEQ = 3
const MAX_LEN_RNA_SEQ = 3000
const MAX_INPUT_SIZE = 50000 // bytes/characters

const {body, validationResult, matchedData} = require('express-validator');
const spawn = require("child_process").spawn;

let valid_rnas_str = '';
let not_valid_inputs_str = ''
let not_valid_rna_molecules_str = ''
let not_valid_secondary_structures_str = ''

let valid_rnas_background_str = ''
let not_valid_inputs_background_str = ''
let not_valid_rna_molecules_background_str = ''
let not_valid_secondary_structures_background_str = ''


_are_nums_consecutives = function (num_list) {
    let i;
    for (i = 0; i < num_list.length - 1; i++) {
        if (num_list[i + 1] - num_list[i] !== 1) {
            return false
        }
    }
    return true
}

_check_rna_sequences = function (input_rna_sequences_str, input_name_str) {
    let valid_rnas_xxx_str = '';
    let not_valid_inputs_xxx_str = '';
    let not_valid_rna_molecules_xxx_str = '';
    let not_valid_secondary_structures_xxx_str = '';

    if (input_rna_sequences_str.replace(/^>/, '').length === 0) {
        throw new Error(input_name_str + ' is empty.');
    }
    if (input_rna_sequences_str.length > MAX_INPUT_SIZE) {
        throw new Error(input_name_str + ' is too big (' + input_rna_sequences_str.length + ' characters, but the max is ' + MAX_INPUT_SIZE + ')');
    }

    // The '>' symbol will be re-added for each input RNA
    input_rna_sequences_str.replace(/^>/, '').split('>').forEach(function (header_seq_struct) {
        let header_seq_struct_list = header_seq_struct.replace(/\n$/, '').split('\n').map(function (val, index) {
            return val.replace(/\r$/, '')
        })

        let num_row = 1
        let rna_molecule = ''
        let valid_rna_row_list = []
        let dot_bracket = ''
        let putative_sec_str_row_list = []
        for (let row of header_seq_struct_list.slice(1)) {
            if (input_validation_controller.check_rna_sequence(row)) {
                valid_rna_row_list.push(num_row)
                rna_molecule += row
            } else {
                putative_sec_str_row_list.push(num_row)
                dot_bracket += row
            }

            num_row += 1
        }

        // (header + rna_seq) or (header + rna_seq + rna_sec_struct)
        if ((valid_rna_row_list.length + putative_sec_str_row_list.length) !== header_seq_struct_list.length - 1) {
            not_valid_inputs_xxx_str += '>' + header_seq_struct
            return
        }

        if (
            (valid_rna_row_list.length === 0) ||
            !_are_nums_consecutives(valid_rna_row_list) ||
            rna_molecule.length < MIN_LEN_RNA_SEQ || rna_molecule.length > MAX_LEN_RNA_SEQ
        ) {
            not_valid_rna_molecules_xxx_str += '>' + header_seq_struct
            return
        }

        if (
            putative_sec_str_row_list.length > 0 && (
                !_are_nums_consecutives(putative_sec_str_row_list) ||
                !input_validation_controller.check_rna_secondary_structure(dot_bracket)
            )
        ) {
            not_valid_secondary_structures_xxx_str += '>' + header_seq_struct
            return
        }

        let processed_entry = '>' + header_seq_struct_list[0] + '\n' + rna_molecule + '\n'
        if (putative_sec_str_row_list.length > 0) {
            processed_entry += dot_bracket + '\n'
        }

        valid_rnas_xxx_str += processed_entry
    });

    return [valid_rnas_xxx_str, not_valid_inputs_xxx_str, not_valid_rna_molecules_xxx_str, not_valid_secondary_structures_xxx_str]
};

check_user_input_handler = function (value, {req}) {
    [valid_rnas_str, not_valid_inputs_str, not_valid_rna_molecules_str, not_valid_secondary_structures_str] = _check_rna_sequences(
        req.files && req.files.fileRNA ?
            req.files.fileRNA.data.toString('utf8') :
            value, 'Input' + (req.files && req.files.fileRNA ? ' file' : '')
    )

    const not_valid_rnas_str = not_valid_inputs_str + not_valid_rna_molecules_str + not_valid_secondary_structures_str

    if (not_valid_rnas_str === '') {
        return true
    } else {
        throw new Error(
            not_valid_rnas_str.replace(/^>/, '').split('>').length +
            ' invalid RNA molecule(s) in the input' + (req.files && req.files.fileRNA ? ' file.' : '.')
        );
    }
}

check_user_background_handler = function (value, {req}) {
    [valid_rnas_background_str, not_valid_inputs_background_str, not_valid_rna_molecules_background_str, not_valid_secondary_structures_background_str] = ['', '', '', '']
    if (req.files && req.files.fileBackground) {
        [valid_rnas_background_str, not_valid_inputs_background_str, not_valid_rna_molecules_background_str, not_valid_secondary_structures_background_str] = _check_rna_sequences(
            req.files.fileBackground.data.toString('utf8'), 'Background'
        )

        const not_valid_rnas_background_str = not_valid_inputs_background_str + not_valid_rna_molecules_background_str + not_valid_secondary_structures_background_str
        if (not_valid_rnas_background_str === '') {
            return true
        } else {
            throw new Error(
                not_valid_rnas_background_str.replace(/^>/, '').split('>').length +
                ' invalid RNA molecule(s) in the background file.');
        }
    } else {
        return true
    }
}

router.post('/fileInput',
    body('inputRNA').trim().custom(check_user_input_handler),
    body('fileBackground').custom(check_user_background_handler),
    input_validation_controller.check_email_handler(),
    (req, res) => {
        const errors = validationResult(req);

        if (req.body.options_species == null) {
            req.body.options_species = '.'
        }
        if (req.body.options_experiments == null) {
            req.body.options_experiments = '.'
        }

        let userID = ''
        let page_to_go;
        if (errors.isEmpty()) {
            page_to_go = 'loading'

            userID = crypto.randomBytes(16).toString("hex");
            console.log('user run ID: ' + userID);

            const pythonProcess = spawn('python3', ["scripts/_completeWithDotBracketAndBEAR.py",
                valid_rnas_str, valid_rnas_background_str, userID, req.body.options_species, req.body.options_experiments
            ]);
            pythonProcess.stdout.on('data', (data) => {
                console.log('stdout:\n' + data); //test stream python -> node
            });
            pythonProcess.stderr.on('data', (data) => {
                console.error('stderr: ' + data); //test stream python -> node
            });
            pythonProcess.on('close', (code, signal) => {
                console.log('scripts/_completeWithDotBracketAndBEAR.py exited with code: ' + code + '\nsignal: ' + signal);
            })
        } else {
            page_to_go = 'landing'
        }

        res.render(page_to_go,
            {
                userID: userID,
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
                progress: '0',
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