"""
PATRÓN PROFESIONAL: Service Layer con @with_transaction
================================================

Este Service demuestra el patrón profesional de arquitectura en capas:
- Lógica de negocio separada del HTTP
- Transacciones automáticas
- Inyección automática de sesiones en repositories
"""

import uuid
from db.db import with_transaction
from .user_repository import UserRepository


class UserService:
    """
    PASO 2: SERVICE LAYER
    
    - Contiene la lógica de negocio
    - Usa @with_transaction para manejo automático de transacciones
    - Coordina múltiples repositories
    - No conoce nada sobre HTTP/FastAPI
    """
    
    def __init__(self):
        # PASO 2.1: Inicializar repositories
        # Cada repository hereda de IAsyncDatabaseRepository
        self.user_repo = UserRepository()
        
        # En un caso real tendrías múltiples repositories:
        # self.profile_repo = ProfileRepository()
        # self.notification_repo = NotificationRepository()
        # self.audit_repo = AuditRepository()
    
    @with_transaction  # ← PASO 2.2: AQUÍ OCURRE LA MAGIA
    async def create_user_with_profile(self, name: str, email: str):
        """
        CASO DE USO: Crear usuario con perfil completo
        
        ¿Qué hace @with_transaction?
        1. Crea una nueva sesión de DB
        2. Busca todos los repositories en self.*_repo
        3. Inyecta automáticamente la sesión en cada repository (self.user_repo.db = session)
        4. Ejecuta esta función
        5. Si todo OK → commit automático
        6. Si hay error → rollback automático
        7. Siempre → close automático
        """
        
        # PASO 2.3: Lógica de negocio - Coordinar múltiples operaciones
        
        # Operación 1: Crear usuario base
        user = await self.user_repo.create_user(name, email)
        
        # Operación 2: Crear perfil por defecto (simulado)
        # profile_id = await self.profile_repo.create_profile(user_id, "default")
        
        # Operación 3: Enviar notificación de bienvenida (simulado) 
        # await self.notification_repo.create_notification(
        #     user_id, "¡Bienvenido a la plataforma!"
        # )
        
        # Operación 4: Registrar en auditoría (simulado)
        # await self.audit_repo.log_user_creation(user_id, email)
        
        # IMPORTANTE: Si cualquier await falla, TODO se revierte automáticamente
        # No necesitas try/catch para manejo de transacciones
        
        return user
    
    @with_transaction
    async def update_user_transactional(self, user_id: uuid.UUID, name: str|None, email: str|None):
        """
        CASO DE USO: Actualización transaccional con validaciones
        
        Demuestra cómo el rollback automático funciona cuando hay errores
        """
        
        # Paso 1: Validar que el usuario existe
        existing_user = await self.user_repo.get_user_by_id(user_id)
        if not existing_user:
            # Esta excepción activará rollback automático
            raise ValueError(f"Usuario con ID {user_id} no encontrado")
        
        # Paso 2: Actualizar datos del usuario
        updated_user = await self.user_repo.update_user(user_id, name, email)
        
        # Paso 3: Validaciones de negocio (pueden fallar)
        if email and "@" not in email:
            # Esta excepción activará rollback automático
            raise ValueError("Email inválido")
        
        # Paso 4: Operaciones adicionales (simuladas)
        # await self.audit_repo.log_user_update(user_id, name, email)
        # await self.notification_repo.notify_profile_updated(user_id)
        
        # Si llegamos aquí, commit automático
        return updated_user
    
    @with_transaction
    async def delete_user_cascade(self, user_id: uuid.UUID):
        """
        CASO DE USO: Eliminación en cascada
        
        Operación compleja que debe ser completamente transaccional.
        Si cualquier paso falla, TODO se revierte.
        """
        
        # Paso 1: Eliminar notificaciones del usuario
        # await self.notification_repo.delete_by_user_id(user_id)
        
        # Paso 2: Eliminar perfil del usuario  
        # await self.profile_repo.delete_by_user_id(user_id)
        
        # Paso 3: Eliminar sesiones activas
        # await self.session_repo.delete_by_user_id(user_id)
        
        # Paso 4: Eliminar usuario principal
        await self.user_repo.delete_user(user_id)
        
        # Paso 5: Registrar eliminación en auditoría
        # await self.audit_repo.log_user_deletion(user_id)
        
        # Si cualquier paso falla, TODA la operación se revierte
        # Esto garantiza que no queden datos huérfanos
        
        return {"message": "Usuario eliminado completamente"}


# =============================================================================
# RESUMEN DEL PATRÓN @with_transaction
# =============================================================================

"""
🎯 REGLAS DE ORO PARA USAR @with_transaction:

1. SOLO en métodos de SERVICE LAYER
   ✅ class UserService: @with_transaction async def method(self):
   ❌ En controllers/routers
   ❌ En repositories  
   ❌ En funciones standalone

2. Repositories SIEMPRE heredan de IAsyncDatabaseRepository
   ✅ class UserRepository(IAsyncDatabaseRepository):
   ❌ class UserRepository: # Sin herencia

3. Un @with_transaction = Una transacción completa
   ✅ Una operación de negocio = un método con @with_transaction
   ❌ Múltiples @with_transaction en una misma operación

4. No manejes transacciones manualmente dentro del service
   ❌ await session.commit() # @with_transaction ya lo hace
   ❌ await session.rollback() # @with_transaction ya lo hace
   ✅ Solo lanza excepciones si algo está mal

5. Validaciones de negocio con excepciones
   ✅ raise ValueError("Email inválido") # Activa rollback automático
   ✅ raise BusinessException("Stock insuficiente") 

✨ VENTAJAS:
- Código limpio sin boilerplate de transacciones
- Rollback automático en cualquier error
- Inyección automática de sesiones
- Arquitectura en capas bien definida
- Fácil testing (services independientes)
"""