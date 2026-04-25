from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import httpx

# 1. PRIMERO creas la instancia de FastAPI
app = FastAPI(title="Panel Admin ETL API")

# 2. SEGUNDO configuras los middlewares (CORS)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_methods=["*"],
    allow_headers=["*"],
)

# 3. TERCERO defines las rutas
@app.get("/")
def home():
    return {"status": "online", "message": "Backend de Byron listo"}

@app.get("/combustibles")
async def get_combustibles():
    url = "https://api.bencinaenlinea.cl/api/combustible_ciudadano"
    
    try:
        async with httpx.AsyncClient() as client:
            # Importante: usar 'await' porque la función es 'async'
            response = await client.get(url, timeout=10.0)
            response.raise_for_status()
            raw_data = response.json()
        
        # Transformación simple (ETL)
        lista_limpia = []
        for item in raw_data.get('data', []):
            lista_limpia.append({
                "id": item.get('id'),
                "nombre": item.get('nombre_largo'),
                "tipo": item.get('tipo_atencion_nombre'),
                "actualizado": item.get('fecha_creacion')
            })
        
        return lista_limpia
        
    except Exception as e:
        return {"error": "Error de conexión", "detalle": str(e)}