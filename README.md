# FastAPI

## Theory

Is a micro-framwork like flask. When we deploy a flask app it use a `WSGI containers - Web Server Gateway Interface` like `gunicorn` and others. Unlike flask, fastapi is an `ASGI containers - Asynchronous server gareway interface ` like `uvicorn`.

uvicorn is a server implementation that's provide a standard interface between python web servers frameworks and application. Uvicorn support http2 and websockets.

Uvicorn uses `starlette` which is a lightweight ASGI framework to build asyncio services.

## Instalación

Esto instalará fastAPI, uvicorn and starlette

```
pip install "fastapi[all]"
```

si da algún error de `wheel-...`

```
pip install wheel
```

## Primeros pasos

La estructura que podemos generar para fastAPI es:

```
project
    |_main.py
    |_misApps
        | __init__.py
        |_ app.py
```

El entry-point de la app será `main.py`.

la manera más sencilla de empezar una API sería

en el archivo main.py ponemos

```python
import uvicorn

if __name__ == "__main__":
    uvicorn.run('misApps.app:newApp', host="127.0.0.1", port=8000, reload=True)
    # uvicorn.run('misApps.app:newApp', reload=True)
```

esto arranca el server ejecutando la función newApp que se encuentra en la ruta `misApps/app.py`

```python
from fastapi import FastAPI


newApp = FastAPI()

# path operation
@newApp.get("/", tags=['ROOT'])
async def root()-> dict:
    return {"message":"hello world"}
```

El tag es para la documentation y `->dict` fija que el return de esa función será un dictionary.

Automáticamente fastAPI convierte el valor de retorno en un JSON

para ejecutar el server solo tenemos que correr el archivo main.py `python main.py`

El nombre que le pongamos a la función tampoco importa demasiado, debe ser lo más dscriptivo posible. Lo importante es el decorator

Cuando instalamos fastAPI se instalo un servidor, uvicorn, así que tanto en local como en deploy deberemos instalar esta dependencia.

Si no tenemos hecho el entry-point en el archivo main.py y tenemos el código de fastAPI directamente en el archivo main.py, para arrancar el servidor, vamos a la terminal

```
uvicorn main:newApp --reload
```

donde main:app es el nombre del archivo que contiene el entry point (main.py) y app es como hemos llamado a la instancia de fastAPI.

puedo modificarlo, si llamo a mi archivo principal `app.py` le paso ese nombre.

```
uvicorn app:my_app --reload
```

![not found](img/1.png)

Hay que tener en cuenta que se ejecuta el primer `path operation` que encaja con la url solicitada, así que el orden importa

## CRUD operation

If we take a look of /docs we will see what for is a tag.

![not found](img/31.png)

a quick intro building a CRUD app

```python

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
```

## mini-app FARM stack (FastApi - react - mongodb)

to build this app we need 3 requirements:

- fastAPI
- uvicorn
- motor -> is a full featured non-blocking io mongodb driver

Tendremos esta estructura

```
react-app
    |_back-end
        \_ database.py
         |_ main.py
         |_ model.py
         |_ __init__.py
    |_front-end
        |
        |
```

en el main.py

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# we add an origin for front-end with react
origins = [
    "http://localhost:3000",
]

# in production we could add a front

app.add_middleware(
    CORSMiddleware,
    allow_origins= origins,
    allow_credentials= True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", tags=['ROOT'])
async def read_root():
    return {"ping":"pong"}


```

middleware `cors` stands for cross origin resource sharing. We must use it coz we run a front-end JS server and another server using fastAPI in the back-end, so front-end and back-end are in a different origin - is a combination of protocol domain (http https) and port. So react will have port 3000 and fastAPI 8000 so we will need some sort of permission for backend interact with a different origin, different port

Una vez hecho esto debemos crear nuestra react-app

```
npx create-react-app front-end
```

entramos en el directorio y corremos el server de react

```
npm start
```

debemos instalar 2 paquetes npm

1. axios -> para enviar request from the client to the server (we could use Fetch API) and getting response from the backend server
2. bootstrap

```
npm install axios bootstrap
```

## path operation

### GET

```python
@app.get("/")
def root():
    return {"message":"welcome to my API"}
```

### POST

Cuando tenemos un request tipo post se envia info a través del body del request.

Lo más habitual es la info se envie en formato JSON. Por lo que el path operator tiene que ser capaz de recibir esa info. Para ello hacemos un import `from fastapi.params import Body`

```python

# path operation - 3 POST request
@app.post("/createposts")
def create_posts(payLoad:dict):

    return {"new_post":f'titel: {payLoad["title"]} content: {payLoad["content"]}'}
```

Si lo que enviamos en el body de la request es del tipo JSON, lo casteamos directamente a dictionary extraerá todos los campos del body y los guardará en la variable `payLoad` tipo dictionary.

El problema de esto es que necesitamos que lo que envie el user debe cumplir un esquema, para ello podemos generar un schema usando `pydantic`

con esta extensión que se instala junto con fastAPI podemos generar una clase para que haga de schema y la request debe enviar una data q se autovalidará con nuestro schema.

```python
from pydantic import BaseModel

class Post(BaseModel):
    title: str
    content: str
    publish: bool = True # OPtional field by default it will b True

# path operation - 3 POST request
@app.post("/createposts")
def create_posts(post:Post):
    return {"new_post":f'titel: {post.title} content: {post.content}'}
```

si enviamos data q no coincide cn ese schema fastapi automáticamnete responde con un error

```javascript
 {
    "detail": [
        {
            "loc": [
                "body",
                "title"
            ],
            "msg": "field required",
            "type": "value_error.missing"
        }
    ]
}
```

# Deploy of FARM app to heroku and github Pages

To this deploy we will have three repors: one into frontend and backend folders. An other one inside app folder. So we will config a git repo of front and back as a submodule of the app

```
git submodule add git@github.com:url_to/awesome_submodule.git path_to_awesome_submodule
```

with this config we can deploy them separatly.

```
react-app
    |_back-end
        \_ database.py
         |_ main.py
         |_ model.py
         |_ __init__.py
    |_front-end
        |_package.json
        |
```

This app has two parts, backend and frontend. So we will deploy our backend build in fastAPI on heroku and our frontend build in react to github Pages.

## backend deploy to heroku

```
react-app
    |_back-end
        \_ database.py
         |_ main.py
         |_ model.py
         |_ __init__.py
         |_ .env
         |_ venv
         |
         |_ Procfile
         |_ runtime.txt
         |_ requirements.txt
```

create on the root directory of the backend:

1. create a requirements.txt file with all dependenies ` pip freeze > requirements.txt`
2. create a runtime.txt file wit python version used in the project `python-3.8.6`
3. Procfile , no extension needed
   If you have the main.py in the app directory, add the following:

   1. `web: uvicorn app.main:app --host=0.0.0.0 --port=${PORT:-5000}`

      If you have the main.py in the root directory:

   2. `web: uvicorn main:app --host=0.0.0.0 --port=${PORT:-5000}`

4. add variables on heroku in secction config Vars, for instance our url to connect to mongoAtlas
   1. URL_MONGO = xxx
   2. our app will use variables in .env file but if detect a global variable will use it

```python
from dotenv import dotenv_values
import os

config = dotenv_values(".env")
DATABASE_URI = config.get("mongo_url")

if os.getenv("DATABASE_URI"): DATABASE_URI = os.getenv("DATABASE_URI") #ensures that if we have a system environment variable, it uses that instead

```

5. push our app to heroku `git push heroku main`
6. `heroku open`

## frontend deploy to github Pages

1. install a dependencie `npm install gh-pages --save-dev`
2. Add some properties to the app's `package.json` file

   1. at the top of the file add

   ```javascript
   //..
   "homepage": "http://gitname.github.io/react-gh-pages"
   ```

   2. add to the existing scripts

   ```javascript
   "scripts": {
   //...
   "predeploy": "npm run build",
   "deploy": "gh-pages -d build"
   }
   ```

3. Create a git repository in the app's folder. `git init`
4. Add the GitHub repository as a "remote" in your local git repository. (dont create a repo in github)
   1. `$ git remote add origin https://github.com/gitname/react-gh-pages.git`
   2. if we have allready a repo created in github create a branch called `gh-pages`
5. deploy the project `$ npm run deploy`

