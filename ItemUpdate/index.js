//reads .env file and sets the environment variables.
const dotenv = require('dotenv');
dotenv.config();
console.log(process.env.CONNECTION_STRING);


//import Azure Storage SDK
const storage = require('azure-storage');
//connect to cosmos DB with connection string
const connectionString = process.env.CONNECTION_STRING;


//create a table
const tableSvc = storage.createTableService(connectionString);
tableSvc.createTableIfNotExists('mytable', function(error, result, response){
    if(!error){
      // Table exists or created
    }
  });