from fastapi import APIRouter, HTTPException, Path, Body
from typing import Any, Dict
import os, sys
from pathlib import Path as PathLib
from supabase import Client

# Agregar la carpeta parent al path para poder importar utils
sys.path.insert(0, str(PathLib(__file__).parent.parent))
from utils.supabase_client import get_supabase_client

router = APIRouter(prefix="/reports", tags=["reports"])

def _sb() -> Client:
    """Crea un cliente de Supabase con configuración optimizada de timeouts"""
    try:
        return get_supabase_client()
    except Exception as e:
        raise HTTPException(500, f"Error conectando a Supabase: {str(e)}")

@router.post("/{report_id}/labels")
def save_labels(report_id: str = Path(...), payload: Dict[str, Any] = Body(...)):
    if "labels" not in payload or not isinstance(payload["labels"], list):
        raise HTTPException(400, "Se espera {'labels': [...]}")

    sb = _sb()
    res = sb.table("reports").update({"labels": payload}).eq("id", report_id).execute()
    if not res.data:
        raise HTTPException(404, "Reporte no encontrado")
    return {"ok": True, "updated": res.data[0]["id"]}