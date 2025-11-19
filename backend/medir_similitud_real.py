#!/usr/bin/env python3
"""
Script para medir la similitud real entre fotos diferentes de la misma mascota.
Ayuda a determinar el threshold óptimo.
"""
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
print("MEDICIÓN DE SIMILITUD ENTRE REPORTES")
print("=" * 70)

try:
    # Obtener los últimos reportes con embeddings
    reports = sb.table("reports").select("*").order("created_at", desc=True).limit(10).execute()
    
    if len(reports.data) < 2:
        print("\n❌ Necesitas al menos 2 reportes para comparar")
        sys.exit(1)
    
    print(f"\n📊 Reportes disponibles:")
    print("-" * 70)
    for i, r in enumerate(reports.data, 1):
        nombre = r.get('pet_name', 'Sin nombre')
        tipo = r.get('type', 'N/A')
        especie = r.get('species', 'N/A')
        created = r.get('created_at', 'N/A')[:19]
        tiene_emb = '✅' if r.get('embedding') else '❌'
        
        print(f"{i}. {nombre} ({tipo}) - {especie} - {created} {tiene_emb}")
    
    # Pedir al usuario que seleccione 2 reportes
    print("\n" + "=" * 70)
    print("Selecciona 2 reportes que sean fotos DIFERENTES de la MISMA mascota:")
    print("-" * 70)
    
    # Para automatizar, comparamos los dos últimos si ambos tienen embedding
    reportes_con_emb = [r for r in reports.data if r.get('embedding')]
    
    if len(reportes_con_emb) < 2:
        print("\n❌ Necesitas al menos 2 reportes con embeddings")
        sys.exit(1)
    
    r1 = reportes_con_emb[0]
    r2 = reportes_con_emb[1]
    
    print(f"\n🔍 Comparando:")
    print(f"   1️⃣ {r1.get('pet_name', 'Sin nombre')} ({r1.get('type')})")
    print(f"   2️⃣ {r2.get('pet_name', 'Sin nombre')} ({r2.get('type')})")
    
    emb1 = r1.get("embedding")
    emb2 = r2.get("embedding")
    
    # Parsear si son strings JSON
    if isinstance(emb1, str):
        emb1 = json.loads(emb1)
    if isinstance(emb2, str):
        emb2 = json.loads(emb2)
    
    print(f"\n✅ Embeddings cargados:")
    print(f"   Reporte 1: {len(emb1)} dimensiones")
    print(f"   Reporte 2: {len(emb2)} dimensiones")
    
    # Calcular similitud coseno
    vec1 = np.array(emb1, dtype=np.float32)
    vec2 = np.array(emb2, dtype=np.float32)
    
    # Normalizar vectores (por si acaso)
    vec1_norm = vec1 / np.linalg.norm(vec1)
    vec2_norm = vec2 / np.linalg.norm(vec2)
    
    similarity = float(np.dot(vec1_norm, vec2_norm))
    
    print("\n" + "=" * 70)
    print(f"🎯 SIMILITUD CALCULADA: {similarity:.6f} ({similarity:.2%})")
    print("=" * 70)
    
    # Interpretación
    print("\n📊 INTERPRETACIÓN:")
    if similarity >= 0.9:
        print(f"   🟢 MUY ALTA (≥90%): Probablemente la MISMA foto o muy similar")
    elif similarity >= 0.7:
        print(f"   🟡 ALTA (70-90%): Fotos similares, mismo ángulo/pose")
    elif similarity >= 0.6:
        print(f"   🟠 MEDIA (60-70%): Fotos diferentes de la misma mascota")
    elif similarity >= 0.5:
        print(f"   🟠 BAJA (50-60%): Posiblemente la misma mascota, ángulos muy diferentes")
    else:
        print(f"   🔴 MUY BAJA (<50%): Probablemente mascotas diferentes")
    
    print("\n💡 RECOMENDACIÓN:")
    if similarity >= 0.6:
        print(f"   ✅ Con threshold de 60%, estos reportes DEBERÍAN hacer match")
    else:
        print(f"   ❌ Con threshold de 60%, estos reportes NO harán match")
        print(f"   💡 Para que hagan match, necesitarías threshold de ~{similarity:.0%}")
        if similarity < 0.5:
            print(f"   ⚠️  ADVERTENCIA: Un threshold tan bajo puede causar muchos falsos positivos")
    
    # Comparar con todos los demás reportes
    print("\n" + "=" * 70)
    print("📊 SIMILITUD CON TODOS LOS REPORTES:")
    print("-" * 70)
    
    for r in reportes_con_emb:
        if r['id'] == r1['id']:
            continue
        
        emb = r.get("embedding")
        if isinstance(emb, str):
            emb = json.loads(emb)
        
        vec = np.array(emb, dtype=np.float32)
        vec_norm = vec / np.linalg.norm(vec)
        
        sim = float(np.dot(vec1_norm, vec_norm))
        
        nombre = r.get('pet_name', 'Sin nombre')
        tipo = r.get('type', 'N/A')
        
        match_icon = "✅" if sim >= 0.6 else "❌"
        print(f"   {match_icon} {nombre} ({tipo}): {sim:.2%}")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)


