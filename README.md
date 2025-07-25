- [FastApi youtube Course - FastAPI Beyond CRUD](#fastapi-youtube-course---fastapi-beyond-crud)
- [FastApi youtube Course - Analytics api](#fastapi-youtube-course---analytics-api)
  - [🚀 Cómo levantar una aplicación FastAPI](#-cómo-levantar-una-aplicación-fastapi)
  - [🧪 1. Modo local (desarrollo)](#-1-modo-local-desarrollo)
  - [🐳 2. Modo Docker (desarrollo o testing)](#-2-modo-docker-desarrollo-o-testing)
  - [🔍 ¿Qué significa cada parte?](#-qué-significa-cada-parte)
  - [🔐 3. Modo producción (Gunicorn + UvicornWorker)](#-3-modo-producción-gunicorn--uvicornworker)
  - [⚙️ Diferencias entre Uvicorn y Gunicorn](#️-diferencias-entre-uvicorn-y-gunicorn)
  - [✅ ¿Cuándo usar cada uno?](#-cuándo-usar-cada-uno)
  - [Docker \& Docker Compose](#docker--docker-compose)
  - [🧠 Resumen de cómo FastAPI captura los parámetros](#-resumen-de-cómo-fastapi-captura-los-parámetros)
  - [✅ GET](#-get)
    - [🔹 1. Parámetros de ruta (path parameters)](#-1-parámetros-de-ruta-path-parameters)
    - [🔹 2. Parámetros de consulta (query parameters)](#-2-parámetros-de-consulta-query-parameters)
      - [Opción A: Declararlos individualmente](#opción-a-declararlos-individualmente)
      - [Opción B: Usar un modelo Pydantic + `Depends`](#opción-b-usar-un-modelo-pydantic--depends)
  - [✅ POST](#-post)
    - [🔹 Datos complejos en el cuerpo (JSON)](#-datos-complejos-en-el-cuerpo-json)
    - [🔹 Datos simples en el cuerpo (`str`, `int`, etc.)](#-datos-simples-en-el-cuerpo-str-int-etc)
  - [✅ Conclusión](#-conclusión)
  - [📋 Uso de listas como parámetros de consulta (query) en FastAPI](#-uso-de-listas-como-parámetros-de-consulta-query-en-fastapi)
  - [✅ Declarar listas en parámetros de función](#-declarar-listas-en-parámetros-de-función)
  - [🔗 Cómo llamar al endpoint](#-cómo-llamar-al-endpoint)
  - [⚙️ Otra opción: Usar modelo Pydantic + Depends (menos común)](#️-otra-opción-usar-modelo-pydantic--depends-menos-común)
  - [🧠 Conclusión](#-conclusión-1)
  - [📮 Peticiones POST y PUT con FastAPI y Pydantic](#-peticiones-post-y-put-con-fastapi-y-pydantic)
  - [✅ Uso de `Body(...)` en FastAPI](#-uso-de-body-en-fastapi)
    - [🔹 Sintaxis básica](#-sintaxis-básica)
    - [🔹 ¿Qué significa `...`?](#-qué-significa-)
    - [🔹 Otros usos comunes](#-otros-usos-comunes)
  - [📥 `POST` con modelo Pydantic](#-post-con-modelo-pydantic)
    - [🔸 JSON esperado:](#-json-esperado)
  - [🔁 `PUT` con modelo Pydantic (actualización parcial)](#-put-con-modelo-pydantic-actualización-parcial)
    - [🔹 Endpoint PUT con `exclude_unset=True`:](#-endpoint-put-con-exclude_unsettrue)
  - [✏️ `PUT` con datos simples (sin modelo)](#️-put-con-datos-simples-sin-modelo)
    - [🔸 JSON esperado:](#-json-esperado-1)
    - [🔹 Varios valores simples:](#-varios-valores-simples)
  - [⚠️ Cuidado: sin `Body(...)` FastAPI lo busca en la query](#️-cuidado-sin-body-fastapi-lo-busca-en-la-query)
  - [✅ Conclusión](#-conclusión-2)
  - [Integrando bbdd postgres](#integrando-bbdd-postgres)
    - [Storing data using SQLModel](#storing-data-using-sqlmodel)
    - [Variables de entorno](#variables-de-entorno)
    - [Uso de SQLModel](#uso-de-sqlmodel)
- [FastAPI](#fastapi)
  - [Theory](#theory)
  - [Instalación](#instalación)
  - [Primeros pasos](#primeros-pasos)
  - [CRUD operation](#crud-operation)
  - [mini-app FARM stack (FastApi - react - mongodb)](#mini-app-farm-stack-fastapi---react---mongodb)
  - [path operation](#path-operation)
    - [GET](#get)
    - [POST](#post)
- [Deploy of FARM app to heroku and github Pages](#deploy-of-farm-app-to-heroku-and-github-pages)
  - [backend deploy to heroku](#backend-deploy-to-heroku)
  - [frontend deploy to github Pages](#frontend-deploy-to-github-pages)



# FastApi youtube Course - FastAPI Beyond CRUD 

source : https://www.youtube.com/watch?v=TO4aQ3ghFOc&t=13s




# FastApi youtube Course - Analytics api

source : https://www.youtube.com/watch?v=tiBeLLv5GJo&t=1647s


## 🚀 Cómo levantar una aplicación FastAPI
---

## 🧪 1. Modo local (desarrollo)

```bash
uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

- Recarga automática al guardar archivos (`--reload`).
- Solo accesible desde tu máquina (`127.0.0.1`).

---

## 🐳 2. Modo Docker (desarrollo o testing)

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

## 🔍 ¿Qué significa cada parte?

- **`uvicorn`**: es el servidor ASGI ligero que ejecuta FastAPI.

- **`main:app`**:
  - `main` → nombre del archivo (por ejemplo, `main.py`)
  - `app` → nombre de la instancia `FastAPI()`

- **`--reload`**: activa la recarga automática al detectar cambios en el código. Ideal para desarrollo.

- **`--host 0.0.0.0`**: hace que la app escuche en todas las interfaces de red, permitiendo acceso desde fuera del contenedor o máquina local (por ejemplo, desde Docker).

- **`--port 8000`**: puerto en el que se expone la API.

En `docker-compose.yml`:

```yaml
ports:
  - "8000:8000"
```

- `0.0.0.0` permite acceder desde otros contenedores o desde el host.
- Ideal para desarrollo en contenedor.

---

## 🔐 3. Modo producción (Gunicorn + UvicornWorker)

```bash
gunicorn -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000 main:app
```

- Lanzamiento con múltiples workers para alta disponibilidad.
- Mejor rendimiento y escalabilidad.
- Usado con Nginx o Kubernetes.

---

## ⚙️ Diferencias entre Uvicorn y Gunicorn

| Característica       | Uvicorn         | Gunicorn + UvicornWorker       |
| -------------------- | --------------- | ------------------------------ |
| Tipo                 | Servidor ASGI   | Servidor WSGI con soporte ASGI |
| Uso típico           | Desarrollo      | Producción                     |
| Recarga automática   | Sí (`--reload`) | No                             |
| Multi-worker         | No              | Sí                             |
| Rendimiento          | Bueno (1 core)  | Alto (multi-core)              |
| Soporte para FastAPI | Nativo          | A través de `UvicornWorker`    |

---

## ✅ ¿Cuándo usar cada uno?

- **Uvicorn**: desarrollo, testing local, recarga automática.
- **Gunicorn + UvicornWorker**: producción, carga real, múltiples procesos, robustez.



## Docker & Docker Compose

```dockerfile
services:
  webapp-container-name:
    image: analytics-api-my-image-name:v1
    build:
      context: .
      dockerfile: Dockerfile-web
    environment:
      - PORT=8001
    env_file:
      - .env
    ports:
      - "8081:8001"
    command: uvicorn main:app --host 0.0.0.0 --port 8001 --reload
    volumes:
      - ./src:/code:rw
    develop:
      watch:
        - action: rebuild
          path: Dockerfile-web
        - action: rebuild
          path: requirements.txt
        - action: rebuild
          path: docker-compose.yaml

```
Si lo dejamos así primero hace caso a la variable declarada en la sección `environment` si tb esta en el archivo la sobreescribirá.

becomes

Develop watch es algo nuevo en docker compose que permite reconstruir las imagenes en cuanto hay un cambio
docker compose up --watch
docker compose down or docker compose down -v (to remove volumes)
docker compose run app /bin/bash or docker compose run app python


## 🧠 Resumen de cómo FastAPI captura los parámetros

FastAPI determina de dónde vienen los datos según el tipo de petición y el tipo de parámetro declarado en la función. Aquí se resumen las formas más comunes:

---

## ✅ GET

### 🔹 1. Parámetros de ruta (path parameters)

Se capturan directamente por nombre en la función:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    ...
```

---

### 🔹 2. Parámetros de consulta (query parameters)

#### Opción A: Declararlos individualmente

```python
@app.get("/users/")
def get_users(name: str, age: int = 0):
    ...
```

#### Opción B: Usar un modelo Pydantic + `Depends`

```python
from pydantic import BaseModel
from fastapi import Depends

class FilterParams(BaseModel):
    name: str
    age: int = 0

@app.get("/users/")
def get_users(filters: FilterParams = Depends()):
    ...
```

---

## ✅ POST

### 🔹 Datos complejos en el cuerpo (JSON)

FastAPI usa modelos Pydantic para parsear el `body` automáticamente:

```python
from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int

@app.post("/users/")
def create_user(user: UserCreate):
    ...
```

---

### 🔹 Datos simples en el cuerpo (`str`, `int`, etc.)

Debes usar `Body(...)` para que FastAPI sepa que vienen del `body`:

```python
from fastapi import Body

@app.post("/example/")
def create_item(name: str = Body(...), active: bool = Body(False)):
    ...
```

---

## ✅ Conclusión

- Los **path params** se capturan por nombre.
- Los **query params** pueden declararse por separado o agruparse en un `BaseModel` con `Depends`.
- En **POST**, los datos complejos se capturan con un modelo Pydantic.
- Para **valores simples** en el body, se debe usar `Body(...)`.

---

## 📋 Uso de listas como parámetros de consulta (query) en FastAPI

FastAPI permite recibir **listas como parámetros de consulta** (query parameters) en peticiones `GET` usando `Query(...)`.

---

## ✅ Declarar listas en parámetros de función

```python
from fastapi import FastAPI, Query
from typing import List

app = FastAPI()

@app.get("/items/")
def get_items(test2: List[str] = Query(...)):
    return {"test2": test2}
```

- El parámetro `test2` es una **lista obligatoria** de cadenas (`str`).
- El `...` indica que es **requerido**.
- Puedes hacer que sea opcional así: `= Query(None)` o `= Query([])`.

---

## 🔗 Cómo llamar al endpoint

Puedes pasar múltiples valores usando el mismo nombre de parámetro repetido:

```
GET /items/?test2=uno&test2=dos&test2=tres
```

FastAPI interpretará eso como:

```json
{
  "test2": ["uno", "dos", "tres"]
}
```

---

## ⚙️ Otra opción: Usar modelo Pydantic + Depends (menos común)

```python
from fastapi import Depends
from fastapi import Query
from pydantic import BaseModel, Field
from typing import List

class EventSchema(BaseModel):
    test2: List[str] = Field(Query([])) # valor por defecto lista vacía

@app.get("/events/")
def get_event(query_params: EventSchema = Depends(EventSchema)):
    return query_params
```

Esto también funciona, aunque no es el uso más típico de `Field(Query(...))`, y puede ser confuso para quienes lean el código.

---

## 🧠 Conclusión

- Para listas en la query string, usa `List[...] = Query(...)` directamente en los parámetros.
- La URL debe repetir el nombre del parámetro para cada valor.
- Usar modelos Pydantic + `Depends` también es válido, pero más avanzado.


---


## 📮 Peticiones POST y PUT con FastAPI y Pydantic

Este documento explica cómo usar `POST` y `PUT` en FastAPI utilizando modelos `Pydantic` o parámetros simples mediante `Body(...)`. También se cubren actualizaciones parciales de datos usando `exclude_unset=True`.

---

## ✅ Uso de `Body(...)` en FastAPI

En FastAPI, `Body(...)` se utiliza para indicar que un parámetro simple (`str`, `int`, `bool`, etc.) debe extraerse del **cuerpo (body)** de la solicitud HTTP, en lugar de la query.

### 🔹 Sintaxis básica

```python
from fastapi import Body

@app.post("/example/")
def create_item(name: str = Body(...)):
    return {"name": name}
```

### 🔹 ¿Qué significa `...`?

- `...` (alias de `Ellipsis`) indica que el campo es **obligatorio**.

### 🔹 Otros usos comunes

| Sintaxis                     | Significado                                               |
| ---------------------------- | --------------------------------------------------------- |
| `Body(...)`                  | El parámetro es obligatorio                               |
| `Body("valor")`              | Valor por defecto opcional                                |
| `Body(..., embed=True)`      | Espera un JSON con clave explícita: `{ "name": "valor" }` |
| `Body(..., example="valor")` | Añade un ejemplo a Swagger                                |
| `Body(..., title="Título")`  | Añade un título en la documentación                       |

---

## 📥 `POST` con modelo Pydantic

FastAPI detecta automáticamente que los modelos `Pydantic` deben ir en el body.

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/items/")
def create_item(item: Item):
    return {"received": item}
```

### 🔸 JSON esperado:

```json
{
  "name": "Teclado",
  "price": 49.99,
  "in_stock": true
}
```

Puedes usar `Body(...)` para añadir metadatos:

```python
from fastapi import Body

@app.post("/items/")
def create_item(item: Item = Body(..., title="Item data", example={"name": "Mouse", "price": 25.5})):
    return item
```

---

## 🔁 `PUT` con modelo Pydantic (actualización parcial)

Para permitir actualizaciones parciales, define un modelo con todos los campos como opcionales:

```python
from typing import Optional

class UpdateItem(BaseModel):
    name: Optional[str] = None
    price: Optional[float] = None
    in_stock: Optional[bool] = None
```

### 🔹 Endpoint PUT con `exclude_unset=True`:

```python
@app.put("/items/{item_id}")
def update_item(item_id: int, item_update: UpdateItem):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")

    stored_item = db[item_id]
    update_data = item_update.dict(exclude_unset=True)
    updated_item = stored_item.copy(update=update_data)

    db[item_id] = updated_item
    return updated_item
```

---

## ✏️ `PUT` con datos simples (sin modelo)

También puedes usar `PUT` con valores aislados mediante `Body(...)`:

```python
from fastapi import Body

@app.put("/toggle/")
def toggle_item(active: bool = Body(...)):
    return {"status": "updated", "active": active}
```

### 🔸 JSON esperado:

```json
{
  "active": true
}
```

### 🔹 Varios valores simples:

```python
@app.put("/update/")
def update_item(name: str = Body(...), price: float = Body(...)):
    return {"updated_name": name, "updated_price": price}
```

```json
{
  "name": "Pantalla",
  "price": 199.99
}
```

---

## ⚠️ Cuidado: sin `Body(...)` FastAPI lo busca en la query

```python
@app.put("/wrong/")
def update_item(name: str):
    return {"name": name}
```

- Este ejemplo esperará `/wrong/?name=valor` (no en el body).

---

## ✅ Conclusión

- Usa **modelos Pydantic** para peticiones complejas (JSON estructurado).
- Usa `Body(...)` para **valores simples** en el cuerpo de la petición.
- Para **actualizaciones parciales**, usa un modelo con campos `Optional[...]` y `exclude_unset=True`.


## Integrando bbdd postgres

Para ello usaremos una bbdd montada sobre postgres que potencia postgres para que sea eficiente analizando datos en tiempo realm, esta ddbb se llama `time scale DB` y la usaremos junto con SQLModel (pydantic + SQLAlchemy)

### Storing data using SQLModel

Para ello cogeremos el esquema de validación de pydantic para validar los datos de entrada o de salida y lo vamos a convertir  para poderlo guardar en nuetsra bbdd.

Una vez tenemos todo configurado ( varibales de entorno = user , password, nombre bbdd  ) podemos crear la cadena de conexión cn la bbdd siempre se construye igual:

`postgresql+psycopg://time-user:time-pw@hostvalue:5432/timescaledb`

en el `hostvalue` tenemos que poner el nuestro servicio de bbdd. 

responde a este standard;

`dialect+driver://username:password@host:port/database`

| Fragmento            | Significado                                                                                                                     |
| -------------------- | ------------------------------------------------------------------------------------------------------------------------------- |
| `postgresql+psycopg` | Dialecto y driver. `postgresql` es el tipo de base de datos, `psycopg` es el driver (cliente de conexión) que SQLAlchemy usará. |
| `time-user`          | Nombre de usuario de la base de datos                                                                                           |
| `time-pw`            | Contraseña del usuario                                                                                                          |
| `hostvalue`          | Dirección del servidor (puede ser `localhost`, `127.0.0.1`, o el nombre de un contenedor como `db_service`)                     |
| `5432`               | Puerto en el que está escuchando PostgreSQL (por defecto es `5432`)                                                             |
| `timescaledb`        | Nombre de la base de datos a la que quieres conectarte                                                                          |

este sería nuestro docker compose

```dockercompose
services:
  webapp-container-name:
    image: analytics-api-my-image-name:v1
    build:
      context: .
      dockerfile: Dockerfile-web
    environment:
      - PORT=8001
      - DATABASE_URL=postgresql+psycopg://time-user:time-pw@db_service:5432/timescaledb
    env_file:
      - .env
    ports:
      - "8081:8001"
    command: uvicorn main:app --host 0.0.0.0 --port 8001 --reload
    volumes:
      - ./src:/code:rw
    develop:
      watch:
        - action: rebuild
          path: Dockerfile-web
        - action: rebuild
          path: requirements.txt
        - action: rebuild
          path: docker-compose.yaml
  db_service:
    image: timescale/timescaledb:latest-pg17
    environment:
      - POSTGRES_USER=time-user
      - POSTGRES_PASSWORD=time-pw
      - POSTGRES_DB=timescaledb
    ports:
      - "5434:5432"
    expose:
      - 5434
    volumes:
      - timescaledb_data:/var/lib/postgresql/data

volumes:
  timescaledb_data:
  

```

el uso de expose:

* Sólo expone el puerto a otros contenedores dentro de la red de Docker Compose, no al host.

* Es como decir: "Este contenedor está escuchando en este puerto", para que otros servicios de la red puedan conectarse.

* No mapea ese puerto a tu máquina local.


### Variables de entorno

Para cargar en los archivos python las variables de entorno usaremos un paquete llamado `python-decouple` Estas variables de entorno las podemos pasar desde el `docker compose`, si no las especificamos en el apartado(environment) :

```Dockerfile
services:
  webapp-container-name:
    image: analytics-api-my-image-name:v1
    build:
      context: .
      dockerfile: Dockerfile-web
    environment:
      - PORT=8001
      - DATABASE_URL=postgresql+psycopg://time-user:time-pw@db_service:5432/timescaledb
```

 las buscará en el archivo `.env`.

La diferencia de poner las variables de entorno en el docker-compose o en un archivo .env es que en el dockercompose éstas se inyecan directamente y desde el código podemos acceder a ellas mediante 

```python

import os

os.environ.get("DATABASE_URL")

```
### Uso de SQLModel

SQLModel es una librería que combina pydantic (validación de modelos) con sqlalchemy persistencia en bbdd. Suena genial pero no nos permite aplicarlo en una arqutectura hexagonal, ya que necesitamos seguir usando pydantic para mantener separadas las capas e independecia de modelos de dominio de los modelos de infra. Si usamos SQLModel para dominio como este internamente depende de sqlalchemy estariamos introduciendo temas de bbdd en el dominio.

un ejemplo de como insertar una table en la bbdd con SQLModel sigue tres pasos:

1. Conectar con la bbdd usado un `database engine`, es decir permitir a python pueda llamar a sql

2. una vez hecha la conexión tenemos q definir nuestro modelo y decirle q ese modelo se convertirá en una tabla

```python
from sqlmodel import Field, SQLModel


class Hero(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    name: str
    secret_name: str
    age: int | None = None
```



# FastAPI

## Theory

Is a micro-framwork like flask. When we deploy a flask app it use a `WSGI containers - Web Server Gateway Interface` like `gunicorn` and others. Unlike flask, fastapi is an `ASGI containers - Asynchronous server gateway interface ` like `uvicorn`.

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

