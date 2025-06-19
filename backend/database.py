from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# URL de conexión a la base de datos PostgreSQL.
# Se recomienda gestionar esto con variables de entorno en un entorno de producción.
SQLALCHEMY_DATABASE_URL = "postgresql://myuser:mysecretpassword@localhost:5432/inventorydb"

# El motor de SQLAlchemy que gestiona la conexión con la base de datos.
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# Fábrica de sesiones que se utilizará para crear sesiones de base de datos
# para cada petición a través de las dependencias de FastAPI.
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base declarativa que utilizarán los modelos de SQLAlchemy.
Base = declarative_base()