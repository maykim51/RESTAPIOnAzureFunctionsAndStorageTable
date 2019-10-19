# Create CRUD with NodeJS, Azure Functions, Azure Table Storage
Azure Function을 이용해서 Azure Cosmos DB를 사용하는 기본 REST API 만들기! (NodeJS 사용)
참고 공식문서: [Azure Function, NodeJS를 사용한 기본 API(CRUD)만들기](https://docs.microsoft.com/en-us/azure/cosmos-db/table-storage-how-to-use-nodejs)



## 다루는 내용
1. Azure Functions, Azure Table Storage에 CRUD를 사용할 준비하기
2. REST API 만들기

## 사전 준비
* HTTP를 통한 Web-client간 기본 구동 지식
* Visual Studio Code
* 미리 만들어둔 Azure Functions 앱 프로젝트: [참고: VS Code에서 만들기](https://docs.microsoft.com/ko-kr/azure/azure-functions/functions-develop-vs-code?tabs=nodejs)
    * Azure Function에 대한 포스트는 별도로 업로드 예정이니 지금은 위의 링크 참조!
* Azure 계정, 구독




## 1.준비하기(Setup)
**1. NodeJS 설치**
* https://nodejs.org/en/download/ 접속 후 다운로드, 설치
* Cmd에서 [node -v] 쳐서 버전 나오면 설치완료 된 것


**2. Azure Functions App 설치**
* cmd에서 아래를 입력한다.
> npm install -s azure-storage\
> npm install -s uuid
* 필요한 경우 [VS Code용 Azure Functions 확장을 설치](https://docs.microsoft.com/ko-kr/azure/azure-functions/functions-create-first-function-vs-code)한다.


**3. 폴더 구조 만들기 Create CRUD folders**
* [VS Code용 Azure Functions extension으로 프로젝트 폴더를 만든다.](https://docs.microsoft.com/ko-kr/azure/azure-functions/functions-develop-vs-code?tabs=nodejs#create-an-azure-functions-project)
* 만들 폴더구조: ItemCreate / ItemRead / ItemUpdate / ItemDelete
* 프로젝트 폴더와 파일들이 생성되면 각 폴더 안 [function.json]파일 안에 사용할 HTTP를 반영한다. (= http crud api 구조를 갖춘다.)
    * CRUD -> HTTP methods: POST / GET / PUT / DELETE 
    * [참고] 그 외에 disabled, authLevel들을 바꾸어두었는데 꼭 필요한 작업은 아니라 설명 생략.

[ItemDelete 폴더의 function.json 샘플]
```
 {
  "disabled": false,
  "bindings": [
    {
      "authLevel": "anonymous",
      "type": "httpTrigger",
      "direction": "in",
      "name": "req",
      "methods": [
        "delete"
      ],
      "route": "items/{id}"
    },
    {
      "type": "http",
      "direction": "out",
      "name": "res"
    }
  ]
}
```

**4. Azure Cosmos DB Table API 계정(Azure Storage 계정)만들기**
* [Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)에 접속해서, Azure Storage 계정을 만든다.
또는
* 다음 사이트를 참조해서 Azure Portal에서 계정을 만든다.
    * [Table API 계정 만들기](https://docs.microsoft.com/en-us/azure/cosmos-db/create-table-dotnet#create-a-database-account)\
    ![001](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/001.png?raw=true)


**5. Function App에 Database 정보를 연결**
* 프로젝트 root 폴더에 .env 파일을 생성하고, CONNECTION STRING을 추가한다. (enronment variable)
    * CONNETION STRING은 Azure Portal Cosmos DB 리소스에서 조회할 수 있다
    * (참고) [Environment Variable을 추가하는 방법](https://medium.com/the-node-js-collection/making-your-node-js-work-everywhere-with-environment-variables-2da8cdf6e786) 참고
* [index.js]파일에 Azure Cosmos DB 연결을 추가한다
```
    //import package
    const storage = require('azure-storage');
    //connect to cosmos DB with connection string
    const connectionString = process.env.CONNECTION_STRING;
    //Create a table
    const tableSvc = storage.createTableService(connectionString);
```

**6. Table 생성하기(두가지 방법)**
* 방법 1\
    : 아래 코드를 삽입하여 테이블을 생성한다. 성공적으로 생성하면 result.created의 값이 true, 그렇지 않으면 false가 된다.
```
//create a table
const tableService = storage.createTableService(connectionString);
tableService.createTableIfNotExists('mytable', function(error, result, response){
    if(!error){
      // Table exists or created
    }
  });
const tableName = "mytable";
```

* 방법 2\
    * Azure Portal > 만들었던 Database Resource 화면에서 **Data Explorer** > **New Table** 선택
    ![002](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/002.png?raw=true)
    * Table ID를 입력하고, 테이블을 생성합니다.
    ![003](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/003.png?raw=true)
    ![004](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/004.png?raw=true)


**7. 테이블에 샘플 데이터 추가하기**
* 위에서 만든 테이블에서 **Entities** > **Add Entity** 선택
* PartitionKey와 RowKey 입력
    ![005](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/005.png?raw=true)
    ![006](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/006.png?raw=true)\

[참고] [Azure Table Storage에 적용할 Table Partition 방법](https://docs.microsoft.com/en-us/rest/api/storageservices/designing-a-scalable-partitioning-strategy-for-azure-table-storage)


**8. index.js파일에 endpoint 작업하기** 
* Item Update 폴더 안의 [function.json], [index.js]를 작업한다. (소스코드 참조)
* [ItemUpdate] 폴더의 [index.js] 샘플
```
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
```
* 같은 작업을 다른 CRUD에도 적용한다. (ItemCreate, ItemRead, ItemDelete)
* 완성된 소스코드는 [https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable) 참조!



## 2.REST API로 만들기

여기까지 만든 endpoint들을 REST API 스타일로로 만드는 작업.\
/items/{id} <- 이러한 URL endpoint를 만든다.

여기서 만들 http function(endpoint)는 아래와 같다. (\*표는 option임을 의미)
- \[POST\] http://localhost:7071/api/items
- \[DELETE\] http://localhost:7071/api/items/{id}
- \[GET\] http://localhost:7071/api/items/{*id}
- \[PUT\] \[POST\] http://localhost:7071/api/items/{id}


**1.아직 로그인 하지 않았다면, 작업중인 Visual Studio Code에서 Azure 계정으로 로그인한다.**
![007](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/007.png?raw=true)
미리 만들어둔 Function App이 없으면 이 단계에서 새로 생성해도 된다.\
이 예시에서는 'ms-food-fighter'라는 Function App에 만들어둔 Function들을 붙여넣었다.


**2. Azure Portal의 Azure Function 블레이드에서 설정하고, 반영된 설정을 로컬 소스파일에 적용한다.**
* [Azure Portal](https://portal.azure.com)에 접속한다
* *Integrate*을 선택한다.
  ![008](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/008.png?raw=true)
  * 만약 여기서 Azure Function이 'read-only'로 되어있으면 아래와 같은 문구가 보이는데, 
  ![009](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/009.png?raw=true)
  * 해결방법은 두 가지다.
    해결방법 1. 모드 변경.
    run-from-package 모드이기 때문에 발생하는 현상이다. 즉, 업로드된 ZIP에서 직접적으로 파일을 읽어오고 있기 때문에 편집할 수가 없는 모드인 것. 따라서 포털에서 WEBSITE_RUN_FROM_ZIP 또는 WEBSITE_RUN_FROM_PACKAGE 설정을 삭제해줘야 한다.
    아래 화면처럼 Visual Studio Code의 Azure 메뉴에서 해당 설정을 쉽게 삭제할 수 있다.
    ![013](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/013.png?raw=true)

    해결방법 2. 프록시 생성.
    로컬의 프로젝트에 proxies를 추가해주면 된다. 앱의 루트폴더(=host.json파일이 있는 곳]에 proxies.json 파일을 만들어주면 된다. [참조]( https://docs.microsoft.com/en-us/azure/azure-functions/functions-proxies)
* ItemCreate의 route template을 아래와 같이 적용하면,
  ![014](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/014.png?raw=true)
  function.json 파일에 적용된다.
  ![015](https://github.com/maykim51/Starter-AzureFunctions-AzureStorageTable/blob/master/images/015.png?raw=true)
 * function.json 내용을 복사해서 VS code 에서(로컬 소스파일) 다른 endpoint들의 function.json을 붙여넣기 한다. 

.... 작성 중.