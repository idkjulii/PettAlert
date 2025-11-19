#!/usr/bin/env python3
"""
Script de diagnóstico para verificar la configuración de embeddings
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# Configurar encoding para Windows
if sys.platform == 'win32':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Cargar variables de entorno
ENV_PATH = Path(__file__).resolve().parent / ".env"
print(f"📁 Cargando .env desde: {ENV_PATH}")
print(f"   ¿Existe? {ENV_PATH.exists()}")

load_dotenv(dotenv_path=ENV_PATH, override=False)

print("\n" + "=" * 70)
print("DIAGNÓSTICO DE CONFIGURACIÓN")
print("=" * 70)

# Verificar variables de entorno
generate_locally_raw = os.getenv("GENERATE_EMBEDDINGS_LOCALLY")
auto_send_n8n_raw = os.getenv("AUTO_SEND_REPORTS_TO_N8N")

print(f"\n📊 Valores RAW del .env:")
print(f"   GENERATE_EMBEDDINGS_LOCALLY = '{generate_locally_raw}'")
print(f"   AUTO_SEND_REPORTS_TO_N8N = '{auto_send_n8n_raw}'")

# Simular la lógica del código
GENERATE_EMBEDDINGS_LOCALLY = (
    os.getenv("GENERATE_EMBEDDINGS_LOCALLY", "false").lower() in ("1", "true", "yes")
)
AUTO_SEND_REPORTS_TO_N8N = (
    os.getenv("AUTO_SEND_REPORTS_TO_N8N", "true").lower() in ("1", "true", "yes")
)

print(f"\n🔧 Valores PROCESADOS (después de la lógica):")
print(f"   GENERATE_EMBEDDINGS_LOCALLY = {GENERATE_EMBEDDINGS_LOCALLY}")
print(f"   AUTO_SEND_REPORTS_TO_N8N = {AUTO_SEND_REPORTS_TO_N8N}")

print(f"\n📝 Interpretación:")
if GENERATE_EMBEDDINGS_LOCALLY:
    print("   ✅ Los embeddings SÍ se generarán localmente")
else:
    print("   ❌ Los embeddings NO se generarán localmente")
    print("   💡 Solución: Asegúrate que .env tenga:")
    print("      GENERATE_EMBEDDINGS_LOCALLY=true")

if AUTO_SEND_REPORTS_TO_N8N:
    print("   ⚠️  Los reportes SÍ se enviarán a N8N (redundante)")
else:
    print("   ✅ Los reportes NO se enviarán a N8N")

print("\n" + "=" * 70)

# Verificar que las dependencias estén disponibles
print("\n🔍 Verificando dependencias...")
try:
    import torch
    import timm
    from PIL import Image
    print("   ✅ torch, timm, PIL disponibles")
    print(f"   📊 torch version: {torch.__version__}")
    print(f"   📊 CUDA disponible: {torch.cuda.is_available()}")
except ImportError as e:
    print(f"   ❌ Error importando dependencias: {e}")

print("\n" + "=" * 70)

