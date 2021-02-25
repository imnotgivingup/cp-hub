const express = require('express');
const multer = require('multer');
const path = require('path');
const { exec } = require("child_process");
const session = require('express-session');
const app = express();
fs = require('fs');
const port = process.env.PORT || 3000;

//For forms
app.use(express.urlencoded({
	extended: true
}))


app.use(express.static(__dirname + '/public'));
app.use(session({
	secret: 'ssshhhhh',
	resave: true,
	saveUninitialized: true,
	cookie: { secure: false }
}));

//Setting up Multer storage object
const storage = multer.diskStorage({
	destination: function(req, file, cb) {
		cb(null, 'uploads_buffer/');
	},
	filename: function(req, file, cb) {
		cb(null, file.originalname);
	}
});

app.listen(port, () => console.log(`Listening on port ${port}...`));

//Root directory
app.get('/', (req, res) => {
	res.sendFile(path.join(__dirname + '/index.html'));
});

app.get('/login', (req, res) => {
	res.sendFile(path.join(__dirname + '/login.html'));
});


app.post('/', (req, res) => {
	var dat,fl=0;
	dat=fs.readFileSync('./uploads/teams.txt',{encoding: 'utf8',flag:'r'});
	dat=dat.split('\n');
	dat.forEach(tdat => {
		tdat=tdat.split(' ');
		if (tdat[1]==req.body.username){
		if(tdat[2]==req.body.password+'\r'){
			fl=1;
			}
		} 
		});
	if (fl){
		req.session.username=req.body.username;
		req.session.password=req.body.password;
		res.sendFile(path.join(__dirname + '/index.html'));
		}
	else res.send('Invalid login');
});

//POST for file upload
app.post('/upload-py', (req, res) => {
	let upload = multer({ storage: storage }).single('py');

	upload(req, res, function(err) {
	//If no file found
		if (!req.file) {
        		return res.send('Please select an image to upload');
        }
		else if (err instanceof multer.MulterError) {
			return res.send(err);
	}
	else if (err) {
		return res.send(err);
	}
	
	//Moving from buffer to main directory with new filename
	exec("MOVE uploads_buffer\\"+req.file.originalname+" uploads\\"+req.file.originalname.split('.').slice(0, -1).join('.') + '-' + Date.now() + path.extname(req.file.originalname), (error, stdout, stderr) => {
    	
	if (error) {
		console.log(`error: ${error.message}`);
        	return;
    	}
    	if (stderr) {
        	console.log(`stderr: ${stderr}`);
        	return;
	}
	res.send(`File uploaded <a href="./">Upload another file</a><p></p><a href="./submissions">Check submissions</a>`);
	});
});

app.get('/submissions',(req,res) => {
	var fin=[],ress=[],dispn=[],dispv=[],fl=0,tmp;

	fin=fs.readdirSync('./uploads');
	ress=fs.readdirSync('./results');

	fin.forEach(finfile => {
		//Flag to check if file has been evaluated
		fl=0
		ress.forEach(resfile => {
			if(finfile.substring(0,finfile.length-2)==resfile.substring(0,resfile.length-3))
				{
				fl=1;
				tmp=resfile;
				}
			});
		if(fl) {
			dispn.push(finfile);
			dispv.push(fs.readFileSync('./results/'+tmp,{encoding:'utf8', flag:'r'}));
			}
		else {
			dispn.push(finfile);
			dispv.push('Pending eval');
			}
		});
	//Sample html table
	let text="<table style=\"width:100%\"><tr><th>Name</th><th>Status</th></tr>";
	
	//Filling the rows of the table
	for(i=0;i<dispn.length;i++){
		text+="<tr>"+"<td>"+dispn[i]+"</td>"+"<td>"+dispv[i]+"</td>"+"</tr>"
		}

	text+="</table>";
	res.send(text);
	});
	
});