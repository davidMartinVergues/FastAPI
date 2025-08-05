- [FastApi Platzi Course](#fastapi-platzi-course)
  - [Descripcion](#descripcion)
  - [SQLModel](#sqlmodel)
  - [async vs sync](#async-vs-sync)
  - [Update objects](#update-objects)
  - [Cómo organizar nuestra app](#cómo-organizar-nuestra-app)
  - [Transacciones en bbdd](#transacciones-en-bbdd)
  - [relaciones many to many](#relaciones-many-to-many)
- [FastApi youtube Course - FastAPI Beyond CRUD](#fastapi-youtube-course---fastapi-beyond-crud)
  - [install FastApi](#install-fastapi)
  - [Create server](#create-server)
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
  - [Request object](#request-object)
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

# FastApi Platzi Course

## Descripcion

Fastapi se basa en dos frameworks :
- starlette => nos facilita la creación de requets HTTP
- pydantic => permite crear modelos de datos

## Pydantic Settings 

¿Para qué sirve?

Gestionar configuración de la aplicación (BD, APIs, secretos) de forma segura y flexible.

Componentes:

1. BaseSettings: Clase base que lee configuración automáticamente
2. SettingsConfigDict: Configura DÓNDE y CÓMO leer los valores

Orden de prioridad:

1. Variables de entorno del servidor (export USER_DB=...)
2. Archivo .env 
3. Valores por defecto en la clase

Ejemplo práctico:

```python
class Settings(BaseSettings):
    USER_DB: str = "default_user"  # ← Especificas QUÉ variables buscar

    model_config = SettingsConfigDict(
        env_file=".env"  # ← Le dices DÓNDE buscar
    )
```

Ventajas:

- Desarrollo: usa .env (fácil)
- Producción: usa variables del servidor (seguro)
- Validación: Pydantic valida tipos automáticamente
- Un solo lugar: defines toda la config en una clase

Resultado:
```python
settings = Settings()  # ← Instancia global lista para usar
settings.USER_DB  # ← Valor final después de aplicar prioridades
```

En resumen: Una forma elegante de manejar configuración que se adapta automáticamente a diferentes
entornos.

Esto lo podemos hacer más complejo y añadir secciones para gestionar los settings de toda nuestra app

```python
from pydantic import BaseModel, Field, validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from typing import Literal

BASE_DIR = Path(__file__).resolve().parent.parent

class DatabaseConfig(BaseModel):
    """Configuración de base de datos"""
    host: str = "localhost"
    port: int = 5432
    user: str = ""
    password: str = ""
    name: str = ""
    pool_size: int = Field(default=10, ge=1, le=50)
    max_overflow: int = Field(default=20, ge=0, le=100)
    echo: bool = False
    
    @property
    def url(self) -> str:
        return f"postgresql+asyncpg://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"

class RedisConfig(BaseModel):
    """Configuración de Redis para cache"""
    host: str = "localhost"
    port: int = 6379
    password: str = ""
    db: int = 0
    ttl: int = Field(default=3600, ge=1)  # TTL en segundos
    
    @property
    def url(self) -> str:
        if self.password:
            return f"redis://:{self.password}@{self.host}:{self.port}/{self.db}"
        return f"redis://{self.host}:{self.port}/{self.db}"

class AppConfig(BaseModel):
    """Configuración general de la aplicación"""
    name: str = "FastAPI App"
    version: str = "1.0.0"
    debug: bool = False
    secret_key: str = Field(..., min_length=32)
    environment: Literal["development", "testing", "staging", "production"] = "development"
    cors_origins: list[str] = ["http://localhost:3000"]
    
    @validator('secret_key')
    def validate_secret_key(cls, v):
        if len(v) < 32:
            raise ValueError('SECRET_KEY debe tener al menos 32 caracteres')
        return v

class EmailConfig(BaseModel):
    """Configuración para servicios de email"""
    provider: Literal["sendgrid", "mailgun", "smtp"] = "smtp"
    
    # SendGrid
    sendgrid_api_key: str = ""
    
    # SMTP
    smtp_host: str = "localhost"
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    smtp_tls: bool = True
    
    # General
    from_email: str = "noreply@example.com"
    from_name: str = "FastAPI App"

class StripeConfig(BaseModel):
    """Configuración de Stripe para pagos"""
    publishable_key: str = ""
    secret_key: str = ""
    webhook_secret: str = ""
    currency: str = "usd"
    
    @validator('secret_key')
    def validate_stripe_key(cls, v):
        if v and not v.startswith(('sk_test_', 'sk_live_')):
            raise ValueError('Stripe secret key debe empezar con sk_test_ o sk_live_')
        return v

class SecurityConfig(BaseModel):
    """Configuración de seguridad"""
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = Field(default=30, ge=1)
    password_min_length: int = Field(default=8, ge=6)
    max_login_attempts: int = Field(default=5, ge=1)
    lockout_duration_minutes: int = Field(default=15, ge=1)

class LoggingConfig(BaseModel):
    """Configuración de logging por servicios"""
    # Configuración general
    level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    max_size_mb: int = Field(default=10, ge=1)
    backup_count: int = Field(default=5, ge=1)
    
    # Logs por servicio
    auth_log: str = "logs/auth.log"
    reservations_log: str = "logs/reservations.log"
    payments_log: str = "logs/payments.log"
    email_log: str = "logs/email.log"
    database_log: str = "logs/database.log"
    api_log: str = "logs/api.log"
    errors_log: str = "logs/errors.log"
    customers_log: str = "logs/customers.log"
    
    # Configuración específica por servicio
    auth_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    payments_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "WARNING"
    database_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "ERROR"
    reservations_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "INFO"
    email_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "WARNING"
    
    @property
    def loggers_config(self) -> dict:
        """Configuración para múltiples loggers"""
        return {
            "auth": {
                "file": self.auth_log,
                "level": self.auth_level,
                "format": f"[AUTH] {self.format}"
            },
            "reservations": {
                "file": self.reservations_log,
                "level": self.reservations_level,
                "format": f"[RESERVATIONS] {self.format}"
            },
            "payments": {
                "file": self.payments_log,
                "level": self.payments_level,
                "format": f"[PAYMENTS] {self.format}"
            },
            "email": {
                "file": self.email_log,
                "level": self.email_level,
                "format": f"[EMAIL] {self.format}"
            },
            "database": {
                "file": self.database_log,
                "level": self.database_level,
                "format": f"[DB] {self.format}"
            },
            "api": {
                "file": self.api_log,
                "level": self.level,
                "format": f"[API] {self.format}"
            },
            "customers": {
                "file": self.customers_log,
                "level": self.level,
                "format": f"[CUSTOMERS] {self.format}"
            },
            "errors": {
                "file": self.errors_log,
                "level": "ERROR",
                "format": f"[ERROR] {self.format}"
            }
        }

class Settings(BaseSettings):
    """Configuración principal de la aplicación"""
    
    # Configuraciones anidadas
    database: DatabaseConfig = DatabaseConfig()
    redis: RedisConfig = RedisConfig()
    app: AppConfig = AppConfig()
    email: EmailConfig = EmailConfig()
    stripe: StripeConfig = StripeConfig()
    security: SecurityConfig = SecurityConfig()
    logging: LoggingConfig = LoggingConfig()
    
    # Configuración del modelo
    model_config = SettingsConfigDict(
        env_file=[BASE_DIR / ".env", BASE_DIR / ".env.local"],
        env_file_encoding="utf-8",
        env_nested_delimiter="__",  # Para variables como DATABASE__HOST
        case_sensitive=False,
        extra="ignore"  # Ignora variables no definidas
    )
    
    @property
    def is_production(self) -> bool:
        return self.app.environment == "production"
    
    @property
    def is_development(self) -> bool:
        return self.app.environment == "development"

# Instancia global
settings = Settings() 
```
## SQLModel
Para convertir nuestros modelos en tablas debemos hacerlo así: 


```python
class Customer(CustomerBase, table=True):
  id : uuid.UUID | None = Field(default=None, primary_key=True)
```

1. `table=True`
2. Usando `Field()`cualquier campo q queramos que se guarde en la tabla tiene que llevar Field.

## async vs sync 

hay q tener en cuenta q para usar postgres como `async`:

  1. instalar `asyncpg`
  2. declarar la url como `f"postgresql://{self.USER_DB}:{self.PSW_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.NAME_DB}"`
hay q tener en cuenta q para usar postgres como `sync`:
  3. en las consultas usar : `await` y `scalars()`.
```python
  async def list_customers(session:SessionDep_async):
  result = await session.execute(select(Customer))
  customers: list[Customer] = list(result.scalars().all())
  return customers

```

  4. instalar `psycopg2`
  5. declarar la url como `f"postgresql://{self.USER_DB}:{self.PSW_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.NAME_DB}"`

## Update objects

Hay dos manera:

1. crear un método para controlar qué atributos actualizamos (EL MEJOR MODO) 

```python
class CustomerBase(SQLModel):
  name : str | None = Field(default= None, max_length=250)
  age : int | None = Field(default= None, gt=0)
  email : EmailStr| None = Field(default= None)
  description: str | None = Field(default=None)

  def get_updatable_fields(self)->dict:
      updatable_fields={
          "name",
          "age",
          "email",
          "description"
      }
      return {k:v for k,v in self.model_dump().items() if getattr(self, k) and k in updatable_fields}


# luego en el endpoint 

@app.patch('/customers/{customer_id}', response_model=Customer)
async def update_customers(customer_id:uuid.UUID,customer_data:CustomerUpdate,session:SessionDep):  
    customer = session.get(Customer, customer_id)
    if not customer:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    for key, value in customer_data.get_updatable_fields().items():
            setattr(customer, key, value)
            
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer

```

2. El otro modo usando las funcinoes built in de Fastapi

```python
@app.patch('/customers/{customer_id}', response_model=Customer)
async def update_customers(customer_id:uuid.UUID,customer_data:CustomerUpdate,session:SessionDep):  
    customer = session.get(Customer, customer_id)
    if not customer:
          raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    
    # solo actualiza si se lo pasamos en el body ese atributo 
    customer.sqlmodel_update(customer_data.model_dump(exclude_unset=True))            
    
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer 
```


## Cómo organizar nuestra app 

siguiendo esta estructura es la recomendada en la documentacion:

![not found](img/2.png)

## Transacciones en bbdd 

para englobar varias operaciones en una misma transacción y poder hacer rollback en el caso q alguna salga mal podemos hacer :

1.   Método 1: Transaction Context Manager

```python
@router.post('/complex-transaction')
async def complex_operation(session: SessionDep_async):
    async with session.begin():  # Inicia transacción explícita
        # Operación 1
        customer = Customer(name="Test")
        session.add(customer)

        # Operación 2
        transaction = Transaction(amount=100,customer_id=customer.id)
        session.add(transaction)

# Si cualquier operación falla, rollback automático
# Si todo OK, commit automático al salir del context
```

2.  Decorator para Transacciones

```python
from functools import wraps

def transactional(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        session = kwargs.get('session')
        async with session.begin():
            return await func(*args, **kwargs)
    return wrapper

@router.post('/decorated')
@transactional
async def operation_with_transaction(session: SessionDep_async):
    # Todas las operaciones en una transacción
    pass
```

## relaciones many to many 

Tenemos que crear una tabla intermedia entre dos tablas


# FastApi youtube Course - FastAPI Beyond CRUD 

source : https://www.youtube.com/watch?v=TO4aQ3ghFOc&t=13s

## install FastApi

```
pip install "fastapi[standard]"
```

## Create server

```python
from fastapi import FastAPI
import uvicorn

webapp = FastAPI()

@webapp.get('/')
async def read_root():
    return {"message":"Hello World"}

if __name__ == '__main__':
    uvicorn.run('main:webapp', host="127.0.0.1", port=8000, reload=True) 
```

podemos ejecutar este app de fastapi de distintos modos 

1. usando el `fasapi CLI`
   1. `fastapi dev` o `fastapi dev main.py` => para indicar dnd instanciamos la app de FastAPI
2. ajecutar desde el interprete de python añadiendo previamente el siguiente código `python main.py` 

```python
    if __name__ == '__main__':
      uvicorn.run('main:webapp', host="127.0.0.1", port=8000, reload=True)
```
3. ejecutar desde consola con `uvicorn` con el siguiente comando. Tenemos que especificar la ruta al archivo, en mi caso main, donde se instancia la fastapi app y nombre de la instancia

```bash
uvicorn main:webapp --reload --host 127.0.0.1 --port 8000
```

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

```yml
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

- **GET**
  - Los **path params** se capturan por nombre.
  - Los **query params** pueden declararse por separado o agruparse en un `BaseModel` con `Depends`.
- **POST**, los datos complejos se capturan con un modelo Pydantic.
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

class ItemModel(BaseModel):
    name: str
    price: float
    in_stock: bool = True

@app.post("/items/")
def create_item(item: ItemModel):
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

## Request object

```python
from fastapi import FastAPI,Request

 
@webapp.get('/greet_with_age/{name}')
async def greet_name(request:Request, name:str = "User", age:int=0)->dict:
    request_info = {
        "method": request.method,
        "url": str(request.url),
        "base_url": str(request.base_url),
        "headers": dict(request.headers),
        "query_params": dict(request.query_params),
        "path_params": request.path_params,
        "client": request.client,
        "cookies": request.cookies,
    }
    return {"message":f"Hello {name} you are {age} years old", "req":request_info}

```
en las peticiones de fastapi podemos extraer info de la request utilizando el objeto request. Aquí un ejemplo de todo lo q podría contener:

puedo acceder a los headers directamente usando la funcion `Header`

```python
from fastapi import FastAPI,Request, Header

@webapp.get('/greet_with_age/{name}')
async def greet_name(
  request:Request, 
  name:str = "User", 
  age:int=0,
  accept : str = Header(None)
  )->dict:
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
```

```json
{
    "message": "Hello david you are 4 years old",
    "req": {
        "Host": "127.0.0.1:8000",
        "method": "GET",
        "url": "http://127.0.0.1:8000/greet_with_age/david?age=4",
        "base_url": "http://127.0.0.1:8000/",
        "headers": {
            "user-agent": "PostmanRuntime/7.44.1",
            "accept": "*/*",
            "postman-token": "078360ec-d0b2-42e1-96fb-c2aa540160ee",
            "host": "127.0.0.1:8000",
            "accept-encoding": "gzip, deflate, br",
            "connection": "keep-alive"
        },
        "query_params": {
            "age": "4"
        },
        "path_params": {
            "name": "david"
        },
        "client": [
            "127.0.0.1",
            50028
        ],
        "cookies": {}
    },
    "accept": "*/*"
}
```


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

