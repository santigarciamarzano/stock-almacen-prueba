from datetime import datetime
from pydantic import BaseModel, ConfigDict

# --- Esquemas para la API ---
# Estos modelos de Pydantic definen la forma de los datos para las peticiones
# y respuestas de la API. Proporcionan validación automática y documentación.

class Movement(BaseModel):
    """Esquema para devolver un movimiento de stock."""
    id: int
    item_id: int
    change: int
    timestamp: datetime

    # Permite que Pydantic cree el modelo a partir de un objeto ORM de SQLAlchemy.
    model_config = ConfigDict(from_attributes=True)


class Item(BaseModel):
    """Esquema principal para un ítem del inventario."""
    id: int
    sku: str
    ean13: str
    stock: int

    model_config = ConfigDict(from_attributes=True)


# --- Esquemas para Cuerpos de Petición (Request Bodies) ---

class StockAdjustment(BaseModel):
    """Esquema para el cuerpo de la petición de ajuste de stock."""
    change: int