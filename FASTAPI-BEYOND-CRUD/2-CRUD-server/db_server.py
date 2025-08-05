from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Configuraci�n de la base de datos PostgreSQL
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/fastapi-beyond-crud")

# Crear el motor de SQLAlchemy
engine = create_engine(DATABASE_URL)

# Crear una clase base para los modelos
Base = declarative_base()

# Configurar el sessionmaker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Funci�n para obtener la sesi�n de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()