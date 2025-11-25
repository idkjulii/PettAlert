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
print("VERIFICACIÓN: ÚLTIMO REPORTE CREADO")
print("=" * 70)

reports = sb.table("reports").select("id, pet_name, type, embedding, created_at").order("created_at", desc=True).limit(1).execute()

if not reports.data:
    print("\n❌ No hay reportes en la base de datos")
    sys.exit(0)

r = reports.data[0]
nombre = r.get("pet_name", "Sin nombre")
tipo = r.get("type", "N/A")
emb = r.get("embedding")
created = r.get("created_at", "N/A")

print(f"\n📝 Último reporte creado:")
print(f"   Nombre: {nombre}")
print(f"   Tipo: {tipo}")
print(f"   Creado: {created}")
print()

if not emb:
    print(f"❌ SIN EMBEDDING")
    print("   El backend NO generó el embedding.")
    print("   Verifica que el backend esté corriendo correctamente.")
elif isinstance(emb, str):
    print(f"❌ EMBEDDING COMO STRING (longitud: {len(emb)})")
    print(f"   Primeros 50 chars: {emb[:50]}")
    print()
    print("   PROBLEMA: El backend NO se reinició correctamente.")
    print("   El código viejo sigue corriendo.")
elif isinstance(emb, list):
    print(f"✅ EMBEDDING COMO ARRAY ({len(emb)} dimensiones)")
    print(f"   Primeros 3 valores: {emb[:3]}")
    print(f"   Tipo del primer elemento: {type(emb[0]).__name__}")
    print()
    print("   🎉 ¡PERFECTO! El fix está funcionando.")
else:
    print(f"⚠️ TIPO DESCONOCIDO: {type(emb).__name__}")

print("\n" + "=" * 70)




