import express from 'express';
import cors from 'cors';
import './loadEnv.js';
import 'express-async-errors';
import posts from './routes/posts.js'

const PORT = process.env.PORT;
const app = express();

app.use(cors());
app.use(express.json());

app.use('/posts', posts);

app.use((err, _req, res, next) => {
	res.status(500).send('An error has occured.')
})

app.listen(PORT, () => {
	console.log(`Server running on port: ${PORT}`)
})
