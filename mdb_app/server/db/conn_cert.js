// !* Ex. 1
const { MongoClient, ServerApiVersion } = require('mongodb');

const uri = process.env.ATLAS_URI || '';

const clientA = new MongoClient(uri, { useNewUrlParser: true, useUnifiedTopology: true, serverApi: ServerApiVersion.v1 });
client.connect(err => {
  const collection = clientA.db("test").collection("devices");
  // perform actions on the collection object
  clientA.close();
});

// !* Example 2

const { MongoClient, ServerApiVersion } = require('mongodb');
const fs = require('fs');

// <path_to_certificate>
const credentials = 'D:/Downloads_Vol2/X509-cert-8384835665760269109.pem'

const client = new MongoClient(process.env.MDB_URI, {
  sslKey: credentials,
  sslCert: credentials,
  serverApi: ServerApiVersion.v1
});

async function run() {
  try {
    await client.connect();
    const database = client.db("testDB");
    const collection = database.collection("testCol");
    const docCount = await collection.countDocuments({});
    console.log(docCount);
    // perform actions using client
  } finally {
    // Ensures that the client will close when you finish/error
    await client.close();
  }
}

run().catch(console.dir);

// prac 2
import { MongoClient } from 'mongodb';
import fs from 'fs' // || fs/promises

// Enable command monitoring for debugging
const clientB = new MongoClient('mongodb://localhost:27017', { monitorCommands: true });

clientB.on('commandStarted', started => console.log(started));
clientB.db().collection('pets');
await clientB.insertOne({ name: 'spot', kind: 'dog' });
