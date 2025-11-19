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
print("VERIFICAR MATCHES GUARDADOS EN LA BASE DE DATOS")
print("=" * 70)

try:
    # Obtener todos los matches
    matches = sb.table("matches").select("*").execute()
    
    print(f"\n📊 Total matches en la base de datos: {len(matches.data)}")
    
    if matches.data:
        print("\n✅ Matches encontrados:\n")
        for i, m in enumerate(matches.data, 1):
            print(f"{i}. Match ID: {m.get('id', 'N/A')[:16]}...")
            print(f"   Lost Report:  {m.get('lost_report_id', 'N/A')[:16]}...")
            print(f"   Found Report: {m.get('found_report_id', 'N/A')[:16]}...")
            print(f"   Similitud: {m.get('similarity_score', 0):.2%}")
            print(f"   Estado: {m.get('status', 'N/A')}")
            print(f"   Matched by: {m.get('matched_by', 'N/A')}")
            print(f"   Creado: {m.get('created_at', 'N/A')[:19]}")
            print()
    else:
        print("\n❌ NO HAY MATCHES GUARDADOS")
        print("\n🔍 Posibles causas:")
        print("   1. La función de guardar matches falló silenciosamente")
        print("   2. Hay un error en la lógica de guardado")
        print("   3. Los reportes no se están comparando")
        
        # Verificar reportes
        print("\n📊 Verificando reportes...")
        reports = sb.table("reports").select("id, pet_name, type, embedding").order("created_at", desc=True).limit(5).execute()
        
        lost = [r for r in reports.data if r.get("type") == "lost" and r.get("embedding")]
        found = [r for r in reports.data if r.get("type") == "found" and r.get("embedding")]
        
        print(f"\n   Reportes LOST con embedding: {len(lost)}")
        print(f"   Reportes FOUND con embedding: {len(found)}")
        
        if len(lost) > 0 and len(found) > 0:
            print(f"\n   ✅ HAY reportes para comparar")
            print(f"   ❌ Pero NO se crearon matches")
            print(f"\n   💡 El problema está en la función de guardar matches")

except Exception as e:
    print(f"\n❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)


