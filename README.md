#WIP... (작업중)

# TIL Rep.: Create CRUD with NodeJS, Azure Functions, Azure Table Storage
Azure Function, NodeJS를 사용한 기본 API(CRUD)만들기\
https://docs.microsoft.com/en-us/azure/cosmos-db/table-storage-how-to-use-nodejs


## 다루는 내용
WIP...

## 사전 준비
* Azure 계정



### 1.준비하기(Setup)
**1. NodeJS 설치**
* https://nodejs.org/en/download/ 접속 후 다운로드, 설치
* Cmd에서 [node -v] 쳐서 버전 나오면 설치완료 된 것


**2. Azure Functions App 설치**
* cmd에서 아래를 입력한다.
> npm install -s azure-storage\
> npm install -s uuid


**3. 폴더 구조 만들기 Create CRUD folders**
* ItemCreate / ItemRead / ItemUpdate / ItemDelete
* 각 폴더 안에 [function.json], [index.js] 만들기
* [methods] in file [function.json] 파일의 [methods]를 반영해서, http crud api 구조를 갖춘다.
    * CRUD -> POST / GET / PUT / DELETE 

[delete 샘플]
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
    ![001](./images/001.PNG)


**5. Function App에 Database 정보를 연결**
* 프로젝트 root 폴더에 .env 파일을 생성하고, CONNECTION STRING을 추가한다. (enronment variable)
    * CONNETION STRING은 Azure Portal Cosmos DB 리소스에서 조회할 수 있다
    * Environment Variable을 추가하는 방법: [여기](https://medium.com/the-node-js-collection/making-your-node-js-work-everywhere-with-environment-variables-2da8cdf6e786) 참고
* [index.js]파일에 Azure Cosmos DB 연결을 추가한다
```
    //import package
    const storage = require('azure-storage');
    //connect to cosmos DB with connection string
    const connectionString = process.env.CONNECTION_STRING;
    //Create a table
    const tableSvc = storage.createTableService(connectionString);
```

**6. Table을 생성한다**
* 아래 코드를 삽입하여 테이블을 생성한다. 성공적으로 생성하면 result.created의 값이 true, 그렇지 않으면 false가 된다.
```
//create a table
const tableSvc = storage.createTableService(connectionString);
tableSvc.createTableIfNotExists('mytable', function(error, result, response){
    if(!error){
      // Table exists or created
    }
  });
```