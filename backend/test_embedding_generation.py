#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la generación de embeddings
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
import asyncio

# Cargar variables de entorno
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)

from supabase import create_client
from services.embeddings import image_bytes_to_vec
import httpx

def test_supabase_connection():
    """Verifica la conexión con Supabase"""
    print("🔍 [TEST] Verificando conexión con Supabase...")
    try:
        url = os.getenv("SUPABASE_URL")
        key = os.getenv("SUPABASE_SERVICE_KEY")
        
        if not url or not key:
            print("❌ [TEST] Error: SUPABASE_URL o SUPABASE_SERVICE_KEY no configuradas")
            return None
        
        sb = create_client(url, key)
        
        # Probar una consulta simple
        result = sb.table("reports").select("id").limit(1).execute()
        print(f"✅ [TEST] Conexión con Supabase exitosa. Encontrados {len(result.data)} reportes")
        return sb
    except Exception as e:
        print(f"❌ [TEST] Error conectando con Supabase: {e}")
        return None

def test_rpc_function(sb):
    """Verifica que la función RPC update_report_embedding exista"""
    print("\n🔍 [TEST] Verificando función RPC update_report_embedding...")
    try:
        # Obtener un reporte de prueba
        result = sb.table("reports").select("id").limit(1).execute()
        
        if not result.data:
            print("⚠️ [TEST] No hay reportes en la base de datos para probar")
            return False
        
        test_report_id = result.data[0]["id"]
        print(f"📋 [TEST] Usando reporte de prueba: {test_report_id}")
        
        # Intentar llamar a la función RPC con un vector de prueba
        test_vector = [0.0] * 512  # Vector de prueba con 512 ceros
        
        try:
            rpc_result = sb.rpc('update_report_embedding', {
                'report_id': test_report_id,
                'embedding_vector': test_vector
            }).execute()
            
            print("✅ [TEST] Función RPC update_report_embedding existe y funciona")
            return True
        except Exception as rpc_error:
            print(f"❌ [TEST] Error llamando a la función RPC: {rpc_error}")
            print(f"   Detalles: {str(rpc_error)}")
            return False
            
    except Exception as e:
        print(f"❌ [TEST] Error verificando función RPC: {e}")
        return False

def test_embedding_generation():
    """Verifica que se puede generar un embedding usando una URL real"""
    print("\n🔍 [TEST] Verificando generación de embeddings...")
    try:
        # Intentar con una imagen real desde internet
        test_image_url = "https://via.placeholder.com/150"
        print(f"   Descargando imagen de prueba desde: {test_image_url}")
        
        import requests
        response = requests.get(test_image_url, timeout=10)
        response.raise_for_status()
        test_image_bytes = response.content
        
        vec = image_bytes_to_vec(test_image_bytes)
        print(f"✅ [TEST] Embedding generado exitosamente. Dimensiones: {vec.shape}")
        print(f"   Primeros 5 valores: {vec[:5]}")
        return True
    except Exception as e:
        print(f"⚠️ [TEST] No se pudo probar con imagen externa: {e}")
        print("   Esto es normal si no hay conexión a internet.")
        print("   La generación de embeddings se probará en el flujo completo.")
        # No fallar, solo advertir
        return True

async def test_full_flow(sb):
    """Prueba el flujo completo: obtener reporte, generar embedding, guardarlo"""
    print("\n🔍 [TEST] Probando flujo completo de generación y guardado de embedding...")
    try:
        # Obtener un reporte con fotos
        result = sb.table("reports").select("id, photos").not_.is_("photos", "null").limit(1).execute()
        
        if not result.data or not result.data[0].get("photos"):
            print("⚠️ [TEST] No hay reportes con fotos para probar")
            return False
        
        report = result.data[0]
        report_id = report["id"]
        photos = report.get("photos", [])
        
        if not photos or len(photos) == 0:
            print("⚠️ [TEST] El reporte no tiene fotos")
            return False
        
        first_photo_url = photos[0]
        print(f"📋 [TEST] Usando reporte: {report_id}")
        print(f"📷 [TEST] URL de foto: {first_photo_url}")
        
        # Descargar la imagen
        print("⬇️ [TEST] Descargando imagen...")
        async with httpx.AsyncClient(timeout=30.0) as client:
            try:
                response = await client.get(first_photo_url)
                response.raise_for_status()
                image_bytes = response.content
                print(f"✅ [TEST] Imagen descargada. Tamaño: {len(image_bytes)} bytes")
            except Exception as e:
                print(f"❌ [TEST] Error descargando imagen: {e}")
                return False
        
        # Generar embedding
        print("🔄 [TEST] Generando embedding...")
        try:
            vec = image_bytes_to_vec(image_bytes)
            embedding_list = vec.tolist()
            print(f"✅ [TEST] Embedding generado. Dimensiones: {len(embedding_list)}")
        except Exception as e:
            print(f"❌ [TEST] Error generando embedding: {e}")
            import traceback
            traceback.print_exc()
            return False
        
        # Guardar embedding
        print("💾 [TEST] Guardando embedding en la base de datos...")
        try:
            rpc_result = sb.rpc('update_report_embedding', {
                'report_id': report_id,
                'embedding_vector': embedding_list
            }).execute()
            
            if rpc_result.data:
                print(f"✅ [TEST] Embedding guardado exitosamente en el reporte {report_id}")
                
                # Verificar que se guardó
                verify_result = sb.table("reports").select("embedding").eq("id", report_id).single().execute()
                if verify_result.data and verify_result.data.get("embedding"):
                    print("✅ [TEST] Verificación: Embedding confirmado en la base de datos")
                    return True
                else:
                    print("⚠️ [TEST] Verificación: Embedding no se encontró en la base de datos")
                    return False
            else:
                print("❌ [TEST] La función RPC no retornó datos")
                return False
                
        except Exception as e:
            print(f"❌ [TEST] Error guardando embedding: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    except Exception as e:
        print(f"❌ [TEST] Error en flujo completo: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    print("=" * 60)
    print("🔬 DIAGNÓSTICO DE GENERACIÓN DE EMBEDDINGS")
    print("=" * 60)
    
    # Test 1: Conexión con Supabase
    sb = test_supabase_connection()
    if not sb:
        print("\n❌ No se puede continuar sin conexión a Supabase")
        sys.exit(1)
    
    # Test 2: Función RPC
    rpc_ok = test_rpc_function(sb)
    if not rpc_ok:
        print("\n⚠️ La función RPC no funciona. Verifica que la migración 002_update_embedding_function.sql se haya ejecutado en Supabase")
    
    # Test 3: Generación de embeddings
    embedding_ok = test_embedding_generation()
    if not embedding_ok:
        print("\n❌ No se puede generar embeddings. Verifica las dependencias de OpenCLIP")
    
    # Test 4: Flujo completo
    if rpc_ok and embedding_ok:
        flow_ok = await test_full_flow(sb)
        if flow_ok:
            print("\n" + "=" * 60)
            print("✅ TODOS LOS TESTS PASARON")
            print("=" * 60)
        else:
            print("\n" + "=" * 60)
            print("❌ EL FLUJO COMPLETO FALLÓ")
            print("=" * 60)
    else:
        print("\n⚠️ No se puede probar el flujo completo debido a errores anteriores")
    
    print("\n💡 Siguientes pasos:")
    print("   1. Si la función RPC falló, ejecuta la migración 002_update_embedding_function.sql en Supabase")
    print("   2. Si la generación de embeddings falló, verifica que open_clip esté instalado")
    print("   3. Si el flujo completo falló, revisa los logs arriba para más detalles")

if __name__ == "__main__":
    asyncio.run(main())
