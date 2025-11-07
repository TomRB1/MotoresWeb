# schemas.py
from pydantic import BaseModel
from typing import Optional
from datetime import date

# Esquemas para las Tablas de Referencia (solo lectura de IDs y Nombres)
class MarcaBase(BaseModel):
    id: int
    nombre: str

class TipoMotorBase(BaseModel):
    id: int
    nombre: str

# Esquema para CREAR/ACTUALIZAR un Motor
class MotorCreate(BaseModel):
    nombre_modelo: str
    litraje: float
    potencia_hp: Optional[int] = None
    fecha_lanzamiento: Optional[date] = None
    marca_id: int  # Clave foránea (FK)
    tipo_motor_id: int  # Clave foránea (FK)

# Esquema para LEER y DEVOLVER un Motor (Respuesta final)
class Motor(MotorCreate):
    # El ID es un string (UUID) generado por la DB
    id: str
    
    # Opcionalmente, puedes incluir los nombres de las marcas/tipos
    # Para simplificar, solo devolveremos los IDs en esta versión