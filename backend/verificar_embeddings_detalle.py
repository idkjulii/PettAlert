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
print("VERIFICAR TIPO DE EMBEDDINGS EN BASE DE DATOS")
print("=" * 70)

reports = sb.table("reports").select("id, pet_name, type, embedding").execute()

for r in reports.data:
    nombre = r.get("pet_name", "Sin nombre")
    tipo = r.get("type", "N/A")
    emb = r.get("embedding")
    
    if emb:
        tipo_emb = type(emb).__name__
        
        if isinstance(emb, str):
            print(f"\n❌ {nombre} ({tipo}):")
            print(f"   Tipo: STRING (longitud: {len(emb)} caracteres)")
            print(f"   Primeros 100 chars: {emb[:100]}")
        elif isinstance(emb, list):
            print(f"\n✅ {nombre} ({tipo}):")
            print(f"   Tipo: ARRAY (dimensiones: {len(emb)})")
            print(f"   Primeros 3 valores: {emb[:3]}")
        else:
            print(f"\n⚠️ {nombre} ({tipo}):")
            print(f"   Tipo: {tipo_emb}")
    else:
        print(f"\n❌ {nombre} ({tipo}): Sin embedding")

print("\n" + "=" * 70)


