# Solución: Error de Timeout de Conexión a Supabase (WinError 10060)

## 🔴 Problema

El backend experimentaba errores de timeout al intentar conectarse a Supabase, especialmente en entornos Windows:

```
httpx.ConnectTimeout: [WinError 10060] Se produjo un error durante el intento de conexión 
ya que la parte conectada no respondió adecuadamente tras un periodo de tiempo
```

### Síntomas:
- ❌ Errores HTTP 500 en endpoints que consultan la base de datos
- ❌ Timeouts en requests de direct-matches, matches, reports
- ❌ El frontend muestra errores al buscar coincidencias
- ❌ Cloudflared reporta errores de conexión al backend

## ✅ Solución Implementada

### 1. Módulo de Configuración Optimizada (`backend/utils/supabase_client.py`)

Se creó un módulo centralizado que configura el cliente de Supabase con:

- **Timeouts optimizados**:
  - Connect timeout: 10 segundos (tiempo para establecer conexión)
  - Read/Write timeout: 30 segundos (configurable)
  - Pool timeout: 5 segundos (obtener conexión del pool)

- **Retry logic**: 
  - Máximo 3 reintentos automáticos por defecto
  - Manejo inteligente de errores transitorios

- **Connection pooling**:
  - Máximo 100 conexiones simultáneas
  - 20 conexiones keep-alive
  - Expiración de keep-alive: 30 segundos

### 2. Actualización de Todos los Routers

Se actualizaron los siguientes routers para usar la configuración optimizada:

- ✅ `backend/routers/direct_matches.py`
- ✅ `backend/routers/matches.py`
- ✅ `backend/routers/reports.py`
- ✅ `backend/routers/ai_search.py`
- ✅ `backend/routers/fix_embeddings.py`
- ✅ `backend/routers/reports_labels.py`
- ✅ `backend/routers/rag_search.py`
- ✅ `backend/main.py`

### 3. Uso

#### Importación Simple:

```python
from utils.supabase_client import get_supabase_client

# Usar en cualquier router
def _sb() -> Client:
    """Crea un cliente de Supabase con configuración optimizada"""
    try:
        return get_supabase_client()
    except Exception as e:
        raise HTTPException(500, f"Error conectando a Supabase: {str(e)}")
```

#### Configuración Personalizada:

```python
from utils.supabase_client import create_supabase_client

# Cliente con timeout de 60 segundos y 5 reintentos
client = create_supabase_client(timeout=60.0, max_retries=5)
```

## 🔧 Configuración Opcional (`.env`)

Puedes configurar timeouts personalizados en el archivo `.env`:

```env
# Timeout en segundos para peticiones a Supabase (default: 30)
SUPABASE_TIMEOUT=30

# Número máximo de reintentos automáticos (default: 3)
SUPABASE_MAX_RETRIES=3
```

## 🚀 Cómo Reiniciar los Servicios

### 1. Detener Servicios Actuales

En PowerShell, presiona `Ctrl+C` en cada terminal para detener:
- Backend (uvicorn)
- Frontend (expo/metro)
- Cloudflared tunnel

### 2. Reiniciar Backend

```powershell
# Activar entorno virtual
& c:/Users/maria/OneDrive/Escritorio/lpm/petFindnoborres/.venv/Scripts/Activate.ps1

# Cambiar a directorio backend
cd backend

# Iniciar uvicorn
uvicorn main:app --reload --port 8003 --host 0.0.0.0
```

### 3. Reiniciar Cloudflared (en otra terminal)

```powershell
cloudflared tunnel --url http://localhost:8003
```

**Importante**: Actualiza el `EXPO_PUBLIC_BACKEND_URL` en el frontend con la nueva URL de cloudflared.

### 4. Reiniciar Frontend (en otra terminal)

```powershell
npm start
```

## 📊 Verificación

### 1. Verificar Health del Backend

```bash
curl http://localhost:8003/health
```

Deberías ver:
```json
{
  "status": "ok",
  "message": "PetAlert API activa",
  "supabase": "conectado"
}
```

### 2. Verificar Estado de Supabase

```bash
curl http://localhost:8003/supabase/status
```

Deberías ver:
```json
{
  "status": "conectado",
  "message": "Conexión exitosa con Supabase"
}
```

### 3. Probar Búsqueda de Matches

```bash
curl -X POST "http://localhost:8003/direct-matches/find/{REPORT_ID}?match_threshold=0.7&top_k=10"
```

## 🐛 Troubleshooting

### Error persiste después de la actualización

1. **Verificar que el entorno virtual está activado**:
   ```powershell
   # Deberías ver (.venv) en el prompt
   (.venv) PS C:\...\petFindnoborres>
   ```

2. **Verificar variables de entorno**:
   ```python
   import os
   print(os.getenv("SUPABASE_URL"))
   print(os.getenv("SUPABASE_SERVICE_KEY"))
   ```

3. **Verificar conectividad a Supabase**:
   ```powershell
   Test-NetConnection -ComputerName eamsbroadstwkrkjcuvo.supabase.co -Port 443
   ```

### Firewall o Antivirus bloqueando conexiones

Si tu firewall o antivirus está bloqueando:

1. Agregar excepción para Python:
   ```
   C:\Users\maria\OneDrive\Escritorio\lpm\petFindnoborres\.venv\Scripts\python.exe
   ```

2. Agregar excepción para el puerto 8003

3. Temporalmente desactivar firewall y probar

### Aumentar Timeouts

Si la conexión es muy lenta, aumenta los timeouts en `utils/supabase_client.py`:

```python
timeout_config = httpx.Timeout(
    connect=30.0,   # Aumentar de 10 a 30
    read=60.0,      # Aumentar de 30 a 60
    write=60.0,     # Aumentar de 30 a 60
    pool=10.0       # Aumentar de 5 a 10
)
```

## 📝 Notas Técnicas

### Por qué ocurría el error

1. **Cliente httpx sin configuración**: El cliente de Supabase Python usa httpx internamente, pero sin configuración explícita de timeouts
2. **Windows y redes lentas**: Windows es más estricto con timeouts de red
3. **Firewall corporativo**: Algunos firewalls introducen latencia adicional
4. **OneDrive sincronización**: OneDrive puede interferir con conexiones de red

### Mejoras implementadas

1. **Timeouts explícitos**: Todos los timeouts configurados explícitamente
2. **Retry logic**: Reintentos automáticos para errores transitorios
3. **Connection pooling**: Reutilización eficiente de conexiones
4. **Mejor manejo de errores**: Mensajes más descriptivos

## ✅ Checklist de Verificación

- [x] Módulo `utils/supabase_client.py` creado
- [x] Todos los routers actualizados
- [x] `main.py` actualizado
- [x] `env.example` actualizado con nuevas opciones
- [x] Documentación creada

## 🆘 Soporte Adicional

Si el error persiste:

1. Verificar logs del backend para ver el error exacto
2. Verificar que Supabase está accesible desde el navegador
3. Probar con otra red (ej: hotspot móvil) para descartar problemas de red local
4. Contactar al administrador de red si estás en una red corporativa

## 🎯 Resultado Esperado

Después de implementar esta solución:

✅ Conexiones estables a Supabase
✅ Sin errores de timeout en operaciones normales
✅ Mejor rendimiento general del backend
✅ Reintentos automáticos en caso de errores transitorios




