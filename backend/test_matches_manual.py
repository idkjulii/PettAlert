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
print("TEST: BÚSQUEDA MANUAL DE MATCHES")
print("=" * 70)

# Obtener todos los reportes
reports = sb.table("reports").select("id, pet_name, type, embedding, species").execute()

print(f"\n📊 Total reportes: {len(reports.data)}")

# Separar por tipo
lost = [r for r in reports.data if r.get("type") == "lost" and r.get("embedding")]
found = [r for r in reports.data if r.get("type") == "found" and r.get("embedding")]

print(f"🔴 Reportes LOST con embedding: {len(lost)}")
for r in lost:
    print(f"   - {r.get('pet_name', 'Sin nombre')} (ID: {r['id'][:8]}...)")

print(f"🟢 Reportes FOUND con embedding: {len(found)}")
for r in found:
    print(f"   - {r.get('pet_name', 'Sin nombre')} (ID: {r['id'][:8]}...)")

if len(lost) == 0 or len(found) == 0:
    print("\n⚠️ Necesitas al menos 1 reporte 'lost' y 1 'found' para buscar matches")
    sys.exit(0)

print("\n" + "=" * 70)
print("CALCULANDO SIMILITUDES")
print("=" * 70)

# Probar con el primer reporte lost
test_report = lost[0]
test_id = test_report["id"]
test_name = test_report.get("pet_name", "Sin nombre")
test_embedding = test_report["embedding"]

print(f"\n🔍 Buscando matches para: {test_name} (lost)")
print(f"   Tipo de embedding: {type(test_embedding).__name__}")

if isinstance(test_embedding, str):
    print(f"   ❌ ERROR: Embedding es STRING")
    print(f"   El reporte se creó con código viejo")
    sys.exit(1)

print(f"   ✅ Embedding es ARRAY ({len(test_embedding)} dims)")

# Convertir a numpy
try:
    base_vec = np.array(test_embedding, dtype=np.float32)
    print(f"   ✅ Convertido a numpy: {base_vec.shape}")
except Exception as e:
    print(f"   ❌ Error convirtiendo a numpy: {e}")
    sys.exit(1)

# Comparar con reportes found
print(f"\n📊 Comparando con {len(found)} reportes 'found':\n")

matches_found = []
for candidate in found:
    cand_name = candidate.get("pet_name", "Sin nombre")
    cand_embedding = candidate["embedding"]
    
    if isinstance(cand_embedding, str):
        print(f"   ⚠️ {cand_name}: Embedding es STRING (reporte viejo)")
        continue
    
    try:
        cand_vec = np.array(cand_embedding, dtype=np.float32)
        similarity = float(np.dot(base_vec, cand_vec))
        
        status = "✅ MATCH!" if similarity >= 0.7 else "❌ No match"
        print(f"   {cand_name}: {similarity:.4f} ({similarity:.1%}) {status}")
        
        if similarity >= 0.7:
            matches_found.append({
                "name": cand_name,
                "id": candidate["id"],
                "similarity": similarity
            })
    except Exception as e:
        print(f"   ❌ {cand_name}: Error - {e}")

print("\n" + "=" * 70)
print(f"📊 RESULTADO: {len(matches_found)} matches encontrados")
print("=" * 70)

if matches_found:
    print("\n✅ Matches que deberían guardarse:")
    for m in matches_found:
        print(f"   - {m['name']}: {m['similarity']:.1%} similitud")
    
    # Verificar si están guardados en la DB
    print(f"\n🔍 Verificando si están en la tabla 'matches'...")
    existing_matches = sb.table("matches").select("*").eq("lost_report_id", test_id).execute()
    
    if existing_matches.data:
        print(f"   ✅ Hay {len(existing_matches.data)} matches guardados:")
        for m in existing_matches.data:
            print(f"      - Similitud: {m.get('similarity_score', 'N/A')}")
            print(f"        Estado: {m.get('status', 'N/A')}")
    else:
        print(f"   ❌ NO hay matches guardados en la base de datos")
        print(f"   Esto significa que find_and_save_matches() no se ejecutó o falló")
else:
    print("\nℹ️ No hay coincidencias con similitud >= 70%")

print("\n" + "=" * 70)





