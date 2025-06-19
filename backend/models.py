from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func

# Base declarativa de SQLAlchemy de la que heredarán todos los modelos.
Base = declarative_base()

class Item(Base):
    """
    Modelo de SQLAlchemy que representa un ítem en el inventario.
    """
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    sku = Column(String, unique=True, index=True, nullable=False)
    ean13 = Column(String, unique=True, index=True, nullable=False)
    stock = Column(Integer, default=0, nullable=False)

class Movement(Base):
    """
    Modelo de SQLAlchemy que representa un movimiento de stock (entrada o salida).
    """
    __tablename__ = "movements"

    id = Column(Integer, primary_key=True, index=True)
    item_id = Column(Integer, ForeignKey("items.id"), nullable=False)
    change = Column(Integer, nullable=False)
    
    # El timestamp se genera automáticamente a nivel de base de datos.
    timestamp = Column(DateTime(timezone=True), server_default=func.now())