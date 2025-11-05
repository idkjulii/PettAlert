# backend/routers/n8n_integration.py
"""
Integración con n8n para procesamiento masivo de imágenes de reportes.
Este módulo permite que n8n procese todas las imágenes de los reportes
para análisis con Google Vision y generación de embeddings.
"""

from fastapi import APIRouter, HTTPException, Query, Body, BackgroundTasks
from typing import List, Dict, Any, Optional
import os
import httpx
import asyncio
from supabase import create_client, Client

router = APIRouter(prefix="/n8n", tags=["n8n-integration"])

def _sb() -> Client:
    """Obtiene el cliente de Supabase"""
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise HTTPException(500, "Faltan SUPABASE_URL / SUPABASE_SERVICE_KEY")
    return create_client(url, key)

def get_n8n_webhook_url() -> str:
    """Obtiene la URL del webhook de n8n desde variables de entorno"""
    webhook_url = os.getenv("N8N_WEBHOOK_URL")
    if not webhook_url:
        # URL por defecto del usuario
        webhook_url = "https://n8n.arc-ctes.shop/webhook-test/9f0311e4-6678-4884-b9d1-af2276fe6aec"
    return webhook_url

async def send_to_n8n_webhook(report_data: Dict[str, Any], webhook_url: Optional[str] = None) -> Dict[str, Any]:
    """
    Envía datos de un reporte al webhook de n8n para procesamiento.
    
    Args:
        report_data: Datos del reporte a enviar
        webhook_url: URL del webhook (opcional, usa la de env si no se proporciona)
    
    Returns:
        Resultado de la petición al webhook
    """
    if not webhook_url:
        webhook_url = get_n8n_webhook_url()
    
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                webhook_url,
                json=report_data,
                headers={"Content-Type": "application/json"}
            )
            response.raise_for_status()
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.content else None
            }
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Timeout al comunicarse con n8n",
            "status_code": None
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "status_code": None
        }


@router.get("/reports/with-images")
async def get_reports_with_images(
    status: str = Query("active", description="Estado de los reportes (active, resolved, closed)"),
    limit: int = Query(100, ge=1, le=1000, description="Número máximo de reportes a retornar"),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    has_labels: Optional[bool] = Query(None, description="Filtrar por reportes con/sin labels")
):
    """
    Obtiene todos los reportes que tienen imágenes para procesamiento en n8n.
    
    Este endpoint está diseñado para que n8n pueda obtener todos los reportes
    que necesitan ser procesados y luego procesar cada imagen individualmente.
    """
    try:
        sb = _sb()
        
        # Construir query base
        query = sb.table("reports").select("id, photos, labels, species, type, status, created_at")
        
        # Filtrar por estado
        if status:
            query = query.eq("status", status)
        
        # Filtrar por reportes que tienen fotos
        # Nota: En Supabase, necesitamos filtrar en el código ya que no hay filtro directo para arrays no vacíos
        
        # Ejecutar query
        result = query.limit(limit).offset(offset).order("created_at", desc=True).execute()
        
        # Filtrar reportes que tienen fotos
        reports_with_photos = []
        for report in result.data:
            photos = report.get("photos", [])
            if photos and isinstance(photos, list) and len(photos) > 0:
                # Si se especifica filtro de labels, aplicarlo
                if has_labels is not None:
                    has_labels_data = report.get("labels") is not None
                    if has_labels != has_labels_data:
                        continue
                
                # Expandir reportes: un reporte con múltiples fotos se convierte en múltiples entradas
                for idx, photo_url in enumerate(photos):
                    reports_with_photos.append({
                        "report_id": report["id"],
                        "image_url": photo_url,
                        "image_index": idx,
                        "total_images": len(photos),
                        "species": report.get("species"),
                        "type": report.get("type"),
                        "status": report.get("status"),
                        "created_at": report.get("created_at"),
                        "has_labels": report.get("labels") is not None,
                        "current_labels": report.get("labels")
                    })
        
        return {
            "reports": reports_with_photos,
            "count": len(reports_with_photos),
            "pagination": {
                "limit": limit,
                "offset": offset,
                "has_more": len(reports_with_photos) == limit
            }
        }
    except Exception as e:
        raise HTTPException(500, f"Error obteniendo reportes con imágenes: {str(e)}")


@router.post("/process-result")
async def process_analysis_result(
    data: Dict[str, Any] = Body(...)
):
    """
    Recibe los resultados del procesamiento de n8n y actualiza el reporte.
    
    Este endpoint es llamado por n8n después de procesar una imagen con Google Vision.
    
    Body esperado:
    {
        "report_id": "uuid",
        "image_url": "https://...",
        "labels": [...],  # Resultado de Google Vision
        "colors": [...],  # Colores dominantes
        "species": "dog",  # Especie detectada (opcional)
        "analysis_metadata": {...}  # Metadata adicional (opcional)
    }
    """
    try:
        report_id = data.get("report_id")
        image_url = data.get("image_url")
        labels = data.get("labels")
        colors = data.get("colors")
        species = data.get("species")
        analysis_metadata = data.get("analysis_metadata", {})
        
        if not report_id:
            raise HTTPException(400, "report_id es requerido")
        
        if not labels:
            raise HTTPException(400, "labels es requerido")
        
        sb = _sb()
        
        # Obtener reporte actual
        current_report = sb.table("reports").select("id, labels, colors, species").eq("id", report_id).single().execute()
        
        if not current_report.data:
            raise HTTPException(404, f"Reporte {report_id} no encontrado")
        
        # Preparar datos para actualizar
        update_data = {}
        
        # Actualizar labels si es la primera vez o si hay mejor calidad
        current_labels = current_report.data.get("labels")
        if not current_labels or isinstance(current_labels, dict):
            # Si no hay labels o es un objeto, reemplazar
            update_data["labels"] = {
                "labels": labels,
                "source": "n8n_google_vision",
                "processed_at": analysis_metadata.get("processed_at"),
                "image_url": image_url
            }
        elif isinstance(current_labels, dict):
            # Si ya hay labels, actualizar solo si no hay labels o si son mejores
            existing_labels_list = current_labels.get("labels", [])
            if not existing_labels_list or len(labels) > len(existing_labels_list):
                update_data["labels"] = {
                    "labels": labels,
                    "source": "n8n_google_vision",
                    "processed_at": analysis_metadata.get("processed_at"),
                    "image_url": image_url
                }
        
        # Actualizar colores si se proporcionan
        if colors:
            update_data["colors"] = colors
        
        # Actualizar especie si se detecta y no está definida
        if species and not current_report.data.get("species"):
            update_data["species"] = species
        
        # Actualizar reporte solo si hay cambios
        if update_data:
            result = sb.table("reports").update(update_data).eq("id", report_id).execute()
            
            return {
                "success": True,
                "message": "Reporte actualizado exitosamente",
                "report_id": report_id,
                "updated_fields": list(update_data.keys())
            }
        else:
            return {
                "success": True,
                "message": "No se requirieron actualizaciones",
                "report_id": report_id,
                "updated_fields": []
            }
            
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error procesando resultado: {str(e)}")


@router.get("/health")
async def n8n_health():
    """Verifica el estado de la integración con n8n"""
    try:
        sb = _sb()
        webhook_url = get_n8n_webhook_url()
        
        # Verificar conexión con Supabase
        test_query = sb.table("reports").select("id").limit(1).execute()
        
        # Contar reportes con imágenes
        all_reports = sb.table("reports").select("id, photos").eq("status", "active").execute()
        
        reports_with_images = sum(
            1 for r in all_reports.data 
            if r.get("photos") and isinstance(r.get("photos"), list) and len(r.get("photos", [])) > 0
        )
        
        # Verificar conectividad con n8n (test rápido)
        n8n_status = "unknown"
        try:
            async with httpx.AsyncClient(timeout=5.0) as client:
                response = await client.get(webhook_url.replace("/webhook-test/", "/health").replace("9f0311e4-6678-4884-b9d1-af2276fe6aec", ""))
                n8n_status = "reachable" if response.status_code < 500 else "error"
        except:
            n8n_status = "unreachable"
        
        return {
            "status": "ok",
            "message": "Integración con n8n funcionando correctamente",
            "supabase": "conectado" if test_query.data is not None else "error",
            "n8n_webhook": webhook_url,
            "n8n_status": n8n_status,
            "reports_with_images": reports_with_images,
            "total_active_reports": len(all_reports.data),
            "endpoints": {
                "get_reports": "/n8n/reports/with-images",
                "send_to_webhook": "/n8n/send-to-webhook",
                "batch_process": "/n8n/batch-process",
                "process_result": "/n8n/process-result",
                "health": "/n8n/health"
            }
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Error en integración n8n: {str(e)}",
            "supabase": "error"
        }


@router.post("/send-to-webhook")
async def send_report_to_webhook(
    report_id: str = Body(..., description="ID del reporte a enviar a n8n"),
    webhook_url: Optional[str] = Body(None, description="URL del webhook (opcional, usa la de env)"),
    background_tasks: BackgroundTasks = None
):
    """
    Envía un reporte específico al webhook de n8n para procesamiento.
    Este endpoint obtiene el reporte y envía cada imagen al webhook.
    """
    try:
        sb = _sb()
        
        # Obtener reporte
        result = sb.table("reports").select("id, photos, species, type, status, created_at, labels").eq("id", report_id).single().execute()
        
        if not result.data:
            raise HTTPException(404, f"Reporte {report_id} no encontrado")
        
        report = result.data
        photos = report.get("photos", [])
        
        if not photos or not isinstance(photos, list) or len(photos) == 0:
            raise HTTPException(400, f"El reporte {report_id} no tiene imágenes")
        
        if not webhook_url:
            webhook_url = get_n8n_webhook_url()
        
        # Preparar datos para enviar (una petición por imagen)
        results = []
        for idx, photo_url in enumerate(photos):
            report_data = {
                "report_id": report_id,
                "image_url": photo_url,
                "image_index": idx,
                "total_images": len(photos),
                "species": report.get("species"),
                "type": report.get("type"),
                "status": report.get("status"),
                "created_at": report.get("created_at"),
                "has_labels": report.get("labels") is not None
            }
            
            # Enviar al webhook (en background para no bloquear)
            if background_tasks:
                background_tasks.add_task(send_to_n8n_webhook, report_data, webhook_url)
                results.append({
                    "image_index": idx,
                    "image_url": photo_url,
                    "status": "enqueued"
                })
            else:
                # Si no hay background tasks, enviar directamente
                result = await send_to_n8n_webhook(report_data, webhook_url)
                results.append({
                    "image_index": idx,
                    "image_url": photo_url,
                    "status": "sent" if result["success"] else "error",
                    "error": result.get("error")
                })
        
        return {
            "success": True,
            "message": f"Reporte {report_id} enviado al webhook de n8n",
            "report_id": report_id,
            "total_images": len(photos),
            "webhook_url": webhook_url,
            "results": results,
            "note": "n8n procesará las imágenes y llamará a /n8n/process-result para actualizar los resultados"
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error enviando reporte al webhook: {str(e)}")


@router.post("/batch-process")
async def batch_process_reports(
    report_ids: Optional[List[str]] = Body(None, description="Lista de IDs de reportes a procesar (opcional)"),
    limit: Optional[int] = Body(10, description="Número de reportes a procesar si no se proporcionan IDs"),
    has_labels: Optional[bool] = Body(False, description="Filtrar por reportes con/sin labels"),
    webhook_url: Optional[str] = Body(None, description="URL del webhook (opcional, usa la de env)"),
    background_tasks: BackgroundTasks = None
):
    """
    Procesa múltiples reportes enviándolos al webhook de n8n.
    
    Si se proporcionan report_ids, procesa esos reportes específicos.
    Si no, obtiene reportes automáticamente según los filtros.
    """
    try:
        sb = _sb()
        
        if not webhook_url:
            webhook_url = get_n8n_webhook_url()
        
        # Obtener reportes a procesar
        if report_ids:
            # Procesar reportes específicos
            result = sb.table("reports").select("id, photos, species, type, status, created_at, labels").in_("id", report_ids).execute()
            reports_to_process = result.data
        else:
            # Obtener reportes automáticamente
            query = sb.table("reports").select("id, photos, species, type, status, created_at, labels").eq("status", "active")
            
            if has_labels is not None:
                # Nota: Supabase no tiene filtro directo para null, necesitamos filtrar después
                pass
            
            result = query.limit(limit).order("created_at", desc=True).execute()
            
            # Filtrar reportes con imágenes y según has_labels
            reports_to_process = []
            for report in result.data:
                photos = report.get("photos", [])
                if photos and isinstance(photos, list) and len(photos) > 0:
                    if has_labels is not None:
                        has_labels_data = report.get("labels") is not None
                        if has_labels != has_labels_data:
                            continue
                    reports_to_process.append(report)
        
        # Enviar cada reporte al webhook
        total_images = 0
        sent_count = 0
        error_count = 0
        
        for report in reports_to_process:
            photos = report.get("photos", [])
            if not photos or not isinstance(photos, list) or len(photos) == 0:
                continue
            
            for idx, photo_url in enumerate(photos):
                report_data = {
                    "report_id": report["id"],
                    "image_url": photo_url,
                    "image_index": idx,
                    "total_images": len(photos),
                    "species": report.get("species"),
                    "type": report.get("type"),
                    "status": report.get("status"),
                    "created_at": report.get("created_at"),
                    "has_labels": report.get("labels") is not None
                }
                
                total_images += 1
                
                # Enviar al webhook en background
                if background_tasks:
                    background_tasks.add_task(send_to_n8n_webhook, report_data, webhook_url)
                    sent_count += 1
                else:
                    result = await send_to_n8n_webhook(report_data, webhook_url)
                    if result["success"]:
                        sent_count += 1
                    else:
                        error_count += 1
        
        return {
            "success": True,
            "message": f"Procesamiento batch iniciado",
            "total_reports": len(reports_to_process),
            "total_images": total_images,
            "sent": sent_count,
            "errors": error_count,
            "webhook_url": webhook_url,
            "note": "Las imágenes se están enviando al webhook de n8n. n8n las procesará y llamará a /n8n/process-result"
        }
    except Exception as e:
        raise HTTPException(500, f"Error en procesamiento batch: {str(e)}")

