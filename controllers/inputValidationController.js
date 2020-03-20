const { body } = require('express-validator');

// check email on POST.
exports.check_email = function(req, res) {
	return body('email', 'The email does not look right.')
		.optional({ checkFalsy: true })
		.isEmail()
};

// check RNA sequence on POST.
exports.check_rna_sequence = function(req, res) {

    
    res.send('NOT IMPLEMENTED: check_rna_sequence POST');
};

// check RNA secondary structure on POST.
exports.check_rna_secondary_structure = function(req, res) {
    res.send('NOT IMPLEMENTED: check_rna_secondary_structure POST');
};