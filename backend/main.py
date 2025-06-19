from typing import List

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session

from . import models, schemas
from .database import engine, SessionLocal

# Crea las tablas en la base de datos si no existen al iniciar la aplicación.
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Configuración de CORS para permitir peticiones desde el frontend de React.
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Dependencias ---

def get_db():
    """
    Dependencia de FastAPI para gestionar las sesiones de la base de datos.
    Asegura que la sesión se cierre siempre después de cada petición.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# --- Endpoints ---

@app.get("/")
def read_root():
    return {"message": "API de Gestión de Inventario"}

@app.get("/api/items/", response_model=List[schemas.Item])
def read_items(db: Session = Depends(get_db)):
    """
    Obtiene una lista de todos los ítems del inventario.
    """
    items = db.query(models.Item).order_by(models.Item.id).all()
    return items

@app.get("/api/movements/", response_model=List[schemas.Movement])
def read_movements(db: Session = Depends(get_db)):
    """
    Obtiene un historial de todos los movimientos de stock, ordenados por fecha.
    """
    movements = db.query(models.Movement).order_by(models.Movement.timestamp.desc()).all()
    return movements

@app.post("/api/items/{item_id}/adjust", response_model=schemas.Item)
def adjust_item_stock(item_id: int, adjustment: schemas.StockAdjustment, db: Session = Depends(get_db)):
    """
    Ajusta el stock de un ítem específico sumando o restando una cantidad.
    Registra la operación en el historial de movimientos.
    """
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()

    if not db_item:
        raise HTTPException(status_code=404, detail="Item not found")

    if db_item.stock + adjustment.change < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")

    if adjustment.change != 0:
        movement = models.Movement(item_id=item_id, change=adjustment.change)
        db.add(movement)
        db_item.stock += adjustment.change
        db.commit()
        db.refresh(db_item)

    return db_item

@app.delete("/api/movements/", status_code=204)
def clear_movements_history(db: Session = Depends(get_db)):
    """
    Borra todos los registros de la tabla de movimientos.
    """
    try:
        num_rows_deleted = db.query(models.Movement).delete(synchronize_session=False)
        db.commit()
        
        return {"detail": f"Successfully deleted {num_rows_deleted} movements."}
    
    except Exception as e:
        db.rollback() # Si algo sale mal, deshacemos la transacción.
        raise HTTPException(status_code=500, detail=f"An error occurred: {e}")