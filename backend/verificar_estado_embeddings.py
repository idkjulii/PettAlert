#!/usr/bin/env python3
"""
Script para verificar el estado de los embeddings después de la migración
Muestra estadísticas sobre embeddings existentes y su dimensión
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno
ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)

from supabase import create_client

def get_supabase():
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise RuntimeError("SUPABASE_URL o SUPABASE_SERVICE_KEY no configuradas")
    return create_client(url, key)

def main():
    # Configurar encoding para Windows ANTES de cualquier print
    import sys
    if sys.platform == 'win32':
        import io
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    
    print("=" * 70)
    print("VERIFICACIÓN DE EMBEDDINGS POST-MIGRACIÓN")
    print("=" * 70)
    print()
    
    try:
        sb = get_supabase()
    except Exception as e:
        print(f"❌ Error conectando con Supabase: {e}")
        print("\nVerifica que tu archivo .env tenga:")
        print("  - SUPABASE_URL")
        print("  - SUPABASE_SERVICE_KEY")
        return
    
    print("✅ Conectado a Supabase")
    print()
    
    # Estadísticas generales
    print("📊 ESTADÍSTICAS GENERALES")
    print("-" * 70)
    try:
        result = sb.table("reports").select("id, embedding, photos, created_at").execute()
        reports = result.data
        
        total = len(reports)
        con_embedding = sum(1 for r in reports if r.get("embedding"))
        sin_embedding = total - con_embedding
        con_fotos = sum(1 for r in reports if r.get("photos") and len(r.get("photos", [])) > 0)
        sin_fotos = total - con_fotos
        
        print(f"  Total de reportes:           {total}")
        print(f"  Reportes con embedding:      {con_embedding}")
        print(f"  Reportes sin embedding:      {sin_embedding}")
        print(f"  Reportes con fotos:          {con_fotos}")
        print(f"  Reportes sin fotos:          {sin_fotos}")
        print()
        
        if sin_embedding > 0 and con_fotos > sin_embedding:
            pendientes = con_fotos - con_embedding
            print(f"⚠️  ATENCIÓN: {pendientes} reportes con fotos necesitan embeddings")
            print()
    except Exception as e:
        print(f"❌ Error obteniendo estadísticas: {e}")
        print()
    
    # Verificar dimensiones de embeddings existentes
    print("📏 DIMENSIONES DE EMBEDDINGS EXISTENTES")
    print("-" * 70)
    try:
        result = sb.table("reports")\
            .select("id, embedding, created_at")\
            .not_.is_("embedding", "null")\
            .limit(10)\
            .execute()
        
        reports_con_emb = result.data
        
        if not reports_con_emb:
            print("  ℹ️  No hay reportes con embeddings")
            print()
        else:
            print("  Mostrando primeros 10 reportes con embeddings:")
            print()
            
            dimensiones_vistas = {}
            
            for report in reports_con_emb:
                embedding = report.get("embedding")
                report_id = report.get("id")
                created_at = report.get("created_at", "")[:10]
                
                if embedding and isinstance(embedding, list):
                    dims = len(embedding)
                    dimensiones_vistas[dims] = dimensiones_vistas.get(dims, 0) + 1
                    
                    # Indicador de versión
                    version = "❌ CLIP (viejo)" if dims == 512 else "✅ MegaDescriptor" if dims == 1536 else "⚠️ Desconocido"
                    
                    print(f"  - ID: {report_id[:8]}... | {dims} dims | {version} | {created_at}")
            
            print()
            print("  📊 Resumen de dimensiones:")
            for dims, count in sorted(dimensiones_vistas.items()):
                version = "CLIP (viejo)" if dims == 512 else "MegaDescriptor" if dims == 1536 else "Desconocido"
                print(f"     {dims} dims ({version}): {count} reportes")
            
            print()
            
            # Advertencias
            if 512 in dimensiones_vistas:
                print("  ⚠️  ADVERTENCIA: Se encontraron embeddings de 512 dimensiones (CLIP)")
                print("     Estos son de la versión anterior y deberían regenerarse.")
                print()
                print("     Ejecuta: python -m scripts.regenerate_embeddings_mega")
                print()
            elif 1536 in dimensiones_vistas:
                print("  ✅ Todos los embeddings están en formato MegaDescriptor (1536 dims)")
                print()
    
    except Exception as e:
        print(f"❌ Error verificando dimensiones: {e}")
        print()
    
    # Verificar configuración de variables de entorno
    print("⚙️  CONFIGURACIÓN DE VARIABLES DE ENTORNO")
    print("-" * 70)
    generate_locally = os.getenv("GENERATE_EMBEDDINGS_LOCALLY", "false")
    auto_send_n8n = os.getenv("AUTO_SEND_REPORTS_TO_N8N", "false")
    
    print(f"  GENERATE_EMBEDDINGS_LOCALLY: {generate_locally}")
    if generate_locally.lower() in ("1", "true", "yes"):
        print("    ✅ Generación local ACTIVADA")
    else:
        print("    ⚠️  Generación local DESACTIVADA")
        print("       Los nuevos reportes NO generarán embeddings automáticamente")
        print("       Cambia a 'true' en tu archivo .env")
    
    print()
    print(f"  AUTO_SEND_REPORTS_TO_N8N: {auto_send_n8n}")
    if auto_send_n8n.lower() in ("1", "true", "yes"):
        print("    ✅ Envío a N8N ACTIVADO")
    else:
        print("    ℹ️  Envío a N8N DESACTIVADO")
    
    print()
    
    # Recomendaciones
    print("📋 PRÓXIMOS PASOS RECOMENDADOS")
    print("-" * 70)
    
    if sin_embedding > 0:
        print("  1. ⚠️  Regenerar embeddings para reportes existentes:")
        print("     python -m scripts.regenerate_embeddings_mega")
        print()
    
    if generate_locally.lower() not in ("1", "true", "yes"):
        print("  2. ⚠️  Activar generación local de embeddings:")
        print("     Edita tu .env y agrega: GENERATE_EMBEDDINGS_LOCALLY=true")
        print("     Luego reinicia el backend")
        print()
    
    print("  3. ✅ Probar generación de embedding:")
    print("     curl -X POST 'http://127.0.0.1:8010/embeddings/generate' \\")
    print("       -F 'file=@test_image.jpg'")
    print()
    
    print("=" * 70)
    print("Verificación completada")
    print("=" * 70)

if __name__ == "__main__":
    main()

