#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
from pathlib import Path
from dotenv import load_dotenv
import json
import numpy as np

load_dotenv(Path(__file__).parent / ".env")
from supabase import create_client

sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

print("=" * 70)
print("CALCULAR SIMILITUD: TONY vs SIN NOMBRE")
print("=" * 70)

try:
    # Obtener los dos últimos reportes
    reports = sb.table("reports").select("*").order("created_at", desc=True).limit(2).execute()
    
    if len(reports.data) < 2:
        print("\n❌ Necesitas al menos 2 reportes")
        sys.exit(1)
    
    r1 = reports.data[0]  # Tony (lost)
    r2 = reports.data[1]  # Sin nombre (found)
    
    print(f"\n📊 Reporte 1: {r1.get('pet_name', 'Sin nombre')} ({r1.get('type')})")
    print(f"   ID: {r1['id'][:16]}...")
    
    print(f"\n📊 Reporte 2: {r2.get('pet_name', 'Sin nombre')} ({r2.get('type')})")
    print(f"   ID: {r2['id'][:16]}...")
    
    emb1 = r1.get("embedding")
    emb2 = r2.get("embedding")
    
    if not emb1 or not emb2:
        print("\n❌ Uno de los reportes no tiene embedding")
        sys.exit(1)
    
    # Parsear si son strings
    if isinstance(emb1, str):
        emb1 = json.loads(emb1)
        print(f"\n✅ Embedding 1: Parseado desde string, {len(emb1)} dims")
    else:
        print(f"\n✅ Embedding 1: Ya es array, {len(emb1)} dims")
    
    if isinstance(emb2, str):
        emb2 = json.loads(emb2)
        print(f"✅ Embedding 2: Parseado desde string, {len(emb2)} dims")
    else:
        print(f"✅ Embedding 2: Ya es array, {len(emb2)} dims")
    
    # Calcular similitud
    vec1 = np.array(emb1, dtype=np.float32)
    vec2 = np.array(emb2, dtype=np.float32)
    
    similarity = float(np.dot(vec1, vec2))
    
    print(f"\n" + "=" * 70)
    print(f"🔍 SIMILITUD CALCULADA: {similarity:.6f} ({similarity:.2%})")
    print("=" * 70)
    
    if similarity >= 0.7:
        print(f"\n✅ MATCH! (>= 70%)")
        print(f"   Deberían aparecer como coincidencias")
    else:
        print(f"\n❌ NO MATCH (< 70%)")
        print(f"   Son mascotas diferentes o fotos muy distintas")
        print(f"\n💡 Para probar el sistema correctamente:")
        print(f"   Crea 2 reportes con la MISMA foto")
        print(f"   La similitud debería ser ~95-100%")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)




