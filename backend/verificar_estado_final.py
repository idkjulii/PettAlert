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

result = sb.table("reports").select("id, pet_name, type, embedding").execute()

total = len(result.data)
con_emb = sum(1 for r in result.data if r.get("embedding"))
sin_emb = total - con_emb

print("=" * 70)
print("ESTADO FINAL DE LA MIGRACIÓN")
print("=" * 70)
print(f"\n📊 Total reportes: {total}")
print(f"✅ Con embedding: {con_emb}")
print(f"❌ Sin embedding: {sin_emb}")

if con_emb > 0:
    # Ver dimensiones
    dims_count = {}
    for r in result.data:
        if r.get("embedding"):
            dims = len(r["embedding"])
            dims_count[dims] = dims_count.get(dims, 0) + 1
    
    print(f"\n📏 Dimensiones de embeddings:")
    for dims, count in sorted(dims_count.items()):
        modelo = "MegaDescriptor ✅" if dims == 1536 else "CLIP (viejo) ❌" if dims == 512 else "?"
        print(f"   {dims} dims ({modelo}): {count} reportes")

print(f"\n🐾 Reportes por tipo:")
tipos = {"lost": 0, "found": 0}
for r in result.data:
    tipo = r.get("type", "N/A")
    if tipo in tipos:
        tipos[tipo] += 1

print(f"   🔴 Perdidos (lost): {tipos['lost']}")
print(f"   🟢 Encontrados (found): {tipos['found']}")

print(f"\n📋 Lista de reportes:")
for i, r in enumerate(result.data[:10], 1):
    nombre = r.get("pet_name", "Sin nombre")
    tipo = "🔴" if r.get("type") == "lost" else "🟢"
    dims = len(r.get("embedding", [])) if r.get("embedding") else 0
    emb_status = f"✅ {dims}" if dims > 0 else "❌ sin emb"
    print(f"   {i}. {tipo} {nombre}: {emb_status}")

print("\n" + "=" * 70)
print("✅ MIGRACIÓN COMPLETADA EXITOSAMENTE" if con_emb == total and 1536 in dims_count else "⚠️ Verificar estado")
print("=" * 70)


