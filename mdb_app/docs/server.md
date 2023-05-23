# Notes for backend authentication

```js
// ## Route definitions
app.METHOD(PATH, HANDLER)
app is an express instance.
METHOD is an HTTP request method, in lowercase.
PATH is a path on the server.
HANDLER is the function to be executed when the route is matched.

const express = require('express');
const app, app2, app3 = express()

// ex. 2
app.get('/user/:uid/photos/:file', function(req, res){
  var uid = req.params.uid
    , file = req.params.file;

  req.user.mayViewFilesFrom(uid, function(yes){
    if (yes) {
      res.sendFile('/uploads/' + uid + '/' + file);
    } else {
      res.send(403, 'Sorry! you cant see that.');
    }
  });
});

app2.get('/client', (req, res) => {
 req.file
 res.send({ some: 'json' });
 res.send('<p>some html</p>');
 res.status(404).send('Sorry, cant find that');
})

// Listen for connections. \
// A node http.Server is returned, w/ this app (which is a func) as its callback.

// express = require('express'), app = express();
var http = require('http'), https = require('https')
http.createServer(app).listen(80); https.createServer({ ... }, app).listen(443);

// Parameter mapping is used to provide pre-conditions to routes which use normalized placeholders. For example a :user_id parameter could automatically load a user's information from the database without any additional code

app3.param('user_id', function(req, res, next, id){
User.find(id, function(err, user){
 if (err) {
 next(err);
 } else if (user) {
 req.user = user;
 next();
 } else {
 next(new Error('failed to load user'));
 }
});
});

const cors = require('cors')

app.get('/', (req, res) => {
 res.send('temp data')
});

app.post('/', (req, res) => {
 res.setDefaultEncoding('POST req to homepage')
})

app.post('/callback', (req, res) => {
 res.send('POST req to callback URI')
})
 ```
