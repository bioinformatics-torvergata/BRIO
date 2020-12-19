const express = require('express');

const router = express.Router();

const fs = require('fs');


_check_completeness = function (uid) {
    //check Out.log, Sync, because otherwise there is a race for the output
    if (fs.existsSync("public/results/" + uid + "/Out.log")) {
        return fs.readFileSync("public/results/" + uid + "/Out.log", 'utf8');
    } else {
        return '0';
    }
}

router.get('/waiting',
    (req, res) => {
        if (!req.query.uid || req.query.uid.length !== 32) {
            res.render('landing',
                {
                    userID: req.body.uid,
                    inputRNA: {},
                    email: {},
                    inputRNA_processed: {},
                    inputBackground_processed: {},
                    errors: '',
                    progress: '0',
                });
        } else {
            let progress = _check_completeness(req.query.uid);
            if (progress === '100') {
                res.render('results',
                    {
                        uid: req.query.uid
                    });
            } else if (progress.length === 32) {
                res.render('results',
                    {
                        uid: progress
                    });
            } else {
                res.render('loading',
                    {
                        userID: req.query.uid,
                        progress: progress
                    });
            }
        }
    });

router.post('/waiting',
    (req, res) => {
        if (req.body.uid.length !== 32) {
            res.render('landing',
                {
                    userID: req.body.uid,
                    inputRNA: req.body.inputRNA,
                    email: req.body.email,
                    inputRNA_processed: {},
                    inputBackground_processed: {},
                    errors: '',
                    progress: '0',
                });
        } else {
            let progress = _check_completeness(req.body.uid);
            if (progress === '100') {
                res.render('results',
                    {
                        uid: req.body.uid
                    });
            } else if (progress.length === 32) {
                res.render('results',
                    {
                        uid: progress
                    });
            } else {
                res.render('loading',
                    {
                        userID: req.body.uid,
                        progress: progress
                    });
            }
        }
    });

module.exports = router;