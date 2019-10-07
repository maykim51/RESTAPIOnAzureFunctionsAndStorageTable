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
  context.log('Start ItemDelete');

  const id = req.params.id;
  if (id) {
      var item = { PartitionKey: 'Partition', RowKey: id };
      tableService.deleteEntity(tableName, item, function (error, result, response) {
          if (!error) {
              context.res.status(204).send();
          }
          else {
              context.res.status(500).json({error : error});
          }
      });
  }
  else {
      context.res.status(404).send();
  }
};