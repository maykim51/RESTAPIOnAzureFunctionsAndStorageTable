#WIP... (작업중)

# TIL Rep.: Create CRUD with NodeJS, Azure Functions, Azure Table Storage
Azure Function, NodeJS를 사용한 기본 API(CRUD)만들기
https://docs.microsoft.com/en-us/azure/cosmos-db/table-storage-how-to-use-nodejs



## 다루는 내용
* 

## 사전 준비


### 1.설치하기(Setup)
1. NodeJS 설치
- https://nodejs.org/en/download/ 접속 후 다운로드, 설치
- Cmd에서 [node -v] 쳐서 버전 나오면 설치완료 된 것

2. Azure Functions App 설치
> npm install -s azure-storage
> npm install -s uuid


3. 폴더 구조 만들기 - Create CRUD folders
- ItemCreate / ItemRead / ItemUpdate / ItemDelete
- [methods] in file [function.json] 파일의 [methods]를 반영해서, http crud api 구조를 갖춘다.
----  CRUD -> POST / GET / PUT / DELETE 
[delete 샘플]
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

4. Azure Storage 계정 만들기
[Azure Storage Explorer](https://azure.microsoft.com/en-us/features/storage-explorer/)