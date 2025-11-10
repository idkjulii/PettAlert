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
        webhook_url = (
            "https://n8n.arc-ctes.shop/webhook-test/9f0311e4-6678-4884-b9d1-af2276fe6aec"
        )
    return webhook_url


async def send_to_n8n_webhook(
    report_data: Dict[str, Any], webhook_url: Optional[str] = None
) -> Dict[str, Any]:
    """
    Envía datos de un reporte al webhook de n8n para procesamiento.
    """
    if not webhook_url:
        webhook_url = get_n8n_webhook_url()

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                webhook_url,
                json=report_data,
                headers={"Content-Type": "application/json"},
            )
            response.raise_for_status()
            return {
                "success": True,
                "status_code": response.status_code,
                "response": response.json() if response.content else None,
            }
    except httpx.TimeoutException:
        return {
            "success": False,
            "error": "Timeout al comunicarse con n8n",
            "status_code": None,
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e),
            "status_code": None,
        }


@router.get("/reports/with-images")
async def get_reports_with_images(
    status: str = Query(
        "active", description="Estado de los reportes (active, resolved, closed)"
    ),
    limit: int = Query(
        100, ge=1, le=1000, description="Número máximo de reportes a retornar"
    ),
    offset: int = Query(0, ge=0, description="Offset para paginación"),
    has_labels: Optional[bool] = Query(
        None, description="Filtrar por reportes con/sin labels"
    ),
):
    """
    Obtiene todos los reportes que tienen imágenes para procesamiento en n8n.
    """
    try:
        sb = _sb()

        query = sb.table("reports").select(
            "id, photos, labels, species, type, status, created_at"
        )

        if status:
            query = query.eq("status", status)

        result = (
            query.limit(limit)
            .offset(offset)
            .order("created_at", desc=True)
            .execute()
        )

        reports_with_photos = []
        for report in result.data or []:
            photos = report.get("photos", [])
            if photos and isinstance(photos, list):
                if has_labels is not None:
                    has_labels_data = report.get("labels") is not None
                    if has_labels != has_labels_data:
                        continue

                for idx, photo_url in enumerate(photos):
                    reports_with_photos.append(
                        {
                            "report_id": report["id"],
                            "image_url": photo_url,
                            "image_index": idx,
                            "total_images": len(photos),
                            "species": report.get("species"),
                            "type": report.get("type"),
                            "status": report.get("status"),
                            "created_at": report.get("created_at"),
                            "has_labels": report.get("labels") is not None,
                            "current_labels": report.get("labels"),
                        }
                    )

        return {
            "reports": reports_with_photos,
            "count": len(reports_with_photos),
            "pagination": {
                "limit": limit,
                "offset": offset,
                "has_more": len(reports_with_photos) == limit,
            },
        }
    except Exception as e:
        raise HTTPException(500, f"Error obteniendo reportes con imágenes: {str(e)}")


async def process_matches(
    report_id: str, matches_data: Dict[str, Any], report_type: str
):
    """
    Procesa los matches encontrados y los guarda en la tabla matches.
    """
    try:
        sb = _sb()
        matches = matches_data.get("matches", [])

        if not matches:
            print(
                f"ℹ️ [matches] No se encontraron coincidencias para el reporte {report_id}"
            )
            return

        print(
            f"🔍 [matches] Procesando {len(matches)} coincidencias para reporte {report_id}..."
        )

        if report_type == "lost":
            lost_report_id = report_id
            found_report_id = None
        else:
            found_report_id = report_id
            lost_report_id = None

        matches_created = 0
        for match in matches:
            try:
                similarity_score = match.get("similarity_score", 0)
                match_report_id = match.get("report_id")

                if not match_report_id:
                    continue

                if similarity_score < 0.7:
                    continue

                match_data = {
                    "similarity_score": round(similarity_score, 4),
                    "matched_by": match.get("source") or "ai_visual",
                    "status": "pending",
                }

                if report_type == "lost":
                    match_data["lost_report_id"] = lost_report_id
                    match_data["found_report_id"] = match_report_id
                else:
                    match_data["lost_report_id"] = match_report_id
                    match_data["found_report_id"] = found_report_id

                if report_type == "lost":
                    existing = (
                        sb.table("matches")
                        .select("id, similarity_score")
                        .eq("lost_report_id", lost_report_id)
                        .eq("found_report_id", match_report_id)
                        .execute()
                    )
                else:
                    existing = (
                        sb.table("matches")
                        .select("id, similarity_score")
                        .eq("lost_report_id", match_report_id)
                        .eq("found_report_id", found_report_id)
                        .execute()
                    )

                if existing.data:
                    existing_match = existing.data[0]
                    if similarity_score > (existing_match.get("similarity_score") or 0):
                        sb.table("matches").update(
                            {
                                "similarity_score": round(similarity_score, 4),
                                "matched_by": match.get("source")
                                or "ai_visual",
                                "status": "pending",
                            }
                        ).eq("id", existing_match["id"]).execute()
                        matches_created += 1
                        print(
                            f"  ✅ [matches] Match actualizado: {match_report_id} (similitud: {similarity_score:.2f})"
                        )
                else:
                    result = (
                        sb.table("matches").insert(match_data).execute()
                    )
                    if result.data:
                        matches_created += 1
                        print(
                            f"  ✅ [matches] Match creado: {match_report_id} (similitud: {similarity_score:.2f})"
                        )

            except Exception as e:
                print(f"  ⚠️ [matches] Error procesando match individual: {str(e)}")
                continue

        print(f"✅ [matches] {matches_created} matches procesados para reporte {report_id}")

    except Exception as e:
        print(f"❌ [matches] Error procesando matches: {str(e)}")


@router.post("/process-result")
async def process_analysis_result(data: Dict[str, Any] = Body(...)):
    """
    Recibe los resultados del procesamiento de n8n y actualiza el reporte.
    """
    try:
        report_id = data.get("report_id")
        image_url = data.get("image_url")

        analysis = data.get("analysis", {})
        labels = data.get("labels") or (
            analysis.get("labels") if isinstance(analysis, dict) else None
        )
        colors = data.get("colors") or (
            analysis.get("colors") if isinstance(analysis, dict) else None
        )
        species = data.get("species") or (
            analysis.get("species_detected") if isinstance(analysis, dict) else None
        )

        matches_data = data.get("matches")
        analysis_metadata = data.get("analysis_metadata", {})

        if not report_id:
            raise HTTPException(400, "report_id es requerido")

        sb = _sb()

        current_report = (
            sb.table("reports")
            .select("id, labels, colors, species, type")
            .eq("id", report_id)
            .execute()
        )

        current_report_data = (
            current_report.data[0] if current_report.data else None
        )

        if not current_report_data:
            raise HTTPException(404, f"Reporte {report_id} no encontrado")

        report_type = current_report_data.get("type")

        update_data = {}

        if labels:
            current_labels = current_report_data.get("labels")
            if not current_labels or isinstance(current_labels, dict):
                update_data["labels"] = {
                    "labels": labels,
                    "source": "n8n_google_vision",
                    "processed_at": analysis_metadata.get("processed_at")
                    or analysis_metadata.get("searched_at"),
                    "image_url": image_url,
                }
            elif isinstance(current_labels, dict):
                existing_labels_list = current_labels.get("labels", [])
                if not existing_labels_list or (
                    isinstance(labels, list)
                    and len(labels) > len(existing_labels_list)
                ):
                    update_data["labels"] = {
                        "labels": labels,
                        "source": "n8n_google_vision",
                        "processed_at": analysis_metadata.get("processed_at")
                        or analysis_metadata.get("searched_at"),
                        "image_url": image_url,
                    }

        if colors:
            update_data["colors"] = colors

        if species and not current_report_data.get("species"):
            update_data["species"] = species

        if update_data:
            sb.table("reports").update(update_data).eq("id", report_id).execute()
            print(
                f"✅ [n8n] Reporte {report_id} actualizado con análisis de Google Vision"
            )

        matches_processed = False
        if matches_data and isinstance(matches_data, dict) and matches_data.get("matches"):
            try:
                await process_matches(report_id, matches_data, report_type)
                matches_processed = True
            except Exception as e:
                print(f"⚠️ [n8n] Error procesando matches (no crítico): {str(e)}")

        return {
            "success": True,
            "message": "Reporte actualizado exitosamente",
            "report_id": report_id,
            "updated_fields": list(update_data.keys()) if update_data else [],
            "matches_processed": matches_processed,
            "matches_found": matches_data.get("matches_found", 0)
            if matches_data
            else 0,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error procesando resultado: {str(e)}")


@router.post("/send-to-webhook")
async def send_report_to_webhook(
    report_id: str = Body(..., description="ID del reporte a enviar a n8n"),
    webhook_url: Optional[str] = Body(
        None, description="URL del webhook (opcional, usa la de env)"
    ),
    background_tasks: BackgroundTasks = None,
):
    """
    Envía un reporte específico al webhook de n8n para procesamiento.
    """
    try:
        sb = _sb()

        result = (
            sb.table("reports")
            .select(
                "id, photos, species, type, status, created_at, labels"
            )
            .eq("id", report_id)
            .execute()
        )

        if not result.data:
            raise HTTPException(404, f"Reporte {report_id} no encontrado")

        report = result.data[0]
        photos = report.get("photos", [])

        if not photos or not isinstance(photos, list):
            raise HTTPException(400, f"El reporte {report_id} no tiene imágenes")

        if not webhook_url:
            webhook_url = get_n8n_webhook_url()

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
                "has_labels": report.get("labels") is not None,
            }

            if background_tasks:
                background_tasks.add_task(
                    send_to_n8n_webhook, report_data, webhook_url
                )
                results.append(
                    {
                        "image_index": idx,
                        "image_url": photo_url,
                        "status": "enqueued",
                    }
                )
            else:
                result_send = await send_to_n8n_webhook(report_data, webhook_url)
                results.append(
                    {
                        "image_index": idx,
                        "image_url": photo_url,
                        "status": "sent"
                        if result_send["success"]
                        else "error",
                        "error": result_send.get("error"),
                    }
                )

        return {
            "success": True,
            "message": f"Reporte {report_id} enviado al webhook de n8n",
            "report_id": report_id,
            "total_images": len(photos),
            "webhook_url": webhook_url,
            "results": results,
            "note": "n8n procesará las imágenes y llamará a /n8n/process-result para actualizar los resultados",
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error enviando reporte al webhook: {str(e)}")


@router.post("/batch-process")
async def batch_process_reports(
    report_ids: Optional[List[str]] = Body(
        None, description="Lista de IDs de reportes a procesar (opcional)"
    ),
    limit: Optional[int] = Body(
        10, description="Número de reportes a procesar si no se proporcionan IDs"
    ),
    has_labels: Optional[bool] = Body(
        False, description="Filtrar por reportes con/sin labels"
    ),
    webhook_url: Optional[str] = Body(
        None, description="URL del webhook (opcional, usa la de env)"
    ),
    background_tasks: BackgroundTasks = None,
):
    """
    Procesa múltiples reportes enviándolos al webhook de n8n.
    """
    try:
        sb = _sb()

        if not webhook_url:
            webhook_url = get_n8n_webhook_url()

        if report_ids:
            result = (
                sb.table("reports")
                .select(
                    "id, photos, species, type, status, created_at, labels"
                )
                .in_("id", report_ids)
                .execute()
            )
            reports_to_process = result.data
        else:
            query = (
                sb.table("reports")
                .select(
                    "id, photos, species, type, status, created_at, labels"
                )
                .eq("status", "active")
            )

            result = query.limit(limit).order("created_at", desc=True).execute()

            reports_to_process = []
            for report in result.data or []:
                photos = report.get("photos", [])
                if photos and isinstance(photos, list):
                    if has_labels is not None:
                        has_labels_data = report.get("labels") is not None
                        if has_labels != has_labels_data:
                            continue
                    reports_to_process.append(report)

        total_images = 0
        sent_count = 0
        error_count = 0

        for report in reports_to_process:
            photos = report.get("photos", [])
            if not photos or not isinstance(photos, list):
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
                    "has_labels": report.get("labels") is not None,
                }

                total_images += 1

                if background_tasks:
                    background_tasks.add_task(
                        send_to_n8n_webhook, report_data, webhook_url
                    )
                    sent_count += 1
                else:
                    result_send = await send_to_n8n_webhook(report_data, webhook_url)
                    if result_send["success"]:
                        sent_count += 1
                    else:
                        error_count += 1

        return {
            "success": True,
            "message": "Procesamiento batch iniciado",
            "total_reports": len(reports_to_process),
            "total_images": total_images,
            "sent": sent_count,
            "errors": error_count,
            "webhook_url": webhook_url,
            "note": "Las imágenes se están enviando al webhook de n8n. n8n las procesará y llamará a /n8n/process-result",
        }
    except Exception as e:
        raise HTTPException(500, f"Error en procesamiento batch: {str(e)}")


