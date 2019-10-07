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
  context.log('Start ItemRead');

  const id = req.params.id;
  if (id) {
      tableService.retrieveEntity(tableName, 'Partition', id, function (error, result, response) {
          if (!error) {
              context.res.status(200).json(response.body);
          }
          else {
              context.res.status(500).json({error : error});
          }
      });
  }
  else {
      // return the top 10 items
      var query = new azure.TableQuery().top(10);
      tableService.queryEntities(tableName, query, null, function (error, result, response) {
          if(!error){
              context.res.status(200).json(response.body.value);
          } else {
              context.res.status(500).json({error : error});
          }
      });
  }
};