from fastapi import APIRouter, HTTPException, Query
from typing import List, Dict, Any, Optional
import os, math, sys
from pathlib import Path
from supabase import Client

# Agregar la carpeta parent al path para poder importar utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.supabase_client import get_supabase_client

router = APIRouter(prefix="/matches", tags=["matches"])

def _sb() -> Client:
    """Crea un cliente de Supabase con configuración optimizada de timeouts"""
    try:
        return get_supabase_client()
    except Exception as e:
        raise HTTPException(500, f"Error conectando a Supabase: {str(e)}")

def _coords(loc: Optional[dict]) -> Optional[tuple]:
    # GeoJSON {"type":"Point","coordinates":[lon,lat]}
    if isinstance(loc, dict) and "coordinates" in loc:
        lon, lat = loc["coordinates"]; return (lat, lon)
    return None

def haversine_km(lat1, lon1, lat2, lon2):
    R=6371.0
    dlat=math.radians(lat2-lat1); dlon=math.radians(lon2-lon1)
    a=math.sin(dlat/2)**2+math.cos(math.radians(lat1))*math.cos(math.radians(lat2))*math.sin(dlon/2)**2
    return 2*R*math.asin(math.sqrt(a))

def label_set(labels_json) -> set:
    if not labels_json: return set()
    items = labels_json.get("labels") if isinstance(labels_json, dict) else None
    if not isinstance(items, list): return set()
    return {(it.get("label") or it.get("description") or "").lower() for it in items if it}

@router.get("/auto-match")
def auto_match(report_id: str = Query(...), radius_km: float = 10.0, top_k: int = 5):
    sb = _sb()
    base = sb.table("reports").select("*").eq("id", report_id).single().execute().data
    if not base: raise HTTPException(404, "Reporte base no encontrado")

    base_pt = _coords(base.get("location"))
    if not base_pt: raise HTTPException(400, "El reporte base no tiene location válido (GeoJSON Point)")
    base_lat, base_lon = base_pt
    base_labels = label_set(base.get("labels"))
    target_type = "found" if base.get("type") == "lost" else "lost"

    candidates = sb.table("reports").select("*") \
        .eq("type", target_type).eq("status", "active").eq("species", base.get("species")).execute().data

    results: List[Dict[str, Any]] = []
    lat_pad = radius_km/111.0; lon_pad = radius_km/111.0

    for c in candidates:
        pt = _coords(c.get("location"))
        if not pt: continue
        lat, lon = pt
        if not (base_lat-lat_pad <= lat <= base_lat+lat_pad and base_lon-lon_pad <= lon <= base_lon+lon_pad):
            continue
        d = haversine_km(base_lat, base_lon, lat, lon)
        if d > radius_km: continue

        overlap = len(base_labels & label_set(c.get("labels")))
        score = overlap*10 - d*0.2
        results.append({
            "candidate": {
                "id": c["id"], "pet_name": c.get("pet_name"), "species": c.get("species"),
                "color": c.get("color"), "location": c.get("location"),
                "photo": (c.get("photos") or [None])[0] if isinstance(c.get("photos"), list) else None,
                "labels": c.get("labels"),
            },
            "distance_km": round(d,2),
            "label_overlap": overlap,
            "score": round(score,3)
        })

    results.sort(key=lambda x: x["score"], reverse=True)
    return {"report_id": report_id, "radius_km": radius_km, "total_candidates": len(results), "top_k": results[:top_k]}


@router.get("/pending")
async def get_pending_matches(
    user_id: Optional[str] = Query(None, description="ID del usuario para filtrar matches de sus reportes"),
    report_id: Optional[str] = Query(None, description="ID del reporte específico para obtener sus matches"),
    status: str = Query("pending", description="Estado de los matches (pending, accepted, rejected)")
):
    """
    Obtiene matches pendientes para un usuario o un reporte específico.
    
    Si se proporciona user_id, retorna todos los matches de reportes del usuario.
    Si se proporciona report_id, retorna todos los matches de ese reporte.
    """
    try:
        sb = _sb()
        
        if report_id:
            # Obtener matches de un reporte específico
            # Puede ser lost_report_id o found_report_id
            matches_lost = sb.table("matches").select("*").eq("lost_report_id", report_id).eq("status", status).execute()
            matches_found = sb.table("matches").select("*").eq("found_report_id", report_id).eq("status", status).execute()
            
            all_matches = (matches_lost.data or []) + (matches_found.data or [])
            
            # Enriquecer con información de los reportes relacionados
            enriched_matches = []
            for match in all_matches:
                lost_id = match.get("lost_report_id")
                found_id = match.get("found_report_id")
                
                # Obtener reporte perdido
                lost_report = None
                if lost_id:
                    lost_result = sb.table("reports").select("id, type, pet_name, species, photos, description, location, created_at").eq("id", lost_id).single().execute()
                    lost_report = lost_result.data if lost_result.data else None
                
                # Obtener reporte encontrado
                found_report = None
                if found_id:
                    found_result = sb.table("reports").select("id, type, pet_name, species, photos, description, location, created_at").eq("id", found_id).single().execute()
                    found_report = found_result.data if found_result.data else None
                
                enriched_matches.append({
                    "match_id": match.get("id"),
                    "similarity_score": match.get("similarity_score"),
                    "matched_by": match.get("matched_by"),
                    "status": match.get("status"),
                    "created_at": match.get("created_at"),
                    "lost_report": lost_report,
                    "found_report": found_report
                })
            
            return {
                "matches": enriched_matches,
                "count": len(enriched_matches),
                "report_id": report_id
            }
        
        elif user_id:
            # Obtener matches de todos los reportes del usuario
            # Primero obtener todos los reportes del usuario
            user_reports = sb.table("reports").select("id").eq("reporter_id", user_id).execute()
            report_ids = [r["id"] for r in (user_reports.data or [])]
            
            if not report_ids:
                return {"matches": [], "count": 0, "user_id": user_id}
            
            # Obtener matches donde los reportes del usuario están involucrados
            matches_lost = sb.table("matches").select("*").in_("lost_report_id", report_ids).eq("status", status).execute()
            matches_found = sb.table("matches").select("*").in_("found_report_id", report_ids).eq("status", status).execute()
            
            all_matches = (matches_lost.data or []) + (matches_found.data or [])
            
            # Enriquecer con información de los reportes (similar al caso anterior)
            enriched_matches = []
            for match in all_matches:
                lost_id = match.get("lost_report_id")
                found_id = match.get("found_report_id")
                
                lost_report = None
                if lost_id:
                    lost_result = sb.table("reports").select("id, type, pet_name, species, photos, description, location, created_at").eq("id", lost_id).single().execute()
                    lost_report = lost_result.data if lost_result.data else None
                
                found_report = None
                if found_id:
                    found_result = sb.table("reports").select("id, type, pet_name, species, photos, description, location, created_at").eq("id", found_id).single().execute()
                    found_report = found_result.data if found_result.data else None
                
                enriched_matches.append({
                    "match_id": match.get("id"),
                    "similarity_score": match.get("similarity_score"),
                    "matched_by": match.get("matched_by"),
                    "status": match.get("status"),
                    "created_at": match.get("created_at"),
                    "lost_report": lost_report,
                    "found_report": found_report
                })
            
            return {
                "matches": enriched_matches,
                "count": len(enriched_matches),
                "user_id": user_id
            }
        else:
            raise HTTPException(400, "Debe proporcionar user_id o report_id")
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error obteniendo matches pendientes: {str(e)}")


@router.put("/{match_id}/status")
async def update_match_status(
    match_id: str,
    status: str = Query(..., description="Nuevo estado del match (accepted, rejected)")
):
    """
    Actualiza el estado de un match (aceptado o rechazado).
    """
    try:
        if status not in ["accepted", "rejected"]:
            raise HTTPException(400, "El estado debe ser 'accepted' o 'rejected'")
        
        sb = _sb()
        
        result = sb.table("matches").update({"status": status}).eq("id", match_id).execute()
        
        if not result.data or len(result.data) == 0:
            raise HTTPException(404, f"Match {match_id} no encontrado")
        
        return {
            "success": True,
            "match_id": match_id,
            "status": status,
            "message": f"Match {status} exitosamente"
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error actualizando estado del match: {str(e)}")