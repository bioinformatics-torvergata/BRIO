const { body } = require('express-validator');

const reg_exp_rna_molecule = new RegExp('^[ACGUTacgut]+$')
const reg_exp_rna_secondary_structure = new RegExp('^[\(\)\.]+$');

exports.check_email_handler = function(req, res) {
	return body('email', 'The email does not look right.')
		.optional({ checkFalsy: true })
		.isEmail()
};


exports.check_rna_sequence = function(rna_seq) {
	return reg_exp_rna_molecule.test(rna_seq)
};

exports.check_rna_secondary_structure = function(rna_struct) {
	if(reg_exp_rna_secondary_structure.test(rna_struct)){
		let count = 0;
		for (let i = 0; i < rna_struct.length; i++) {
			if (rna_struct[i] === '('){
				count += 1
			}else if(rna_struct[i] === ')'){
				count -= 1
			}
			if (count < 0){
				break
			}
		}

		return count === 0
	}

	return false
};