from fastapi import FastAPI,Request, Header
import uvicorn

webapp = FastAPI()

@webapp.get('/')
async def read_root():
    return {"message":"Hello World"}

@webapp.get('/greet/{name}') 
async def greet(name:str)-> dict:
    return {"message":f"Hello {name}"}

@webapp.get('/greet')
async def greet_2(name:str)-> dict:
    return {"message":f"Hello {name}"}

@webapp.get('/greet_with_age/{name}')
async def greet_name(request:Request, name:str = "User", age:int=0,accept : str = Header(None))->dict:
    request_info = {
        "Host": request.headers["host"],
        "method": request.method,
        "url": str(request.url),
        "base_url": str(request.base_url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "path_params": request.path_params,
        "client": request.client,
        "cookies": request.cookies,
    }
    return {"message":f"Hello {name} you are {age} years old", "req":request_info, "accept":accept}

if __name__ == '__main__':
    uvicorn.run('main:webapp', host="127.0.0.1", port=8000, reload=True)