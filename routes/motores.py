
from fastapi import APIRouter, Depends, HTTPException, status
import psycopg
from typing import List
from datetime import date
import uuid

# Importamos el conector y los esquemas
from .. import schemas
from ..dbmanager import get_db_cursor

# 1. Crear el Router
router = APIRouter(
    prefix="/motores", 
    tags=["Motores"],
)

# --------------------------
# ENDPOINTS CRUD
# --------------------------

# Función auxiliar para convertir el resultado del cursor a Motor
def map_row_to_motor(row: dict) -> schemas.Motor:
    return schemas.Motor(
        id=row['id'],
        nombre_modelo=row['nombre_modelo'],
        litraje=row['litraje'],
        potencia_hp=row['potencia_hp'],
        fecha_lanzamiento=row['fecha_lanzamiento'],
        marca_id=row['marca_id'],
        tipo_motor_id=row['tipo_motor_id'],
    )

# 1. READ ALL (Lectura de todos los motores)
@router.get("/", response_model=List[schemas.Motor])
def read_motores(cursor: psycopg.Cursor = Depends(get_db_cursor)):
    # Nota: Los nombres de las columnas deben coincidir exactamente con el esquema
    cursor.execute('SELECT * FROM "motores";')
    results = cursor.fetchall()
    return [map_row_to_motor(row) for row in results]

# 2. READ ONE (Lectura de un motor por ID)
@router.get("/{motor_id}", response_model=schemas.Motor)
def read_motor(motor_id: str, cursor: psycopg.Cursor = Depends(get_db_cursor)):
    cursor.execute('SELECT * FROM "motores" WHERE id = %s;', (motor_id,))
    motor_data = cursor.fetchone()
    
    if motor_data is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motor no encontrado")
        
    return map_row_to_motor(motor_data)

# 3. CREATE (Creación de un nuevo motor)
@router.post("/", response_model=schemas.Motor, status_code=status.HTTP_201_CREATED)
def create_motor(motor: schemas.MotorCreate, cursor: psycopg.Cursor = Depends(get_db_cursor)):
    new_uuid = str(uuid.uuid4())
    
    try:
        cursor.execute(
            # Consulta INSERT, usa RETURNING para devolver el motor completo (solo necesitas el ID si es autogenerado, pero aquí lo generamos nosotros)
            'INSERT INTO "motores" (id, nombre_modelo, litraje, potencia_hp, fecha_lanzamiento, marca_id, tipo_motor_id) '
            'VALUES (%s, %s, %s, %s, %s, %s, %s) RETURNING *;',
            (
                new_uuid, 
                motor.nombre_modelo, 
                motor.litraje, 
                motor.potencia_hp, 
                motor.fecha_lanzamiento, 
                motor.marca_id, 
                motor.tipo_motor_id
            )
        )
        # Obtenemos el registro insertado
        db_motor = cursor.fetchone() 
        return map_row_to_motor(db_motor)
        
    except psycopg.Error as e:
        # En caso de error (ej. clave foránea inexistente o dato inválido)
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error de base de datos: {e.diag.message_primary}")

# 4. DELETE (Eliminación de un motor)
@router.delete("/{motor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_motor(motor_id: str, cursor: psycopg.Cursor = Depends(get_db_cursor)):
    cursor.execute('DELETE FROM "motores" WHERE id = %s RETURNING id;', (motor_id,))
    
    if cursor.rowcount == 0:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motor no encontrado")
        
    return 

# 5. UPDATE (Actualización de un motor)
@router.put("/{motor_id}", response_model=schemas.Motor)
def update_motor(motor_id: str, motor_update: schemas.MotorCreate, cursor: psycopg.Cursor = Depends(get_db_cursor)):
    
    # Preparamos los campos y valores para la consulta
    fields = motor_update.model_dump()
    set_clauses = ', '.join([f'"{key}" = %s' for key in fields.keys()])
    values = list(fields.values())
    
    # Agregamos el ID para la cláusula WHERE
    values.append(motor_id) 

    try:
        cursor.execute(
            f'UPDATE "motores" SET {set_clauses} WHERE id = %s RETURNING *;',
            values
        )
        
        updated_motor = cursor.fetchone()
        
        if updated_motor is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Motor no encontrado")
            
        return map_row_to_motor(updated_motor)

    except psycopg.Error as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f"Error de base de datos: {e.diag.message_primary}")