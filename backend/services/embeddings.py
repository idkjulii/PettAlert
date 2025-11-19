# backend/services/embeddings.py
import io
import asyncio
from typing import Optional
import numpy as np
from PIL import Image
import torch
import torchvision.transforms as T
import timm

# Configuración para MegaDescriptor
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "hf-hub:BVRA/MegaDescriptor-L-384"
EMBEDDING_DIM = None  # Se detectará automáticamente al cargar el modelo

_model = None
_transforms = None
_actual_dim = None

# Semáforo para limitar concurrencia (máximo 2 inferencias simultáneas)
_inference_semaphore = asyncio.Semaphore(2)

def _load_model():
    """Carga el modelo MegaDescriptor y sus transformaciones"""
    global _model, _transforms, _actual_dim
    if _model is None:
        print(f"🔄 Cargando MegaDescriptor en {DEVICE}...")
        # Cargar modelo desde Hugging Face Hub
        # num_classes=0 para obtener solo features (sin capa de clasificación)
        _model = timm.create_model(MODEL_NAME, pretrained=True, num_classes=0)
        _model = _model.to(DEVICE)
        _model.eval()
        
        # Verificar dimensión real del embedding
        with torch.no_grad():
            dummy_input = torch.randn(1, 3, 384, 384).to(DEVICE)
            dummy_output = _model(dummy_input)
            _actual_dim = dummy_output.shape[-1]
            print(f"📊 Dimensión del modelo: {_actual_dim}")
        
        # Transformaciones específicas para MegaDescriptor (384x384)
        _transforms = T.Compose([
            T.Resize(size=(384, 384)),
            T.ToTensor(),
            T.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
        ])
        print(f"✅ MegaDescriptor cargado exitosamente")
    return _model, _transforms, _actual_dim

async def image_bytes_to_vec_async(image_bytes: bytes) -> np.ndarray:
    """
    Genera embedding de forma asíncrona con control de concurrencia.
    
    Args:
        image_bytes: Bytes de la imagen
        
    Returns:
        numpy array float32 normalizado
    """
    async with _inference_semaphore:
        # Ejecutar en thread pool para no bloquear el event loop
        return await asyncio.to_thread(_generate_embedding, image_bytes)

def _generate_embedding(image_bytes: bytes) -> np.ndarray:
    """Genera el embedding (función interna)"""
    model, transforms, actual_dim = _load_model()
    
    # Cargar y convertir imagen
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    # Aplicar transformaciones y generar embedding
    with torch.inference_mode():
        img_tensor = transforms(img).unsqueeze(0).to(DEVICE)
        feats = model(img_tensor)
        
        # Normalización L2
        feats = feats / feats.norm(dim=-1, keepdim=True)
        
        # Convertir a numpy ANTES de liberar memoria
        vec = feats.squeeze(0).detach().cpu().numpy().astype("float32")
    
    # Limpiar memoria explícitamente
    del img, img_tensor, feats
    if DEVICE == "cuda":
        torch.cuda.empty_cache()
    
    print(f"🔍 Embedding generado: {vec.shape[-1]} dimensiones")
    
    return vec

def image_bytes_to_vec(image_bytes: bytes) -> np.ndarray:
    """
    Genera embedding L2-normalizado usando MegaDescriptor (versión síncrona).
    
    Args:
        image_bytes: Bytes de la imagen
        
    Returns:
        numpy array float32 normalizado (dimensión automática según el modelo)
    """
    # Versión síncrona simple para mantener compatibilidad con código existente
    return _generate_embedding(image_bytes)
