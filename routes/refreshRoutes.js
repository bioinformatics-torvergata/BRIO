const express = require('express');

const router = express.Router();

var fs = require('fs');


_check_completeness = function(uid){
	//check Out.log, Sync, because otherwise there is a race for the output
	var contents = fs.readFileSync("results/"+uid+"/Out.log", 'utf8');
	return contents;
}

router.post('/waiting',
	(req,res) => {

		let progress = _check_completeness(req.body.uid);
		if (progress == '100'){
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