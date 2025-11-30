# Optimizaciones de Embeddings - MegaDescriptor

## Problema Identificado

Después de 2-3 búsquedas consecutivas, el servidor experimentaba:
- **Memory leaks** - El modelo acumulaba tensors en memoria
- **GPU memory overflow** (si usa CUDA)
- **Timeout errors** - Requests bloqueando el event loop

## Soluciones Implementadas

### 1. ✅ Limpieza Explícita de Memoria

**Archivo**: `backend/services/embeddings.py`

```python
# Limpiar memoria explícitamente después de cada inferencia
del img, img_tensor, feats
if DEVICE == "cuda":
    torch.cuda.empty_cache()
```

**Beneficios**:
- Libera memoria GPU/CPU inmediatamente
- Previene acumulación de tensors
- Reduce fragmentación de memoria

### 2. ✅ Control de Concurrencia

**Implementación**:
```python
# Semáforo para limitar concurrencia (máximo 2 inferencias simultáneas)
_inference_semaphore = asyncio.Semaphore(2)

async def image_bytes_to_vec_async(image_bytes: bytes):
    async with _inference_semaphore:
        return await asyncio.to_thread(_generate_embedding, image_bytes)
```

**Beneficios**:
- Previene sobrecarga del modelo
- Máximo 2 inferencias simultáneas
- Requests adicionales esperan en cola

### 3. ✅ Ejecución Asíncrona No-Bloqueante

**Implementación**:
```python
# Ejecutar en thread pool para no bloquear el event loop
await asyncio.to_thread(_generate_embedding, image_bytes)
```

**Beneficios**:
- El event loop de FastAPI no se bloquea
- Otras requests pueden procesarse mientras se genera embedding
- Mejor performance general del servidor

### 4. ✅ torch.inference_mode()

**Implementación**:
```python
with torch.inference_mode():
    img_tensor = transforms(img).unsqueeze(0).to(DEVICE)
    feats = model(img_tensor)
```

**Beneficios**:
- Más eficiente que `torch.no_grad()`
- Deshabilita completamente el autograd
- Menor uso de memoria

## Resultados Esperados

### Antes:
- ❌ Crash después de 2-3 búsquedas
- ❌ Uso creciente de memoria RAM/GPU
- ❌ Timeouts en requests subsecuentes
- ❌ Servidor se congela

### Después:
- ✅ Búsquedas ilimitadas sin crashes
- ✅ Uso de memoria constante
- ✅ Responses rápidas y consistentes
- ✅ Servidor estable

## Uso

### Función Asíncrona (Recomendada para nuevos endpoints):
```python
from services.embeddings import image_bytes_to_vec_async

async def my_endpoint():
    vec = await image_bytes_to_vec_async(image_bytes)
```

### Función Síncrona (Compatibilidad con código existente):
```python
from services.embeddings import image_bytes_to_vec

def my_sync_function():
    vec = image_bytes_to_vec(image_bytes)
```

## Monitoreo

Para verificar que las optimizaciones funcionan:

```bash
# Ver uso de memoria del proceso Python
watch -n 1 'ps aux | grep python | grep uvicorn'

# Si usa CUDA, ver memoria GPU
watch -n 1 nvidia-smi
```

## Configuración Adicional

Si el problema persiste, ajustar el límite de concurrencia:

```python
# En backend/services/embeddings.py
_inference_semaphore = asyncio.Semaphore(1)  # Reducir a 1 para menos uso de memoria
```

## Testing

Probar múltiples búsquedas consecutivas:

```bash
for i in {1..10}; do
  echo "Búsqueda $i"
  curl -X POST "https://tu-tunel.trycloudflare.com/embeddings/search_image?top_k=10" \
    -F "file=@test.jpg"
  sleep 1
done
```

Todas las búsquedas deberían completarse exitosamente.





