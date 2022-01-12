from fastapi import FastAPI


newApp = FastAPI()

# path operation
@newApp.get("/", tags=['ROOT'])
async def root()-> dict:
    return {"message":"hello world"}

# we are gonna implement a to-do-app

# request get -> read Todo

# path operation
@newApp.get("/todo", tags=['todos'])
async def get_todo()-> dict:
    return {"data":todos}

@newApp.post("/todo", tags=["todos"])
async def add_todo(todo:dict)->dict:
    todos.append(todo)
    return {
        "data":"todo added succesfully"
    }

@newApp.put("/todo/{id}", tags=['todos'])
async def update_todo(id:int,body:dict)->dict:

    for todo in todos:
        if int(todo["id"])== id:
            todo['activity']=body["activity"]
            return {
            "data":f'todo - {id} - has been updated succesfully'
            }
    return {
         "data":f'todo {id} has not been updated'
    }

@newApp.delete('/todo/{id}', tags=['todos'])
async def delete_post(id:int)->dict:
    for todo in todos:
        if int(todo["id"])== id:
            todos.remove(todo)
            return {
            "data":f'todo - {id} - has been deleted succesfully'
            }
    return {
         "data":f'todo {id} has not been deleted'
    }




 # we are not gonna implement connection with ddbb so we will use a list as bbdd
todos=[ 
    {
        "id":"1",
        "activity": "learn fastAPI"
    },
    {
        "id":"2",
        "activity": "learn fastAPI faster!"
    },
]