"""
Router de Búsqueda RAG (Retrieval Augmented Generation)
=======================================================

Este router implementa búsqueda semántica usando RAG (Retrieval Augmented Generation).
RAG combina búsqueda vectorial con embeddings para encontrar información relevante.

Funcionalidades:
- Búsqueda de reportes similares usando embeddings
- Búsqueda con filtros de ubicación
- Guardar y recuperar embeddings de reportes
- Estadísticas de embeddings

Los embeddings se almacenan en Supabase usando pgvector para búsquedas eficientes.
"""

# backend/routers/rag_search.py
from fastapi import APIRouter, HTTPException, Query, Body
from typing import List, Dict, Any, Optional
import os, sys
from pathlib import Path
import numpy as np  # Para operaciones con vectores
from supabase import Client

# Agregar la carpeta parent al path para poder importar utils
sys.path.insert(0, str(Path(__file__).parent.parent))
from utils.supabase_client import get_supabase_client

# Crear el router con prefijo /rag
router = APIRouter(prefix="/rag", tags=["rag-search"])

def _sb() -> Client:
    """
    Crea un cliente de Supabase con configuración optimizada de timeouts.
    
    Returns:
        Client: Cliente de Supabase configurado
        
    Raises:
        HTTPException: Si no se puede conectar a Supabase
    """
    try:
        return get_supabase_client()
    except Exception as e:
        raise HTTPException(500, f"Error conectando a Supabase: {str(e)}")

@router.post("/search")
async def rag_search(
    embedding: List[float] = Body(..., description="Vector de embedding (512 dimensiones)"),
    match_threshold: float = Query(0.7, ge=0.0, le=1.0, description="Umbral mínimo de similitud"),
    match_count: int = Query(10, ge=1, le=50, description="Número máximo de resultados"),
    filter_species: Optional[str] = Query(None, description="Filtrar por especie"),
    filter_type: Optional[str] = Query(None, description="Filtrar por tipo (lost/found)")
):
    """
    Búsqueda RAG usando embeddings almacenados en Supabase.
    Busca reportes similares basándose en similitud de embeddings.
    """
    try:
        # Validar que el embedding tenga 512 dimensiones
        if len(embedding) != 512:
            raise HTTPException(400, f"El embedding debe tener 512 dimensiones, se recibieron {len(embedding)}")
        
        sb = _sb()
        
        # Llamar a la función SQL de búsqueda
        result = sb.rpc('search_similar_reports', {
            'query_embedding': embedding,
            'match_threshold': match_threshold,
            'match_count': match_count,
            'filter_species': filter_species,
            'filter_type': filter_type
        }).execute()
        
        if not result.data:
            return {
                "results": [],
                "count": 0,
                "message": "No se encontraron reportes similares"
            }
        
        return {
            "results": result.data,
            "count": len(result.data),
            "search_params": {
                "match_threshold": match_threshold,
                "match_count": match_count,
                "filter_species": filter_species,
                "filter_type": filter_type
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error en búsqueda RAG: {str(e)}")

@router.post("/search-with-location")
async def rag_search_with_location(
    embedding: List[float] = Body(..., description="Vector de embedding (512 dimensiones)"),
    user_lat: float = Query(..., description="Latitud del usuario"),
    user_lng: float = Query(..., description="Longitud del usuario"),
    max_distance_km: float = Query(10.0, ge=0.1, le=100.0, description="Distancia máxima en km"),
    match_threshold: float = Query(0.7, ge=0.0, le=1.0, description="Umbral mínimo de similitud"),
    match_count: int = Query(10, ge=1, le=50, description="Número máximo de resultados"),
    filter_species: Optional[str] = Query(None, description="Filtrar por especie"),
    filter_type: Optional[str] = Query(None, description="Filtrar por tipo (lost/found)")
):
    """
    Búsqueda RAG con filtro geográfico.
    Combina similitud de embeddings con proximidad geográfica.
    """
    try:
        # Validar que el embedding tenga 512 dimensiones
        if len(embedding) != 512:
            raise HTTPException(400, f"El embedding debe tener 512 dimensiones, se recibieron {len(embedding)}")
        
        sb = _sb()
        
        # Llamar a la función SQL de búsqueda con ubicación
        result = sb.rpc('search_similar_reports_with_location', {
            'query_embedding': embedding,
            'user_lat': user_lat,
            'user_lng': user_lng,
            'max_distance_km': max_distance_km,
            'match_threshold': match_threshold,
            'match_count': match_count,
            'filter_species': filter_species,
            'filter_type': filter_type
        }).execute()
        
        if not result.data:
            return {
                "results": [],
                "count": 0,
                "message": "No se encontraron reportes similares en el área especificada"
            }
        
        return {
            "results": result.data,
            "count": len(result.data),
            "search_params": {
                "user_location": {"lat": user_lat, "lng": user_lng},
                "max_distance_km": max_distance_km,
                "match_threshold": match_threshold,
                "match_count": match_count,
                "filter_species": filter_species,
                "filter_type": filter_type
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error en búsqueda RAG con ubicación: {str(e)}")

@router.post("/save-embedding/{report_id}")
async def save_embedding(
    report_id: str,
    embedding: List[float] = Body(..., description="Vector de embedding (512 dimensiones)")
):
    """
    Guarda un embedding en Supabase para un reporte específico.
    """
    try:
        # Validar que el embedding tenga 512 dimensiones
        if len(embedding) != 512:
            raise HTTPException(400, f"El embedding debe tener 512 dimensiones, se recibieron {len(embedding)}")
        
        sb = _sb()
        
        # Usar la función RPC para actualizar el embedding
        result = sb.rpc('update_report_embedding', {
            'report_id': report_id,
            'embedding_vector': embedding
        }).execute()
        
        if not result.data:
            raise HTTPException(404, f"Reporte {report_id} no encontrado")
        
        return {
            "success": True,
            "report_id": report_id,
            "message": "Embedding guardado exitosamente",
            "embedding_dimensions": len(embedding)
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error guardando embedding: {str(e)}")

@router.get("/embedding/{report_id}")
async def get_embedding(report_id: str):
    """
    Obtiene el embedding de un reporte específico.
    """
    try:
        sb = _sb()
        
        result = sb.rpc('get_report_embedding', {
            'report_id': report_id
        }).execute()
        
        if not result.data or result.data is None:
            raise HTTPException(404, f"Reporte {report_id} no tiene embedding o no existe")
        
        # El embedding viene como vector de pgvector
        embedding = result.data
        
        return {
            "report_id": report_id,
            "embedding": embedding if isinstance(embedding, list) else embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding),
            "dimensions": len(embedding) if isinstance(embedding, (list, np.ndarray)) else 512
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(500, f"Error obteniendo embedding: {str(e)}")

@router.get("/has-embedding/{report_id}")
async def check_has_embedding(report_id: str):
    """
    Verifica si un reporte tiene embedding.
    """
    try:
        sb = _sb()
        
        result = sb.rpc('has_embedding', {
            'report_id': report_id
        }).execute()
        
        return {
            "report_id": report_id,
            "has_embedding": result.data if isinstance(result.data, bool) else bool(result.data)
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error verificando embedding: {str(e)}")

@router.get("/stats")
async def get_rag_stats():
    """
    Obtiene estadísticas sobre los embeddings en la base de datos.
    """
    try:
        sb = _sb()
        
        # Contar total de reportes
        total_result = sb.table("reports").select("id", count="exact").execute()
        total_count = total_result.count if hasattr(total_result, 'count') else len(total_result.data)
        
        # Contar reportes con embedding
        with_embedding_result = sb.table("reports").select("id", count="exact").not_.is_("embedding", "null").execute()
        with_embedding_count = with_embedding_result.count if hasattr(with_embedding_result, 'count') else len(with_embedding_result.data)
        
        # Contar reportes activos con embedding
        active_with_embedding_result = sb.table("reports").select("id", count="exact").eq("status", "active").not_.is_("embedding", "null").execute()
        active_with_embedding_count = active_with_embedding_result.count if hasattr(active_with_embedding_result, 'count') else len(active_with_embedding_result.data)
        
        return {
            "total_reports": total_count,
            "reports_with_embedding": with_embedding_count,
            "active_reports_with_embedding": active_with_embedding_count,
            "coverage_percentage": round((with_embedding_count / total_count * 100) if total_count > 0 else 0, 2),
            "embedding_dimensions": 512
        }
        
    except Exception as e:
        raise HTTPException(500, f"Error obteniendo estadísticas: {str(e)}")



