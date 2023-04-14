import express from 'express';
import db from '../db/conn.js';
import { ObjectId } from 'mongodb';

const router = express.Router();

// get list of 22 posts
router.get('/', async (req, res) => {
	let collection = await db.collection('posts');
	let results = await collection.find({}).limit(22).toArray();

	res.send(results).status(200);
});

	/*
	  (method) Db.collection<Document>(name: string, options?: CollectionOptions | undefined): Collection<Document>
	ret a ref to a DB coll. || !exists: implicitly created
	@param name — the collection name we wish to access.
	@returns — return the new Collection instance
	*/
// *! fetch latest posts
router.get('/latest', async (req, res) => {
	let collection = await db.collection('posts');
	// Execute an aggregation framework pipeline against the coll
	// An array of aggregation pipelines to execute
	let results = await collection
		.aggregate([
			{ $project: { author: 1, title: 1, tags: 1, date: 1 } },
			{ $sort: { date: -1 } },
			{ $limit: 3 },
			//Returns an array of docs. Promise<Document[]>
			// Must ensure memory >= req to store results
		])
		.toArray();
	res.send(results).status(200);
});

// GET single post
router.get("/:id", async (req, res) => {
	let collection = await db.collection("posts")
	// A class representation of the BSON ObjectId type.
	let query = {_id: ObjectId(req.params.id)}
	let result = await collection.findOne(query)
	// find the first doc that matches query
	// @param filter - query for find ops
})
