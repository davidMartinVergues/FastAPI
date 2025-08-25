"""
PATRÓN PROFESIONAL: Repository Layer con IAsyncDatabaseRepository
================================================================

Este Repository demuestra cómo recibir sesiones inyectadas automáticamente:
- Hereda de IAsyncDatabaseRepository
- self.db recibe la sesión automáticamente via @with_transaction
- Solo se encarga de operaciones CRUD
"""

import uuid
from fastapi import HTTPException
from sqlmodel import select
from db.db import IAsyncDatabaseRepository
from sqlalchemy import text
from models import Users, UsersUpdate

import logging

log_api = logging.getLogger("api")


# En un proyecto real importarías tu modelo:
# from models.user import User


class UserRepository(IAsyncDatabaseRepository):
    """
    PASO 3: REPOSITORY LAYER
    
    - Hereda de IAsyncDatabaseRepository (OBLIGATORIO)
    - self.db se inyecta automáticamente por @with_transaction
    - Solo operaciones CRUD, sin lógica de negocio
    - No maneja transacciones (eso lo hace el Service)
    """
    
    async def create_user(self, name: str, email: str):
        """
        PASO 3.1: Crear un nuevo usuario
        
        - self.db fue inyectado automáticamente por @with_transaction
        - No hacemos commit/rollback aquí (lo hace el Service)
        - Solo operación CRUD pura
        """
        if not self.db:
            raise ValueError("Database session not injected")
        
        # OPÇÃO A: Con SQLModel (recomendado)
        # user = User(name=name, email=email)
        # self.db.add(user)
        # await self.db.flush()  # Para obtener el ID sin commit
        # return user.id
        
        # OPÇÃO B: Con SQL raw (para este ejemplo)
        u = Users(name=name, email=email)
        self.db.add(u)
        # await self.db.commit()
        await self.db.flush()
        return u
    
    async def get_user_by_id(self, user_id: uuid.UUID):
        """Obtener usuario por ID"""
        if not self.db:
            raise ValueError("Database session not injected")
        
        user = await self.db.get(Users,user_id)
        
        if not user:
            raise HTTPException(status_code=404, detail="Customer not found")
        return user

    
    async def get_all_users(self):
        """Obtener todos los usuarios"""
        if not self.db:
            raise ValueError("Database session not injected")
            
        result = await self.db.execute(select(Users))
        return result.scalars().all()
    
    async def update_user(self, user_id: uuid.UUID, name: str|None, email: str|None):
        """Actualizar usuario"""
        if not self.db:
            raise ValueError("Database session not injected")
            
        user_to_update = UsersUpdate(name=name, email=email)
        
        u = await self.db.get(Users,user_id)

        if not u:
            raise HTTPException(status_code=404, detail="Customer not found")
        
        for key, value in user_to_update.updatable_fields().items():
            setattr(u, key, value)
        
        self.db.add(u)
        # await self.db.commit()
        await self.db.refresh(u)
        return u
    
    async def delete_user(self, user_id: uuid.UUID):
        """Eliminar usuario"""
        if not self.db:
            raise ValueError("Database session not injected")
            
        user = await self.db.get(Users,user_id)
        await self.db.delete(user)
        return True