const express = require('express');

const router = express.Router();

const fs = require('fs');


_check_completeness = function(uid){
	//check Out.log, Sync, because otherwise there is a race for the output
	if (fs.existsSync("results/"+uid+"/Out.log")) {
		return fs.readFileSync("results/" + uid + "/Out.log", 'utf8');
	}else{
		return '0';
	}
}

router.post('/waiting',
	(req,res) => {

		let progress = _check_completeness(req.body.uid);
		if (progress === '100'){
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