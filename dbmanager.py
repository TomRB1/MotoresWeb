# dbmanager.py
# Basado en tu API funcional (usando psycopg3 y SSL)

import os
import psycopg
from psycopg.rows import dict_row
from typing import Generator

# IMPORTANTE: En Vercel, la variable de entorno se llama "DATABASE_URL"
# Si en tu API funcional la llamas diferente, cambia os.environ.get("DATABASE_URL")
DATABASE_URL = os.environ.get("DATABASE_URL")

if not DATABASE_URL:
    raise Exception("La variable de entorno DATABASE_URL no está configurada en Vercel.")

def get_db_cursor() -> Generator[psycopg.Cursor, None, None]:
    """
    Función de dependencia que establece y gestiona la conexión a PostgreSQL (Supabase).
    Utiliza psycopg3 y fuerza el modo SSL para la conexión segura.
    """
    conn = None
    cursor = None
    try:
        # 1. Conexión: usa el driver psycopg.
        # 2. SSL: Usa sslmode="require" para la conexión segura a Supabase.
        # 3. dict_row: Para que los resultados se devuelvan como diccionarios.
        conn = psycopg.connect(
            DATABASE_URL,
            row_factory=dict_row,
            sslmode="require" 
        )
        cursor = conn.cursor()
        
        yield cursor
        
        # Si no hubo errores, confirmamos la transacción (COMMIT)
        conn.commit()
    except Exception as e:
        if conn:
            conn.rollback() # En caso de error, deshacemos la transacción
        print(f"Error de conexión o transacción: {e}")
        # En una API en producción, podríamos relanzar el error o manejarlo con HTTPException.
    finally:
        # Cerramos la conexión y el cursor
        if cursor:
            cursor.close()
        if conn:
            conn.close()