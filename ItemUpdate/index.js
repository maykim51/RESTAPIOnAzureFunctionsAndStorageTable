//reads .env file and sets the environment variables.
const dotenv = require('dotenv');
dotenv.config();

//import Azure Storage SDK
const storage = require('azure-storage');
//connect to cosmos DB with connection string
const connectionString = process.env.CONNECTION_STRING;
console.log(connectionString)


//create a table
const tableService = storage.createTableService(connectionString);
tableService.createTableIfNotExists('mytable', function (error, result, response) {
  if (!error) {
    // Table exists or created
  }
});
const tableName = "mytable";

module.exports = async function (context, req) {
  context.log('Start ItemUpdate');

  if (req.body) {
    const item = req.body;

    item.Rowkey = id;

    tableService.replaceEntity(tableName, item, function (error, result, response) {
      if (!error) {
        context.res.status(202).json(result);
      } else {
        context.res.status(500).json({ error: error });
      }
    });
  }
  else {
    context.res = {
      status: 400,
      body: "Please pass an item in the request body"
    };
    context.done();
  }
};