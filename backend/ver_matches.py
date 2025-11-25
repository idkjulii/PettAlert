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

# Ver reportes por tipo
reports = sb.table("reports").select("id, pet_name, type, species").execute()

lost = [r for r in reports.data if r.get("type") == "lost"]
found = [r for r in reports.data if r.get("type") == "found"]

print("=" * 70)
print("ESTADO DE REPORTES PARA MATCHES")
print("=" * 70)
print(f"\n🔴 Reportes PERDIDOS (lost): {len(lost)}")
for r in lost[:5]:
    print(f"   - {r.get('pet_name', 'Sin nombre')} ({r.get('species', 'N/A')})")

print(f"\n🟢 Reportes ENCONTRADOS (found): {len(found)}")
for r in found[:5]:
    print(f"   - {r.get('pet_name', 'Sin nombre')} ({r.get('species', 'N/A')})")

# Ver matches existentes
matches = sb.table("matches").select("*").execute()

print(f"\n🔗 Matches encontrados: {len(matches.data)}")
if matches.data:
    for m in matches.data[:5]:
        print(f"   - Similitud: {m.get('similarity_score', 0):.2f}")
        print(f"     Lost ID: {m.get('lost_report_id')}")
        print(f"     Found ID: {m.get('found_report_id')}")
        print(f"     Estado: {m.get('status', 'N/A')}")
        print()
else:
    print("   ℹ️  No hay matches todavía")
    if len(lost) > 0 and len(found) == 0:
        print("\n💡 Necesitas crear reportes tipo 'found' (encontrados)")
        print("   para que haya matches con los reportes 'lost'")
    elif len(found) > 0 and len(lost) == 0:
        print("\n💡 Necesitas crear reportes tipo 'lost' (perdidos)")
        print("   para que haya matches con los reportes 'found'")

print("\n" + "=" * 70)




