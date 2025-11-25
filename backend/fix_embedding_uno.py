#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
from pathlib import Path
from dotenv import load_dotenv
import httpx

load_dotenv(Path(__file__).parent / ".env")
from supabase import create_client

sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

print("=" * 70)
print("FIX: REGENERAR UN EMBEDDING CORRECTAMENTE")
print("=" * 70)

# Obtener el primer reporte found
report = sb.table("reports").select("*").eq("type", "found").limit(1).execute()

if not report.data:
    print("❌ No hay reportes found")
    sys.exit(1)

r = report.data[0]
report_id = r["id"]
photo_url = r.get("photos", [None])[0]

if not photo_url:
    print("❌ Reporte no tiene foto")
    sys.exit(1)

print(f"\n🔄 Procesando reporte: {r.get('pet_name', 'Sin nombre')}")
print(f"   ID: {report_id}")
print(f"   Foto: {photo_url[:80]}...")

# Descargar imagen
print("\n📥 Descargando imagen...")
response = httpx.get(photo_url, follow_redirects=True, timeout=30.0)
image_bytes = response.content
print(f"   ✅ Imagen descargada ({len(image_bytes)} bytes)")

# Generar embedding
print("\n🔄 Generando embedding...")
from services.embeddings import image_bytes_to_vec
vec = image_bytes_to_vec(image_bytes)
vec_list = vec.tolist()
print(f"   ✅ Embedding generado: {len(vec_list)} dimensiones")

# OPCIÓN 1: Intentar con RPC
print("\n📤 Intentando guardar con RPC...")
try:
    result = sb.rpc('update_report_embedding', {
        'report_id': str(report_id),
        'embedding_vector': vec_list
    }).execute()
    print(f"   Resultado RPC: {result.data}")
except Exception as e:
    print(f"   ❌ Error con RPC: {e}")

# Verificar qué se guardó
print("\n🔍 Verificando embedding guardado...")
check = sb.table("reports").select("embedding").eq("id", report_id).execute()
emb = check.data[0]["embedding"]

print(f"\n📊 RESULTADO:")
print(f"   Tipo: {type(emb).__name__}")

if isinstance(emb, str):
    print(f"   ❌ STRING (longitud: {len(emb)})")
    print(f"   Primeros 100 chars: {emb[:100]}")
elif isinstance(emb, list):
    print(f"   ✅ ARRAY (dimensiones: {len(emb)})")
    print(f"   Primeros 3 valores: {emb[:3]}")
    print(f"   Tipo del primer elemento: {type(emb[0]).__name__}")

print("\n" + "=" * 70)




