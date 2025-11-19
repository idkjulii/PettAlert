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
print("VERIFICACIÓN: EMBEDDINGS DESPUÉS DEL FIX")
print("=" * 70)

reports = sb.table("reports").select("id, pet_name, type, embedding").execute()

if not reports.data:
    print("\n❌ No hay reportes en la base de datos")
    print("   Crea algunos reportes desde la app móvil primero")
    sys.exit(0)

print(f"\n📊 Total reportes: {len(reports.data)}\n")

todo_ok = True

for r in reports.data:
    nombre = r.get("pet_name", "Sin nombre")
    tipo = r.get("type", "N/A")
    emb = r.get("embedding")
    
    if not emb:
        print(f"❌ {nombre} ({tipo}): Sin embedding")
        todo_ok = False
    elif isinstance(emb, str):
        print(f"❌ {nombre} ({tipo}): STRING (longitud: {len(emb)}) - NO FUNCIONA")
        todo_ok = False
    elif isinstance(emb, list):
        print(f"✅ {nombre} ({tipo}): ARRAY ({len(emb)} dims) - CORRECTO")
    else:
        print(f"⚠️ {nombre} ({tipo}): Tipo desconocido: {type(emb).__name__}")
        todo_ok = False

print("\n" + "=" * 70)

if todo_ok:
    print("✅ ÉXITO: Todos los embeddings están correctos")
    print("   Ahora puedes buscar matches desde la app!")
else:
    print("❌ PROBLEMA: Algunos embeddings no están correctos")
    print("   Verifica que:")
    print("   1. Aplicaste la migración SQL en Supabase")
    print("   2. Reiniciaste el backend (uvicorn)")
    print("   3. Creaste reportes DESPUÉS de reiniciar")

print("=" * 70)


