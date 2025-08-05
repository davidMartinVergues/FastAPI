"""
PATRÓN PROFESIONAL: Services con @with_transaction
Arquitectura limpia con inyección automática de sesiones
"""

import uuid
from fastapi import APIRouter, HTTPException
from .user_service import UserService
from models import UsersUpdate

router = APIRouter()

# =============================================================================
# PATRÓN PROFESIONAL: Services con @with_transaction
# =============================================================================

@router.post("/create-user")
async def create_user(name: str, email: str):
    """
    PASO 1: Controller - Solo maneja HTTP y llama al Service
    No maneja sesiones ni transacciones directamente
    """
    service = UserService()
    try:
        result = await service.create_user_with_profile(name, email)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error interno del servidor: {e}")


@router.put("/users/{user_id}")
async def update_user(user_id: uuid.UUID, user_data : UsersUpdate):
    """
    Controller que delega toda la lógica al Service
    """
    service = UserService()
    try:
        result = await service.update_user_transactional(user_id, user_data.name, user_data.email)
        return result
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error actualizando usuario")


@router.delete("/users/{user_id}")
async def delete_user_cascade(user_id: uuid.UUID):
    """
    Operación compleja delegada completamente al Service
    """
    service = UserService()
    try:
        result = await service.delete_user_cascade(user_id)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error eliminando usuario")


# =============================================================================
# EXPLICACIÓN PASO A PASO DEL PATRÓN @with_transaction
# =============================================================================

"""
🎯 ARQUITECTURA EN 3 CAPAS:

1. CONTROLLER (FastAPI Router)
   ├── Solo maneja HTTP (request/response)
   ├── Valida datos de entrada
   ├── Llama al Service correspondiente
   └── Maneja excepciones y códigos HTTP

2. SERVICE (Use Cases / Application Layer)
   ├── Contiene la lógica de negocio
   ├── Usa @with_transaction para transacciones automáticas
   ├── Coordina múltiples repositories
   └── No conoce nada sobre HTTP

3. REPOSITORY (Data Access Layer)
   ├── Hereda de IAsyncDatabaseRepository
   ├── Accede directamente a la base de datos
   ├── Recibe la sesión inyectada automáticamente
   └── Solo se encarga de operaciones CRUD

🔄 FLUJO PASO A PASO:

PASO 1: Cliente hace request HTTP
├── POST /users {"name": "Juan", "email": "juan@email.com"}

PASO 2: FastAPI Router (Controller)
├── def create_user(name, email):
├── service = UserService()
└── await service.create_user_with_profile(name, email)

PASO 3: Service con @with_transaction
├── @with_transaction  ← AQUÍ OCURRE LA MAGIA
├── async def create_user_with_profile(self, name, email):
├── El decorator:
│   ├── Crea una nueva sesión DB
│   ├── Busca todos los repositories en self (self.user_repo, self.profile_repo, etc.)
│   ├── Inyecta automáticamente la sesión en cada repository
│   └── Establece la sesión en el contexto global
└── Ejecuta la función del service

PASO 4: Service ejecuta lógica de negocio
├── user_id = await self.user_repo.create_user(name, email)  ← Repository 1
├── profile_id = await self.profile_repo.create_profile(user_id)  ← Repository 2
└── await self.notification_repo.send_welcome(user_id)  ← Repository 3

PASO 5: Repositories usan sesión inyectada
├── class UserRepository(IAsyncDatabaseRepository):
├── async def create_user(self, name, email):
├── self.db ← Esta sesión fue inyectada automáticamente por @with_transaction
└── await self.db.add(user) / await self.db.commit() etc.

PASO 6: @with_transaction maneja el resultado
├── Si TODO sale bien → await session.commit() automático
├── Si HAY error → await session.rollback() automático
└── Siempre → session.close() automático

PASO 7: Controller devuelve respuesta HTTP
├── return {"user_id": user_id, "message": "Usuario creado"}
└── HTTP 200 OK

✨ VENTAJAS DE ESTE PATRÓN:

1. SEPARACIÓN DE RESPONSABILIDADES
   ├── Controller: Solo HTTP
   ├── Service: Solo lógica de negocio
   └── Repository: Solo acceso a datos

2. TRANSACCIONES AUTOMÁTICAS
   ├── Una transacción por use case
   ├── Commit/rollback automático
   └── No código boilerplate

3. INYECCIÓN AUTOMÁTICA
   ├── No pasar sesiones manualmente
   ├── Todos los repositories comparten la misma sesión
   └── Consistencia de datos garantizada

4. TESTEABLE
   ├── Services independientes de FastAPI
   ├── Repositories mockeable fácilmente
   └── Lógica de negocio aislada

5. ESCALABLE
   ├── Fácil agregar nuevos repositories
   ├── Use cases complejos sin complejidad adicional
   └── Reutilización de código
"""