# models.py

from sqlalchemy import Column, Integer, String, ForeignKey, Numeric, Date
from sqlalchemy.orm import relationship
from .database import Base

# --- Tablas de Referencia ---

class Marca(Base):
    __tablename__ = "marcas"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    motores = relationship("Motor", back_populates="marca")

class TipoMotor(Base):
    __tablename__ = "tipos_motor"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, unique=True, index=True)
    motores = relationship("Motor", back_populates="tipo")

# --- Tabla Principal ---

class Motor(Base):
    __tablename__ = "motores"
    
    # Supabase usa UUID para el ID, que mapeamos a String
    id = Column(String, primary_key=True, index=True) 
    nombre_modelo = Column(String, index=True)
    litraje = Column(Numeric(3, 1))
    potencia_hp = Column(Integer, nullable=True)
    fecha_lanzamiento = Column(Date, nullable=True)

    # Claves Foráneas
    marca_id = Column(Integer, ForeignKey("marcas.id"))
    tipo_motor_id = Column(Integer, ForeignKey("tipos_motor.id"))

    # Definición de relaciones
    marca = relationship("Marca", back_populates="motores")
    tipo = relationship("TipoMotor", back_populates="motores")