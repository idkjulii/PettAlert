#!/usr/bin/env python3
"""
Script rápido para probar la generación de embeddings con un reporte real
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import asyncio
import httpx

# Cargar variables de entorno
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)

from supabase import create_client
from services.embeddings import image_bytes_to_vec

def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL o SUPABASE_SERVICE_KEY no configuradas")
    return create_client(url, key)

async def test_with_real_report():
    print("=" * 60)
    print("🧪 PROBANDO GENERACIÓN DE EMBEDDINGS CON REPORTE REAL")
    print("=" * 60)
    
    sb = get_supabase()
    
    # Obtener un reporte con fotos pero sin embedding
    print("\n📥 Buscando reporte con fotos...")
    result = sb.table("reports").select("id, photos, embedding").not_.is_("photos", "null").limit(5).execute()
    
    if not result.data:
        print("❌ No se encontraron reportes con fotos")
        return
    
    # Buscar uno sin embedding
    report = None
    for r in result.data:
        if r.get("embedding") is None:
            report = r
            break
    
    if not report:
        print("⚠️ Todos los reportes ya tienen embeddings. Usando el primero...")
        report = result.data[0]
    
    report_id = report["id"]
    photos = report.get("photos", [])
    has_embedding = report.get("embedding") is not None
    
    print(f"\n📋 Reporte seleccionado: {report_id}")
    print(f"   Fotos: {len(photos) if photos else 0}")
    print(f"   Tiene embedding: {'Sí' if has_embedding else 'No'}")
    
    if not photos or len(photos) == 0:
        print("❌ El reporte no tiene fotos")
        return
    
    first_photo_url = photos[0]
    print(f"\n📷 URL de la primera foto: {first_photo_url}")
    
    # Descargar imagen
    print("\n⬇️ Descargando imagen...")
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(first_photo_url)
            response.raise_for_status()
            image_bytes = response.content
            print(f"✅ Imagen descargada: {len(image_bytes)} bytes")
    except Exception as e:
        print(f"❌ Error descargando imagen: {e}")
        return
    
    # Generar embedding
    print("\n🔄 Generando embedding...")
    try:
        vec = image_bytes_to_vec(image_bytes)
        embedding_list = vec.tolist()
        print(f"✅ Embedding generado: {len(embedding_list)} dimensiones")
        print(f"   Primeros valores: {embedding_list[:5]}")
    except Exception as e:
        print(f"❌ Error generando embedding: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Guardar embedding
    print("\n💾 Guardando embedding en la base de datos...")
    try:
        rpc_result = sb.rpc('update_report_embedding', {
            'report_id': report_id,
            'embedding_vector': embedding_list
        }).execute()
        
        if rpc_result.data:
            print("✅ Función RPC ejecutada")
        else:
            print("⚠️ Función RPC no retornó datos")
        
        # Verificar que se guardó
        print("\n🔍 Verificando que se guardó...")
        verify_result = sb.table("reports").select("embedding").eq("id", report_id).single().execute()
        
        if verify_result.data and verify_result.data.get("embedding"):
            embedding_saved = verify_result.data["embedding"]
            if isinstance(embedding_saved, list) and len(embedding_saved) == 512:
                print(f"✅✅✅ ÉXITO: Embedding guardado correctamente!")
                print(f"   Dimensiones: {len(embedding_saved)}")
                print(f"   Primeros valores guardados: {embedding_saved[:5]}")
            else:
                print(f"⚠️ Embedding guardado pero formato inesperado: {type(embedding_saved)}")
        else:
            print("❌ Embedding no se encontró en la base de datos")
            print("   Esto puede indicar un problema con la función RPC o permisos")
            
    except Exception as e:
        print(f"❌ Error guardando embedding: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_with_real_report())
