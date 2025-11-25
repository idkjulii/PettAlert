#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
from pathlib import Path
from dotenv import load_dotenv
import numpy as np
from datetime import datetime, timedelta

load_dotenv(Path(__file__).parent / ".env")
from supabase import create_client

sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

print("=" * 70)
print("VERIFICACIÓN COMPLETA - EMBEDDINGS Y MATCHES")
print("=" * 70)

# Obtener reportes recientes (últimas 2 horas)
try:
    reports = sb.table("reports").select("*").order("created_at", desc=True).limit(5).execute()
    
    print(f"\n📊 Últimos {len(reports.data)} reportes:\n")
    
    for r in reports.data:
        nombre = r.get("pet_name", "Sin nombre")
        tipo = r.get("type", "N/A")
        emb = r.get("embedding")
        created = r.get("created_at", "N/A")
        
        emb_status = "❌ Sin embedding"
        if emb:
            if isinstance(emb, str):
                emb_status = f"❌ STRING ({len(emb)} chars)"
            elif isinstance(emb, list):
                emb_status = f"✅ ARRAY ({len(emb)} dims)"
        
        print(f"   {nombre} ({tipo}) - {emb_status}")
        print(f"      Creado: {created}")
        print(f"      ID: {r['id'][:16]}...")
        print()
    
    # Obtener los dos últimos reportes (deberían ser el lost y found)
    if len(reports.data) >= 2:
        r1 = reports.data[0]
        r2 = reports.data[1]
        
        # Verificar si son tipos opuestos
        if r1.get("type") != r2.get("type"):
            print("=" * 70)
            print("COMPARANDO LOS DOS ÚLTIMOS REPORTES")
            print("=" * 70)
            
            emb1 = r1.get("embedding")
            emb2 = r2.get("embedding")
            
            if emb1 and emb2 and isinstance(emb1, list) and isinstance(emb2, list):
                vec1 = np.array(emb1, dtype=np.float32)
                vec2 = np.array(emb2, dtype=np.float32)
                
                similarity = float(np.dot(vec1, vec2))
                
                print(f"\n🔍 Similitud calculada: {similarity:.6f} ({similarity:.2%})")
                
                if similarity >= 0.7:
                    print(f"   ✅ MATCH! (>= 70%)")
                else:
                    print(f"   ❌ No match (< 70%)")
                
                # Verificar si hay match en la DB
                print(f"\n📊 Buscando en tabla 'matches'...")
                
                matches = sb.table("matches").select("*").execute()
                
                if matches.data:
                    print(f"   ✅ Hay {len(matches.data)} matches guardados:")
                    for m in matches.data:
                        print(f"      - Similitud: {m.get('similarity_score', 'N/A')}")
                        print(f"        Lost: {m.get('lost_report_id', 'N/A')[:16]}...")
                        print(f"        Found: {m.get('found_report_id', 'N/A')[:16]}...")
                        print(f"        Estado: {m.get('status', 'N/A')}")
                else:
                    print(f"   ❌ NO hay matches guardados en la base de datos")
                    print(f"\n   💡 Esto significa que find_and_save_matches() no se ejecutó")
                    print(f"      Revisa los logs del backend cuando creaste los reportes")
            else:
                print(f"\n❌ Los embeddings no son arrays válidos")
                print(f"   Reporte 1: {type(emb1).__name__}")
                print(f"   Reporte 2: {type(emb2).__name__}")
        else:
            print(f"\n⚠️ Los dos últimos reportes son del mismo tipo ({r1.get('type')})")
            print(f"   No se pueden comparar")
    
except Exception as e:
    print(f"❌ Error: {e}")

print("\n" + "=" * 70)




