#!/usr/bin/env python3
import sys
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import os
from pathlib import Path
from dotenv import load_dotenv
import httpx
import asyncio

load_dotenv(Path(__file__).parent / ".env")
from supabase import create_client

sb = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_SERVICE_KEY"))

async def buscar_matches():
    print("=" * 70)
    print("BUSCANDO MATCHES PARA REPORTES PERDIDOS")
    print("=" * 70)
    
    # Obtener reportes perdidos
    reports = sb.table("reports").select("id, pet_name, type, species").eq("type", "lost").execute()
    
    if not reports.data:
        print("\nℹ️  No hay reportes perdidos para buscar matches")
        return
    
    print(f"\n🔍 Buscando matches para {len(reports.data)} reportes perdidos...\n")
    
    total_matches = 0
    
    for r in reports.data:
        report_id = r["id"]
        nombre = r.get("pet_name", "Sin nombre")
        especie = r.get("species", "N/A")
        
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                resp = await client.get(f"http://localhost:8003/direct-matches/find/{report_id}")
                
                if resp.status_code == 200:
                    data = resp.json()
                    matches = data.get("matches", [])
                    
                    if matches:
                        print(f"✅ {nombre} ({especie}): {len(matches)} matches")
                        for i, m in enumerate(matches[:3], 1):
                            sim = m.get("similarity", 0)
                            matched_id = m.get("report_id", "N/A")
                            print(f"   {i}. Similitud: {sim:.2%} (ID: {matched_id[:8]}...)")
                        total_matches += len(matches)
                    else:
                        print(f"ℹ️  {nombre} ({especie}): Sin matches (similitud < 70%)")
                else:
                    print(f"❌ {nombre}: Error HTTP {resp.status_code}")
                    
        except Exception as e:
            print(f"❌ {nombre}: Error - {e}")
    
    print(f"\n" + "=" * 70)
    print(f"📊 Total matches encontrados: {total_matches}")
    print("=" * 70)
    
    if total_matches > 0:
        print("\n💡 Los matches se guardaron en la tabla 'matches'")
        print("   Puedes verlos desde la app o consultando:")
        print("   GET /matches/pending?user_id={tu_user_id}")

if __name__ == "__main__":
    asyncio.run(buscar_matches())


