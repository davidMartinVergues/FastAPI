from pydantic_settings import BaseSettings, SettingsConfigDict
from pathlib import Path
from pydantic import BaseModel, Field, field_validator, model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal, Any

BASE_DIR = Path(__file__).resolve().parent.parent  # ✔️ pathlib compatible

class DatabaseConfig(BaseModel):
    """Configuración de base de datos"""
    USER_DB: str = ""
    PSW_DB: str = ""
    HOST_DB: str = ""
    NAME_DB: str = ""
    PORT_DB: str = ""
    POOL_SIZE: int = Field(default=10, ge=1, le=50)
    MAX_OVERFLOW: int = Field(default=20, ge=0, le=100)
    ECHO: bool = False
    
    @property
    def url_async(self) -> str:
        return f"postgresql+asyncpg://{self.USER_DB}:{self.PSW_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.NAME_DB}"
    
    @property
    def url_sync(self) -> str:
        return f"postgresql://{self.USER_DB}:{self.PSW_DB}@{self.HOST_DB}:{self.PORT_DB}/{self.NAME_DB}"
    
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
    secret_key: str = Field(default="secret", min_length=2)
    environment: Literal["development", "testing", "staging", "production"] = "development"
    cors_origins: list[str] = ["http://localhost:3000"]
    
    @field_validator('secret_key')
    def validate_secret_key(cls, v):
        if len(v) < 2:
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
    
    @field_validator('secret_key')
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
    max_size_mb: int = Field(default=100, ge=1)
    backup_count: int = Field(default=10, ge=1)
    
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
        env_file=BASE_DIR / ".env",
        env_file_encoding="utf-8",
        env_nested_delimiter="__",  # Para variables con prefijo en funcion de la variable en este caso DATABASE__HOST_DB
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
