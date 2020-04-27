const express = require('express');

const router = express.Router();

_check_completeness = function(uid){
	//check Out.log
	return '25';
}

router.post('/waiting',
	(req,res) => {

		let progress = _check_completeness(req.body.uid);
		if (progress == '1'){
			res.render('results', 
				{
					uid:req.body.uid
				});
		}else{
			res.render('loading',
				{
				userID : req.body.uid,
				progress : progress 
				});
		}


	});

module.exports = router;