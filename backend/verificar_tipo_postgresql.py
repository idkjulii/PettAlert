#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).parent / ".env")
from supabase import create_client

sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

print("=" * 70)
print("VERIFICAR TIPO REAL EN POSTGRESQL")
print("=" * 70)

# Query directa a PostgreSQL para ver el tipo del campo
query = """
SELECT 
    column_name,
    data_type,
    udt_name
FROM information_schema.columns 
WHERE table_name = 'reports' 
AND column_name = 'embedding';
"""

try:
    result = sb.rpc('exec_sql', {'query': query}).execute()
    print(f"Resultado: {result}")
except Exception as e:
    print(f"Error con RPC exec_sql: {e}")
    print("\nIntentando query alternativa...")

# Intentar obtener info del tipo usando una query más simple
print("\n📊 Verificando si el vector se puede usar en búsqueda de similitud...")

# Obtener dos reportes
reports = sb.table("reports").select("id, embedding").limit(2).execute()

if len(reports.data) < 2:
    print("❌ Necesitas al menos 2 reportes para probar")
    sys.exit(1)

r1 = reports.data[0]
r2 = reports.data[1]

print(f"\nReporte 1: {r1['id']}")
print(f"  Embedding tipo: {type(r1['embedding']).__name__}")
print(f"  Es string: {isinstance(r1['embedding'], str)}")

print(f"\nReporte 2: {r2['id']}")
print(f"  Embedding tipo: {type(r2['embedding']).__name__}")

# Intentar búsqueda de similitud usando la función RPC
print("\n🔍 Intentando búsqueda de similitud con función RPC...")

try:
    # Usar el embedding del primer reporte para buscar similares
    emb1_str = r1['embedding']
    
    # La función RPC espera vector(1536), intentemos pasarle el string
    result = sb.rpc('search_similar_reports', {
        'query_embedding': emb1_str,
        'match_threshold': 0.5,
        'match_count': 5
    }).execute()
    
    print(f"✅ Búsqueda funcionó!")
    print(f"   Resultados: {len(result.data)}")
    for r in result.data[:3]:
        print(f"   - Similitud: {r.get('similarity_score', 'N/A')}")
        
except Exception as e:
    print(f"❌ Error en búsqueda: {e}")
    print("\n💡 Esto confirma que los embeddings NO están como vector en PostgreSQL")

print("\n" + "=" * 70)





