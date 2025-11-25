from pathlib import Path
from dotenv import load_dotenv
import os, sys

# Carga .env desde la carpeta backend (donde está este archivo)
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)

# Log mínimo para confirmar
if not os.getenv("SUPABASE_URL") or not os.getenv("SUPABASE_SERVICE_KEY"):
    print("WARNING: No se encontraron variables de Supabase en .env")
else:
    print("OK: Variables de Supabase cargadas desde", ENV_PATH)

from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from supabase import Client
import traceback, asyncio
from typing import List, Dict, Any

# Importar utils
sys.path.insert(0, str(Path(__file__).parent))
from utils.supabase_client import get_supabase_client

# Importar los routers
from routers import reports as reports_router
from routers import reports_labels as reports_labels_router
from routers import matches as matches_router
from routers import ai_search as ai_search_router
from routers import embeddings_supabase as embeddings_router
from routers import rag_search as rag_router
from routers import direct_matches as direct_matches_router
from routers import fix_embeddings as fix_embeddings_router
from routers import pets as pets_router

# =========================
# Configuración base
# =========================
BASE_DIR = Path(__file__).parent                 # carpeta: .../backend

# Configuración de Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_SERVICE_KEY") or os.getenv("SUPABASE_ANON_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    print("WARNING: Variables de Supabase no encontradas en .env")
    supabase_client = None
else:
    try:
        supabase_client: Client = get_supabase_client()
        print("✅ Cliente de Supabase creado con configuración optimizada")
    except Exception as e:
        print(f"❌ Error creando cliente de Supabase: {e}")
        supabase_client = None

# Orígenes permitidos (para el front). En .env podés setear:
# ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
ALLOWED_ORIGINS = [o.strip() for o in os.getenv("ALLOWED_ORIGINS", "*").split(",") if o.strip()]

# =========================
# App FastAPI
# =========================
app = FastAPI(title="PetAlert API", version="1.5.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS if ALLOWED_ORIGINS else ["*"],  # WARNING: en prod, especificar dominios
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =========================
# Startup: Pre-cargar MegaDescriptor
# =========================
@app.on_event("startup")
async def startup_event():
    """Pre-carga el modelo MegaDescriptor al iniciar el servidor"""
    generate_locally = os.getenv("GENERATE_EMBEDDINGS_LOCALLY", "false").lower() in ("1", "true", "yes")
    
    if generate_locally:
        print("🔄 Pre-cargando modelo MegaDescriptor...")
        try:
            from services.embeddings import _load_model
            _load_model()
            print("✅ MegaDescriptor pre-cargado. Los embeddings se generarán rápidamente.")
        except Exception as e:
            print(f"⚠️ Error pre-cargando MegaDescriptor: {e}")
            print("   El modelo se cargará en la primera petición (puede tardar ~60s)")
    else:
        print("ℹ️ Generación local de embeddings desactivada (GENERATE_EMBEDDINGS_LOCALLY=false)")

# Incluir los routers
app.include_router(reports_router.router)
app.include_router(reports_labels_router.router)
app.include_router(matches_router.router)
app.include_router(ai_search_router.router)
app.include_router(embeddings_router.router)
app.include_router(rag_router.router)
app.include_router(direct_matches_router.router)
app.include_router(fix_embeddings_router.router)
app.include_router(pets_router.router)

# =========================
# Helpers
# =========================
async def _save_to_supabase(data: Dict[str, Any]) -> bool:
    """
    Guarda datos en Supabase si está configurado.
    Retorna True si se guardó exitosamente, False en caso contrario.
    """
    if not supabase_client:
        return False
    
    try:
        # Aquí puedes agregar la lógica para guardar en Supabase
        # Por ejemplo, guardar análisis de imágenes en una tabla
        result = supabase_client.table("image_analyses").insert(data).execute()
        return True
    except Exception as e:
        print(f"Error guardando en Supabase: {e}")
        return False

# =========================
# Endpoints
# =========================
@app.get("/health")
async def health():
    """Endpoint de salud para verificar que la API está funcionando."""
    supabase_status = "conectado" if supabase_client else "no configurado"
    return {
        "status": "ok", 
        "message": "PetAlert API activa",
        "supabase": supabase_status
    }

@app.get("/version")
async def version():
    """Endpoint para obtener información de la versión."""
    return {
        "version": app.version, 
        "allowed_origins": ALLOWED_ORIGINS or ["*"],
        "features": ["embeddings", "supabase" if supabase_client else "no_supabase"]
    }

# =========================
# Endpoint adicional para Supabase
# =========================
@app.get("/supabase/status")
async def supabase_status():
    """Verifica el estado de la conexión con Supabase."""
    if not supabase_client:
        return {"status": "no_configurado", "message": "Variables de Supabase no encontradas"}
    
    try:
        # Intentar una consulta simple para verificar la conexión
        result = supabase_client.table("image_analyses").select("id").limit(1).execute()
        return {"status": "conectado", "message": "Conexión exitosa con Supabase"}
    except Exception as e:
        return {"status": "error", "message": f"Error conectando con Supabase: {e}"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)