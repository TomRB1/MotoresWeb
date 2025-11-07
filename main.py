from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# Importamos el router de motores
from routes import motores 

app = FastAPI(
    title="API CRUD de Motores (psycopg3)",
    description="API RESTful para la gestión del catálogo de motores con FastAPI y Supabase.",
    version="1.0.0"
)

# Configuración CORS (puedes ajustar los orígenes si es necesario)
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluimos el router de motores
app.include_router(motores.router)

# Ruta base o 'health check'
@app.get("/", tags=["Root"])
def read_root():
    return {"message": "API de Motores activa. Ve a /docs para la documentación."}