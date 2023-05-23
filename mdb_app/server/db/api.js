// import dotenv from 'dotenv';
// import axios from 'axios';
import './loadEnv.js';

var axios = require('axios');
var data = JSON.stringify({
    "collection": "listingsAndReviews",
    "database": "sample_airbnb",
    "dataSource": "Cluster0",
    "projection": {
        "_id": 1
    }
});

var config = {
    method: "post",
    url: "https://eastus2.azure.data.mongodb-api.com/app/data-pdctr/endpoint/data/v1/action/findOne",
    headers: {
        'Content-Type': 'application/json',
        'Access-Control-Request-Headers': '*',
        'api-key': process.env.DATA_API_KEY || "",
		'Accept': 'application/ejson'
    },
	data: data
};

axios(config)
	.then(function(response){
		console.log(JSON.stringify(response.data))
	})
	.catch(function (error){
		console.log(error)
	});

/* 	axios(config)
	.then((response) => {
		console.log(JSON.stringify(response.data))
	})
	.catch((error) => {
		console.error(error)
	}); */
