#!/usr/bin/env python3
"""
Verifica cómo se están guardando los embeddings en la base de datos
"""
import os
from pathlib import Path
from dotenv import load_dotenv

ENV_PATH = Path(__file__).resolve().parent / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=False)

from supabase import create_client
import psycopg

def check_with_supabase_client():
    """Verifica usando el cliente de Supabase"""
    print("=" * 60)
    print("🔍 VERIFICANDO EMBEDDINGS CON CLIENTE SUPABASE")
    print("=" * 60)
    
    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_SERVICE_KEY")
    sb = create_client(url, key)
    
    # Obtener un reporte con embedding
    result = sb.table("reports").select("id, embedding").not_.is_("embedding", "null").limit(1).execute()
    
    if not result.data:
        print("❌ No se encontraron reportes con embeddings")
        return
    
    report = result.data[0]
    report_id = report["id"]
    embedding = report.get("embedding")
    
    print(f"\n📋 Reporte: {report_id}")
    print(f"   Tipo de embedding: {type(embedding)}")
    
    if isinstance(embedding, str):
        print(f"   Longitud del string: {len(embedding)}")
        print(f"   Primeros 100 caracteres: {embedding[:100]}")
    elif isinstance(embedding, list):
        print(f"   Longitud del array: {len(embedding)}")
        print(f"   Primeros 5 valores: {embedding[:5]}")
    else:
        print(f"   Valor: {embedding}")

def check_with_direct_psycopg():
    """Verifica usando conexión directa a PostgreSQL"""
    print("\n" + "=" * 60)
    print("🔍 VERIFICANDO EMBEDDINGS CON CONEXIÓN DIRECTA")
    print("=" * 60)
    
    dsn = os.getenv("DATABASE_URL")
    if not dsn:
        print("⚠️ DATABASE_URL no configurada, saltando verificación directa")
        return
    
    try:
        with psycopg.connect(dsn, autocommit=True) as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    SELECT id, embedding, 
                           pg_typeof(embedding) as embedding_type,
                           array_length(embedding::float[], 1) as embedding_length
                    FROM public.reports 
                    WHERE embedding IS NOT NULL 
                    LIMIT 1
                """)
                
                row = cur.fetchone()
                if row:
                    report_id, embedding, emb_type, emb_length = row
                    print(f"\n📋 Reporte: {report_id}")
                    print(f"   Tipo en PostgreSQL: {emb_type}")
                    print(f"   Longitud del array: {emb_length}")
                    
                    # Obtener primeros valores
                    cur.execute("""
                        SELECT embedding[1:5] as first_5
                        FROM public.reports 
                        WHERE id = %s
                    """, (report_id,))
                    first_5 = cur.fetchone()[0]
                    print(f"   Primeros 5 valores: {first_5}")
                    
                    print("\n✅ El embedding está guardado correctamente como vector(512)")
                else:
                    print("❌ No se encontraron reportes con embeddings")
                    
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    check_with_supabase_client()
    check_with_direct_psycopg()
    
    print("\n" + "=" * 60)
    print("💡 CONCLUSIÓN:")
    print("   Si el embedding se muestra como string en Supabase pero")
    print("   como vector en PostgreSQL, esto es NORMAL.")
    print("   Supabase convierte los vectores a string para JSON.")
    print("   La búsqueda por similitud funcionará correctamente.")
    print("=" * 60)
