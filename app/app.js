var express = require('express');
var app = express();

var morgan = require('morgan');
app.use(morgan('short'));

var bodyParser = require('body-parser');
app.use(bodyParser.urlencoded({ extended:false }));

app.use(express.static(__dirname + '/public'));


app.listen(8000, 'localhost', function() {
    console.log('Server running at http://localhost:8000/');
});
