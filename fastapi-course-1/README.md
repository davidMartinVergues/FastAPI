- [FastApi youtube Course](#fastapi-youtube-course)
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

# FastApi youtube Course

source : https://www.youtube.com/watch?v=tiBeLLv5GJo&t=1647s


# 🚀 Cómo levantar una aplicación FastAPI
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


# 🧠 Resumen de cómo FastAPI captura los parámetros

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

# 📋 Uso de listas como parámetros de consulta (query) en FastAPI

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


# 📮 Peticiones POST y PUT con FastAPI y Pydantic

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
