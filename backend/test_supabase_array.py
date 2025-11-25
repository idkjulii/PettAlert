#!/usr/bin/env python3
"""Test simple para verificar cómo Supabase maneja arrays"""
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
print("TEST: CÓMO SUPABASE PYTHON MANEJA ARRAYS")
print("=" * 70)

# Obtener un reporte existente
try:
    reports = sb.table("reports").select("id").limit(1).execute()
    
    if not reports.data:
        print("\n❌ No hay reportes para probar")
        print("   Crea un reporte desde la app primero")
        sys.exit(1)
    
    report_id = reports.data[0]["id"]
    print(f"\n🔍 Usando reporte ID: {report_id[:16]}...")
    
    # Test 1: Array simple de Python
    print("\n" + "=" * 70)
    print("TEST 1: Enviar array de Python directamente")
    print("=" * 70)
    
    test_array = [0.1, 0.2, 0.3, 0.4, 0.5] * 307 + [0.1]  # 1536 valores
    print(f"Array Python: {type(test_array).__name__}, {len(test_array)} elementos")
    print(f"Primer elemento: {test_array[0]} (tipo: {type(test_array[0]).__name__})")
    
    result = sb.table('reports').update({
        'embedding': test_array
    }).eq('id', report_id).execute()
    
    print(f"✅ UPDATE completado, registros afectados: {len(result.data)}")
    
    # Verificar qué se guardó
    check = sb.table("reports").select("embedding").eq("id", report_id).execute()
    emb = check.data[0]["embedding"]
    
    print(f"\n📊 Lo que se guardó en la DB:")
    print(f"   Tipo en Python: {type(emb).__name__}")
    
    if isinstance(emb, str):
        print(f"   ❌ Se guardó como STRING (longitud: {len(emb)})")
        print(f"   Primeros 100 chars: {emb[:100]}")
        print(f"\n   🔍 Este es el PROBLEMA")
        print(f"   La librería postgrest-py está convirtiendo el array a string")
        
    elif isinstance(emb, list):
        print(f"   ✅ Se guardó como ARRAY (dimensiones: {len(emb)})")
        print(f"   Primeros 3 valores: {emb[:3]}")
        print(f"   Tipo del primer elemento: {type(emb[0]).__name__}")
        print(f"\n   ✅ ¡FUNCIONA! El problema está en otro lado")
    else:
        print(f"   ⚠️  Tipo desconocido: {type(emb).__name__}")
    
    # Test 2: Verificar la versión de las librerías
    print("\n" + "=" * 70)
    print("VERSIONES DE LIBRERÍAS")
    print("=" * 70)
    
    try:
        import supabase
        print(f"supabase: {supabase.__version__ if hasattr(supabase, '__version__') else 'desconocida'}")
    except:
        pass
    
    try:
        import postgrest
        print(f"postgrest: {postgrest.__version__ if hasattr(postgrest, '__version__') else 'desconocida'}")
    except:
        pass
    
    try:
        import httpx
        print(f"httpx: {httpx.__version__}")
    except:
        pass

except Exception as e:
    print(f"❌ Error: {e}")
    import traceback
    traceback.print_exc()

print("\n" + "=" * 70)




