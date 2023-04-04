import { MongoClient } from "mongodb";

const connStr = process.env.ATLAS_URI || '';

const client = new MongoClient(connStr);

let conn;
try {
	conn = await client.connect();
}	catch(e) {
	console.error(e);
}

let db = conn.db("sample_airbnb");

export default db;
