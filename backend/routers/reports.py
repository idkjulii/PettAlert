from fastapi import APIRouter, HTTPException, Query, Body, BackgroundTasks
from typing import List, Dict, Any, Optional
import os, math
from supabase import create_client, Client
import httpx
import asyncio
from services.embeddings import image_bytes_to_vec
from routers.n8n_integration import send_to_n8n_webhook, get_n8n_webhook_url

router = APIRouter(prefix="/reports", tags=["reports"])

def _sb() -> Client:
    url = os.getenv("SUPABASE_URL"); key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise HTTPException(500, "Faltan SUPABASE_URL / SUPABASE_SERVICE_KEY")
    return create_client(url, key)

def _extract_coords(location_data) -> Optional[tuple]:
    """Extrae coordenadas de diferentes formatos de location"""
    if not location_data:
        return None
    
    # Formato PostGIS: "SRID=4326;POINT(lon lat)"
    if isinstance(location_data, str) and "POINT(" in location_data:
        try:
            # Extraer coordenadas del string POINT
            coords_str = location_data.split("POINT(")[1].split(")")[0]
            lon, lat = map(float, coords_str.split())
            return (lat, lon)
        except:
            return None
    
    # Formato GeoJSON: {"type":"Point","coordinates":[lon,lat]}
    if isinstance(location_data, dict) and "coordinates" in location_data:
        try:
            lon, lat = location_data["coordinates"]
            return (lat, lon)
        except:
            return None
    
    return None

def haversine_km(lat1, lon1, lat2, lon2):
    """Calcula distancia en kilómetros entre dos puntos"""
    R = 6371.0
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return 2 * R * math.asin(math.sqrt(a))

async def generate_and_save_embedding(report_id: str, photo_url: str):
    """
    Genera y guarda el embedding de una imagen para un reporte.
    Se ejecuta en segundo plano para no bloquear la respuesta.
    """
    try:
        print(f"🔄 [embedding] Generando embedding para reporte {report_id} desde {photo_url}")
        
        # Descargar la imagen
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(photo_url)
            response.raise_for_status()
            image_bytes = response.content
        
        # Generar embedding
        vec = image_bytes_to_vec(image_bytes)
        vec_list = vec.tolist()
        
        # Guardar en Supabase usando RPC
        sb = _sb()
        result = sb.rpc('update_report_embedding', {
            'report_id': report_id,
            'embedding_vector': vec_list
        }).execute()
        
        if result.data:
            print(f"✅ [embedding] Embedding guardado exitosamente para reporte {report_id}")
        else:
            print(f"⚠️ [embedding] No se pudo guardar embedding para reporte {report_id}")
            
    except Exception as e:
        print(f"❌ [embedding] Error generando embedding para reporte {report_id}: {str(e)}")
        # No lanzar excepción, solo loguear el error

@router.get("/")
async def get_all_reports():
    """Obtiene todos los reportes activos"""
    try:
        sb = _sb()
        result = sb.table("reports").select("*").eq("status", "active").order("created_at", desc=True).execute()
        return {"reports": result.data, "count": len(result.data)}
    except Exception as e:
        raise HTTPException(500, f"Error obteniendo reportes: {str(e)}")

@router.get("/nearby")
async def get_nearby_reports(
    lat: float = Query(..., description="Latitud"),
    lng: float = Query(..., description="Longitud"),
    radius_km: float = Query(10.0, description="Radio en kilómetros")
):
    """Obtiene reportes cercanos a una ubicación"""
    try:
        sb = _sb()
        result = sb.table("reports").select("*").eq("status", "active").execute()
        
        nearby_reports = []
        for report in result.data:
            coords = _extract_coords(report.get("location"))
            if coords:
                report_lat, report_lon = coords
                distance = haversine_km(lat, lng, report_lat, report_lon)
                if distance <= radius_km:
                    report["distance_km"] = round(distance, 2)
                    nearby_reports.append(report)
        
        # Ordenar por distancia
        nearby_reports.sort(key=lambda x: x["distance_km"])
        
        return {"reports": nearby_reports, "count": len(nearby_reports)}
    except Exception as e:
        raise HTTPException(500, f"Error obteniendo reportes cercanos: {str(e)}")

@router.get("/{report_id}")
async def get_report_by_id(report_id: str):
    """Obtiene un reporte por ID"""
    try:
        sb = _sb()
        result = sb.table("reports").select("*").eq("id", report_id).single().execute()
        
        if not result.data:
            raise HTTPException(404, "Reporte no encontrado")
        
        return {"report": result.data}
    except Exception as e:
        if "404" in str(e):
            raise e
        raise HTTPException(500, f"Error obteniendo reporte: {str(e)}")

@router.post("/")
async def create_report(
    report_data: Dict[str, Any] = Body(...),
    background_tasks: BackgroundTasks = None
):
    """Crea un nuevo reporte y genera embeddings automáticamente si hay fotos"""
    try:
        sb = _sb()
        
        # Validar datos requeridos
        required_fields = ["type", "reporter_id", "species", "description", "location"]
        for field in required_fields:
            if field not in report_data:
                raise HTTPException(400, f"Campo requerido faltante: {field}")
        
        # Crear reporte
        # Insertar el reporte (insert retorna el registro insertado)
        insert_result = sb.table("reports").insert(report_data).execute()
        
        if not insert_result.data:
            raise HTTPException(500, "Error creando reporte")
        
        # insert_result.data puede ser una lista o un diccionario según la versión de Supabase
        if isinstance(insert_result.data, list):
            created_report = insert_result.data[0] if insert_result.data else None
        else:
            created_report = insert_result.data
        
        if not created_report:
            raise HTTPException(500, "Error creando reporte: no se retornó el registro")
        
        report_id = created_report.get("id")
        
        # Generar embedding automáticamente si hay fotos (de forma síncrona para asegurar que se guarde)
        photos = created_report.get("photos") or report_data.get("photos", [])
        if photos and isinstance(photos, list) and len(photos) > 0:
            first_photo = photos[0]
            if first_photo:
                print(f"📸 [embedding] Reporte creado con fotos. Generando embedding para reporte {report_id}...")
                # Generar embedding de forma síncrona para asegurar que se guarde antes de retornar
                try:
                    await generate_and_save_embedding(report_id, first_photo)
                    print(f"✅ [embedding] Embedding generado y guardado para reporte {report_id}")
                except Exception as e:
                    print(f"⚠️ [embedding] Error generando embedding (no crítico): {str(e)}")
                    # No fallar la creación del reporte si falla el embedding
                
                # Enviar automáticamente al webhook de n8n para procesamiento
                try:
                    print(f"📤 [n8n] Enviando reporte {report_id} al webhook de n8n...")
                    webhook_url = get_n8n_webhook_url()
                    
                    # Enviar cada foto al webhook (en background para no bloquear)
                    for idx, photo_url in enumerate(photos):
                        report_payload = {
                            "report_id": report_id,
                            "image_url": photo_url,
                            "image_index": idx,
                            "total_images": len(photos),
                            "species": created_report.get("species"),
                            "type": created_report.get("type"),
                            "status": created_report.get("status"),
                            "created_at": created_report.get("created_at"),
                            "has_labels": created_report.get("labels") is not None
                        }
                        
                        # Enviar en background para no bloquear la respuesta
                        if background_tasks:
                            background_tasks.add_task(send_to_n8n_webhook, report_payload, webhook_url)
                        else:
                            # Si no hay background tasks, enviar directamente pero no bloquear
                            asyncio.create_task(send_to_n8n_webhook(report_payload, webhook_url))
                    
                    print(f"✅ [n8n] Reporte {report_id} enviado al webhook de n8n ({len(photos)} imágenes)")
                except Exception as e:
                    print(f"⚠️ [n8n] Error enviando reporte a n8n (no crítico): {str(e)}")
                    # No fallar la creación del reporte si falla el envío a n8n
        
        return {"report": created_report, "message": "Reporte creado exitosamente"}
    except Exception as e:
        if "400" in str(e) or "500" in str(e):
            raise e
        raise HTTPException(500, f"Error creando reporte: {str(e)}")

@router.put("/{report_id}")
async def update_report(
    report_id: str,
    updates: Dict[str, Any] = Body(...),
    background_tasks: BackgroundTasks = None
):
    """Actualiza un reporte existente y genera embeddings si hay nuevas fotos"""
    try:
        sb = _sb()
        
        # Obtener el reporte actual para verificar si tiene embedding
        current_result = sb.table("reports").select("id, photos, embedding").eq("id", report_id).single().execute()
        
        if not current_result.data:
            raise HTTPException(404, "Reporte no encontrado")
        
        current_report = current_result.data
        
        # Actualizar reporte
        result = sb.table("reports").update(updates).eq("id", report_id).select("*").execute()
        
        if not result.data or len(result.data) == 0:
            raise HTTPException(404, "Reporte no encontrado")
        
        updated_report = result.data[0] if isinstance(result.data, list) else result.data
        
        # Generar embedding si:
        # 1. Hay fotos nuevas o actualizadas
        # 2. El reporte no tiene embedding aún
        photos = updated_report.get("photos") or updates.get("photos", [])
        has_embedding = current_report.get("embedding") is not None
        
        if photos and isinstance(photos, list) and len(photos) > 0:
            first_photo = photos[0]
            if first_photo and (not has_embedding or "photos" in updates):
                print(f"📸 [embedding] Reporte actualizado con fotos. Generando embedding para reporte {report_id}...")
                # Generar embedding de forma síncrona para asegurar que se guarde
                try:
                    await generate_and_save_embedding(report_id, first_photo)
                    print(f"✅ [embedding] Embedding generado y guardado para reporte {report_id}")
                except Exception as e:
                    print(f"⚠️ [embedding] Error generando embedding (no crítico): {str(e)}")
                    # No fallar la actualización del reporte si falla el embedding
                
                # Enviar automáticamente al webhook de n8n si hay fotos nuevas
                if "photos" in updates:
                    try:
                        print(f"📤 [n8n] Enviando reporte actualizado {report_id} al webhook de n8n...")
                        webhook_url = get_n8n_webhook_url()
                        
                        # Enviar cada foto nueva al webhook (en background)
                        for idx, photo_url in enumerate(photos):
                            report_payload = {
                                "report_id": report_id,
                                "image_url": photo_url,
                                "image_index": idx,
                                "total_images": len(photos),
                                "species": updated_report.get("species"),
                                "type": updated_report.get("type"),
                                "status": updated_report.get("status"),
                                "created_at": updated_report.get("created_at"),
                                "has_labels": updated_report.get("labels") is not None
                            }
                            
                            # Enviar en background para no bloquear
                            if background_tasks:
                                background_tasks.add_task(send_to_n8n_webhook, report_payload, webhook_url)
                            else:
                                asyncio.create_task(send_to_n8n_webhook(report_payload, webhook_url))
                        
                        print(f"✅ [n8n] Reporte actualizado {report_id} enviado al webhook de n8n ({len(photos)} imágenes)")
                    except Exception as e:
                        print(f"⚠️ [n8n] Error enviando reporte actualizado a n8n (no crítico): {str(e)}")
        
        return {"report": updated_report, "message": "Reporte actualizado exitosamente"}
    except Exception as e:
        if "404" in str(e):
            raise e
        raise HTTPException(500, f"Error actualizando reporte: {str(e)}")

@router.delete("/{report_id}")
async def delete_report(report_id: str):
    """Elimina un reporte (soft delete cambiando status a cancelled)"""
    try:
        sb = _sb()
        result = sb.table("reports").update({"status": "cancelled"}).eq("id", report_id).execute()
        
        if not result.data or len(result.data) == 0:
            raise HTTPException(404, "Reporte no encontrado")
        
        return {"message": "Reporte eliminado exitosamente"}
    except Exception as e:
        if "404" in str(e):
            raise e
        raise HTTPException(500, f"Error eliminando reporte: {str(e)}")

@router.post("/{report_id}/resolve")
async def resolve_report(report_id: str):
    """Marca un reporte como resuelto"""
    try:
        sb = _sb()
        result = sb.table("reports").update({
            "status": "resolved",
            "resolved_at": "now()"
        }).eq("id", report_id).select("*").execute()
        
        if not result.data or len(result.data) == 0:
            raise HTTPException(404, "Reporte no encontrado")
        
        updated_report = result.data[0] if isinstance(result.data, list) else result.data
        return {"report": updated_report, "message": "Reporte marcado como resuelto"}
    except Exception as e:
        if "404" in str(e):
            raise e
        raise HTTPException(500, f"Error resolviendo reporte: {str(e)}")
