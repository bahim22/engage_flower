const { MongoClient } = require('mongodb');

const uri = process.env.ATLAS_URI || "";

const client = new MongoClient(uri);

async function run() {
	try {
		const database = client.db('sample_mflix');
		// The name of the database we want to use
		const movies = database.collection('movies');
		// the collection name we wish to access.

		const query = { title: "Back to the Future" };
		const movie = await movies.findOne(query);

		console.log(movie);
	}	finally {
		await client.close();
	}
}
run().catch(console.dir);
