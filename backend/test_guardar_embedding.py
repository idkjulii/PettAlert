#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
from pathlib import Path
from dotenv import load_dotenv
import json

load_dotenv(Path(__file__).parent / ".env")
from supabase import create_client

sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

print("=" * 70)
print("TEST: GUARDAR EMBEDDING CON DIFERENTES MÉTODOS")
print("=" * 70)

# Obtener un reporte existente
report = sb.table("reports").select("id").limit(1).execute()
if not report.data:
    print("❌ No hay reportes para probar")
    sys.exit(1)

report_id = report.data[0]["id"]
print(f"\n🔍 Usando reporte ID: {report_id}")

# Crear un embedding de prueba (pequeño para debug)
test_embedding = [0.1, 0.2, 0.3, 0.4, 0.5] * 307 + [0.1]  # 1536 valores
print(f"📊 Embedding de prueba: {len(test_embedding)} dimensiones")

# MÉTODO 1: Intentar con json.dumps (como está en el código actual)
print("\n" + "=" * 70)
print("MÉTODO 1: json.dumps() → RPC")
print("=" * 70)

vec_str = json.dumps(test_embedding)
print(f"Formato enviado: {type(vec_str).__name__}")
print(f"Longitud string: {len(vec_str)}")
print(f"Primeros 100 chars: {vec_str[:100]}")

try:
    result = sb.rpc('update_report_embedding', {
        'report_id': str(report_id),
        'embedding_vector': vec_str
    }).execute()
    print(f"✅ RPC retornó: {result.data}")
except Exception as e:
    print(f"❌ Error: {e}")

# Verificar qué se guardó
check = sb.table("reports").select("embedding").eq("id", report_id).execute()
emb = check.data[0]["embedding"]
print(f"\n📊 Lo que se guardó:")
print(f"   Tipo: {type(emb).__name__}")
if isinstance(emb, str):
    print(f"   ❌ STRING (longitud: {len(emb)})")
elif isinstance(emb, list):
    print(f"   ✅ ARRAY (dimensiones: {len(emb)})")
    print(f"   Tipo elementos: {type(emb[0]).__name__}")

# MÉTODO 2: Intentar con UPDATE directo (sin RPC)
print("\n" + "=" * 70)
print("MÉTODO 2: UPDATE directo con casting")
print("=" * 70)

try:
    # Usar la query cruda de PostgreSQL
    vec_str_pg = "[" + ",".join(map(str, test_embedding)) + "]"
    print(f"Formato: {vec_str_pg[:100]}...")
    
    result = sb.table('reports').update({
        'embedding': vec_str_pg
    }).eq('id', report_id).execute()
    
    print(f"✅ UPDATE completado")
except Exception as e:
    print(f"❌ Error: {e}")

# Verificar qué se guardó
check = sb.table("reports").select("embedding").eq("id", report_id).execute()
emb = check.data[0]["embedding"]
print(f"\n📊 Lo que se guardó:")
print(f"   Tipo: {type(emb).__name__}")
if isinstance(emb, str):
    print(f"   ❌ STRING (longitud: {len(emb)})")
elif isinstance(emb, list):
    print(f"   ✅ ARRAY (dimensiones: {len(emb)})")
    print(f"   Tipo elementos: {type(emb[0]).__name__}")

print("\n" + "=" * 70)




