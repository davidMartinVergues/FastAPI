import logging
from logging.handlers import RotatingFileHandler
import os
from .settings import settings

class ColoredFormatter(logging.Formatter):
    """Formatter que agrega colores a los logs en consola"""
    
    # Códigos de color ANSI
    COLORS = {
        'DEBUG': '\033[36m',    # Cyan
        'INFO': '\033[32m',     # Verde
        'WARNING': '\033[33m',  # Amarillo
        'ERROR': '\033[31m',    # Rojo
        'CRITICAL': '\033[91m', # Rojo brillante
        'ENDC': '\033[0m'       # Reset color
    }

    def format(self, record):
        # Formatear el mensaje base
        log_message = super().format(record)
        # Agregar color basado en el nivel
        color = self.COLORS.get(record.levelname, self.COLORS['ENDC'])
        return f"{color}{log_message}{self.COLORS['ENDC']}"

# Flag global para evitar configuración múltiple
_loggers_configured = False

def setup_loggers():
    """Configura todos los loggers de la aplicación"""
    global _loggers_configured
    
    # Si ya están configurados, no hacer nada
    if _loggers_configured:
        print("⚠️  Loggers ya configurados, omitiendo...")
        return

    # Crear directorio logs si no existe
    os.makedirs("logs", exist_ok=True)

    # Configurar cada logger según la configuración
    for logger_name, config in settings.logging.loggers_config.items():
        logger = logging.getLogger(logger_name)
        logger.setLevel(getattr(logging, config["level"]))

        # Limpiar handlers existentes para evitar duplicación
        for handler in logger.handlers[:]:
            logger.removeHandler(handler)

        # Handler con rotación de archivos
        file_handler = RotatingFileHandler(
            config["file"],
            maxBytes=settings.logging.max_size_mb * 1024 * 1024,
            backupCount=settings.logging.backup_count
        )

        # Handler para consola
        console_handler = logging.StreamHandler()

        # Formato específico para cada servicio
        file_formatter = logging.Formatter(config["format"])  # Sin colores para archivos
        console_formatter = ColoredFormatter(config["format"])  # Con colores para consola
        
        file_handler.setFormatter(file_formatter)
        console_handler.setFormatter(console_formatter)

        # Agregar ambos handlers
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)
        
        # Evitar propagación al root logger
        logger.propagate = False

    _loggers_configured = True
    print("✅ Loggers configurados correctamente")