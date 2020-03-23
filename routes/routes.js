//routes.js

const express = require('express');

const router = express.Router();

router.get('/', (req, res) => {
  res.render('landing', {
    inputRNA: '',
    email: '',
    valid_rnas: '',
    not_valid_inputs: '',
    not_valid_rna_molecules: '',
    not_valid_secondary_structures: '',
    errors: {},
  });
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
