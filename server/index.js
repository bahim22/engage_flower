const express = require('express');
const app = express()
// const cors = require('cors')

app.get('/', (req, res) => {
	res.send('temp data')
});

app.post('/', (req, res) => {
	res.setDefaultEncoding('POST req to homepage')
})

app.post('/callback', (req, res) => {
	res.send('POST req to callback URI')
})
