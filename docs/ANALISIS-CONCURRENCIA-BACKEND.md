# 🔄 Análisis de Concurrencia: Múltiples Usuarios Procesando Imágenes

## 📋 Escenario de Prueba

**Situación**: Varios usuarios (ej: 10-20) envían imágenes simultáneamente al backend para:
- Crear reportes con fotos
- Buscar coincidencias por imagen
- Generar embeddings

## ⚠️ Problemas Identificados

### 1. **Limitación de Concurrencia Parcial**

**Estado Actual**:
```python
# backend/services/embeddings.py
_inference_semaphore = asyncio.Semaphore(2)  # Máximo 2 inferencias simultáneas
```

**Problema**:
- ✅ El semáforo limita a **2 inferencias simultáneas** del modelo
- ❌ Pero **NO limita las requests HTTP** que llegan al servidor
- ❌ Los endpoints pueden recibir **muchas más requests** de las que pueden procesar

**Consecuencia**:
- Si 10 usuarios envían imágenes al mismo tiempo:
  - 2 se procesan inmediatamente
  - 8 esperan en cola (pueden tardar mucho)
  - Las requests pueden acumularse y causar timeouts

### 2. **Uso Inconsistente de Funciones Asíncronas**

**Problema Detectado**:

#### ✅ Endpoints que SÍ usan función asíncrona (respetan semáforo):
- Ninguno actualmente usa `image_bytes_to_vec_async`

#### ❌ Endpoints que NO usan función asíncrona (NO respetan semáforo):
```python
# backend/routers/embeddings_supabase.py
@router.post("/generate")
async def generate_embedding(file: UploadFile = File(...)):
    vec = image_bytes_to_vec(image_bytes)  # ❌ Función SÍNCRONA
    # No respeta el semáforo de concurrencia
```

```python
# backend/routers/embeddings_supabase.py
@router.post("/search_image")
async def search_image(...):
    qvec = image_bytes_to_vec(await file.read())  # ❌ Función SÍNCRONA
    # No respeta el semáforo de concurrencia
```

```python
# backend/routers/reports.py
async def generate_and_save_embedding(...):
    vec = image_bytes_to_vec(image_bytes)  # ❌ Función SÍNCRONA
    # No respeta el semáforo de concurrencia
```

**Consecuencia**:
- El semáforo **NO se está aplicando** en la mayoría de endpoints
- Múltiples inferencias pueden ejecutarse simultáneamente
- **Riesgo de sobrecarga de memoria GPU/CPU**
- **Riesgo de crashes** si hay muchas requests

### 3. **Procesamiento Síncrono en Creación de Reportes**

**Problema**:
```python
# backend/routers/reports.py
@router.post("/")
async def create_report(...):
    # ... crear reporte ...
    
    # ❌ Genera embedding de forma SÍNCRONA antes de retornar
    await generate_and_save_embedding(report_id, first_photo)
    
    return {"report": created_report}  # Usuario espera hasta que termine
```

**Consecuencia**:
- El usuario **espera** hasta que se genere el embedding (puede tardar 2-5 segundos)
- Si hay cola de requests, el tiempo de espera se multiplica
- **Mala experiencia de usuario** (tiempos de respuesta lentos)

### 4. **Falta de Rate Limiting**

**Problema**:
- ❌ No hay límite de requests por usuario/IP
- ❌ Un usuario puede enviar muchas imágenes rápidamente
- ❌ Riesgo de **abuso** o **ataques de denegación de servicio**

### 5. **Falta de Límite de Tamaño de Archivo**

**Problema**:
- ❌ No hay validación del tamaño máximo de imagen
- ❌ Un usuario puede enviar imágenes muy grandes (ej: 50MB)
- ❌ Puede causar:
  - **OOM (Out of Memory)** en el servidor
  - **Timeouts** al procesar
  - **Consumo excesivo de ancho de banda**

### 6. **Acumulación de Requests en Cola**

**Problema**:
- Si hay 20 usuarios enviando imágenes simultáneamente:
  - Solo 2 se procesan a la vez (si el semáforo funcionara)
  - 18 esperan en cola
  - Si cada procesamiento tarda 3 segundos:
    - Request #18 esperará: 18/2 * 3 = **27 segundos**
  - **Alto riesgo de timeout** (FastAPI default: 60s)

## 🔍 Comportamiento Actual con Múltiples Usuarios

### Escenario: 10 usuarios envían imágenes simultáneamente

```
Tiempo 0s:
  Usuario 1 → Request 1 (procesando)
  Usuario 2 → Request 2 (procesando)
  Usuario 3 → Request 3 (esperando)
  Usuario 4 → Request 4 (esperando)
  ...
  Usuario 10 → Request 10 (esperando)

Tiempo 3s:
  Request 1 ✅ Completado
  Request 2 ✅ Completado
  Request 3 → Inicia procesamiento
  Request 4 → Inicia procesamiento
  Request 5-10 → Siguen esperando

Tiempo 6s:
  Request 3 ✅ Completado
  Request 4 ✅ Completado
  Request 5 → Inicia procesamiento
  Request 6 → Inicia procesamiento
  ...

Tiempo 15s:
  Request 9 → Inicia procesamiento
  Request 10 → Inicia procesamiento

Tiempo 18s:
  Request 9 ✅ Completado
  Request 10 ✅ Completado
```

**Problema Real**: Como el semáforo NO se está usando correctamente, **TODAS las requests pueden procesarse simultáneamente**, causando:
- ❌ **Sobrecarga de memoria**
- ❌ **Crashes del servidor**
- ❌ **Timeouts**

## ✅ Soluciones Recomendadas

### 1. **Usar Función Asíncrona en Todos los Endpoints**

**Cambio necesario**:

```python
# backend/routers/embeddings_supabase.py

# ❌ ANTES
@router.post("/generate")
async def generate_embedding(file: UploadFile = File(...)):
    vec = image_bytes_to_vec(image_bytes)  # Síncrono

# ✅ DESPUÉS
@router.post("/generate")
async def generate_embedding(file: UploadFile = File(...)):
    vec = await image_bytes_to_vec_async(image_bytes)  # Asíncrono con semáforo
```

**Aplicar en**:
- `/embeddings/generate`
- `/embeddings/search_image`
- `/embeddings/index/{report_id}`
- `generate_and_save_embedding()` en `reports.py`

### 2. **Procesar Embeddings en Background Tasks**

**Cambio necesario**:

```python
# backend/routers/reports.py

# ❌ ANTES
@router.post("/")
async def create_report(...):
    # ... crear reporte ...
    await generate_and_save_embedding(report_id, first_photo)  # Bloquea respuesta
    return {"report": created_report}

# ✅ DESPUÉS
@router.post("/")
async def create_report(
    report_data: Dict[str, Any] = Body(...),
    background_tasks: BackgroundTasks
):
    # ... crear reporte ...
    
    # Procesar embedding en background (no bloquea respuesta)
    if photos:
        background_tasks.add_task(
            generate_and_save_embedding,
            report_id,
            first_photo
        )
    
    return {"report": created_report}  # Respuesta inmediata
```

**Beneficios**:
- ✅ Usuario recibe respuesta inmediata
- ✅ Embedding se genera en segundo plano
- ✅ Mejor experiencia de usuario

### 3. **Implementar Rate Limiting**

**Solución**: Usar `slowapi` o `fastapi-limiter`

```python
# backend/main.py
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# Aplicar en endpoints
@router.post("/embeddings/generate")
@limiter.limit("10/minute")  # Máximo 10 requests por minuto por IP
async def generate_embedding(...):
    ...
```

### 4. **Validar Tamaño de Archivo**

**Solución**:

```python
# backend/routers/embeddings_supabase.py

MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB

@router.post("/generate")
async def generate_embedding(file: UploadFile = File(...)):
    image_bytes = await file.read()
    
    # Validar tamaño
    if len(image_bytes) > MAX_IMAGE_SIZE:
        raise HTTPException(
            413,
            f"Imagen demasiado grande. Máximo: {MAX_IMAGE_SIZE / 1024 / 1024}MB"
        )
    
    vec = await image_bytes_to_vec_async(image_bytes)
    ...
```

### 5. **Aumentar Límite del Semáforo (Opcional)**

**Si el servidor tiene recursos suficientes**:

```python
# backend/services/embeddings.py

# Aumentar de 2 a 4 o más (depende de GPU/RAM disponible)
_inference_semaphore = asyncio.Semaphore(4)  # Más inferencias simultáneas
```

**Consideraciones**:
- ⚠️ Más memoria GPU/RAM necesaria
- ⚠️ Verificar que el servidor puede soportarlo
- ✅ Mejor throughput (más requests por segundo)

### 6. **Implementar Cola de Procesamiento (Solución Avanzada)**

**Para alta escala**, usar un sistema de colas (Redis + Celery):

```python
# Usar Celery para procesar embeddings en workers separados
from celery import Celery

celery_app = Celery('petalert', broker='redis://localhost:6379')

@celery_app.task
def generate_embedding_task(report_id: str, photo_url: str):
    # Procesar embedding en worker separado
    ...

# En el endpoint
@router.post("/")
async def create_report(...):
    # ... crear reporte ...
    if photos:
        generate_embedding_task.delay(report_id, first_photo)  # Enviar a cola
    return {"report": created_report}
```

**Beneficios**:
- ✅ Escalabilidad horizontal (múltiples workers)
- ✅ No bloquea el servidor principal
- ✅ Mejor manejo de picos de tráfico

## 📊 Comparación: Antes vs Después

### Antes (Estado Actual)
- ❌ Semáforo no se aplica correctamente
- ❌ Múltiples inferencias simultáneas sin control
- ❌ Usuario espera generación de embedding
- ❌ Sin rate limiting
- ❌ Sin validación de tamaño
- ⚠️ **Riesgo de crashes con múltiples usuarios**

### Después (Con Soluciones)
- ✅ Semáforo limita a 2-4 inferencias simultáneas
- ✅ Control de concurrencia efectivo
- ✅ Usuario recibe respuesta inmediata
- ✅ Rate limiting previene abuso
- ✅ Validación de tamaño previene OOM
- ✅ **Sistema estable con múltiples usuarios**

## 🧪 Prueba de Carga Recomendada

**Script de prueba**:

```bash
# Simular 10 usuarios enviando imágenes simultáneamente
for i in {1..10}; do
  curl -X POST "http://localhost:8003/embeddings/generate" \
    -F "file=@test_image.jpg" \
    -w "\nTiempo: %{time_total}s\n" &
done
wait
```

**Métricas a monitorear**:
- Tiempo de respuesta promedio
- Uso de memoria RAM/GPU
- Número de requests exitosas vs fallidas
- Errores de timeout

## 🎯 Prioridad de Implementación

1. **🔴 CRÍTICO**: Usar función asíncrona en todos los endpoints
2. **🟠 ALTO**: Procesar embeddings en background tasks
3. **🟡 MEDIO**: Validar tamaño de archivo
4. **🟢 BAJO**: Implementar rate limiting
5. **🔵 OPCIONAL**: Sistema de colas (si escala mucho)

---

**Conclusión**: El sistema actual **NO está preparado** para manejar múltiples usuarios simultáneos de forma segura. Se recomienda implementar las soluciones críticas antes de producción.


