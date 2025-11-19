#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
from pathlib import Path
from dotenv import load_dotenv
import numpy as np

load_dotenv(Path(__file__).parent / ".env")
from supabase import create_client

sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

print("=" * 70)
print("DEBUG: BÚSQUEDA MANUAL DE MATCHES")
print("=" * 70)

# Obtener el reporte found
found_reports = sb.table("reports").select("id, pet_name, type, embedding, species").eq("type", "found").execute()
print(f"\n🟢 Reportes FOUND: {len(found_reports.data)}")

if not found_reports.data:
    print("❌ No hay reportes 'found' para buscar")
    sys.exit(1)

found = found_reports.data[0]
print(f"   ID: {found['id']}")
print(f"   Nombre: {found.get('pet_name', 'Sin nombre')}")
print(f"   Tiene embedding: {'✅' if found.get('embedding') else '❌'}")
if found.get('embedding'):
    print(f"   Dimensiones: {len(found['embedding'])}")

# Obtener reportes lost
lost_reports = sb.table("reports").select("id, pet_name, type, embedding, species").eq("type", "lost").execute()
print(f"\n🔴 Reportes LOST: {len(lost_reports.data)}")

if not lost_reports.data:
    print("❌ No hay reportes 'lost' para comparar")
    sys.exit(1)

# Comparar embeddings manualmente
found_emb = np.array(found['embedding'], dtype=np.float32)

print("\n🔍 Calculando similitudes:")
print("-" * 70)

for lost in lost_reports.data:
    nombre = lost.get('pet_name', 'Sin nombre')
    especie = lost.get('species', 'N/A')
    
    if not lost.get('embedding'):
        print(f"   {nombre}: ❌ Sin embedding")
        continue
    
    lost_emb = np.array(lost['embedding'], dtype=np.float32)
    
    # Similitud coseno
    similarity = float(np.dot(found_emb, lost_emb))
    
    match_status = "✅ MATCH!" if similarity >= 0.7 else "❌ No match"
    print(f"   {nombre} ({especie}): {similarity:.4f} ({similarity:.1%}) {match_status}")

print("\n" + "=" * 70)
print("💡 Threshold para match: >= 0.7 (70%)")
print("=" * 70)


