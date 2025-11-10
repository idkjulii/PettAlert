# 🔧 Solución de Problemas del Backend

## Problema: "No es posible conectar con el servidor remoto"

Este error en PowerShell significa que el backend no está corriendo o no está escuchando en el puerto 8003.

### ✅ Solución Paso a Paso

#### 1. Verificar que el Backend Esté Corriendo

Abre una **nueva terminal** y ejecuta:

```powershell
cd backend
python -m uvicorn main:app --reload --port 8003
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8003 (Press CTRL+C to quit)
INFO:     Started reloader process
INFO:     Started server process
INFO:     Application startup complete.
```

#### 2. Verificar que el Puerto Esté Libre

Si el puerto 8003 está ocupado, verás un error como:
```
ERROR:    [Errno 48] Address already in use
```

**Solución:**
```powershell
# Ver qué proceso usa el puerto 8003
netstat -ano | findstr :8003

# Matar el proceso (reemplaza PID con el número que aparece)
taskkill /PID <PID> /F
```

#### 3. Probar la Conexión

Una vez que el backend esté corriendo, en **otra terminal** prueba:

```powershell
# Opción 1: Usar Invoke-WebRequest (PowerShell nativo)
Invoke-WebRequest -Uri http://127.0.0.1:8003/health -Method GET

# Opción 2: Usar curl (si está instalado)
curl http://127.0.0.1:8003/health

# Opción 3: Abrir en el navegador
# Ve a: http://127.0.0.1:8003/health
```

#### 4. Verificar Endpoints del Backend

```powershell
# Estadísticas de RAG
Invoke-WebRequest -Uri http://127.0.0.1:8003/rag/stats -Method GET
```

---

## 🔍 Verificar que Todo Funcione

### Test Completo

Crea un archivo `test-backend.ps1`:

```powershell
# Test Backend
Write-Host "Testing Backend..." -ForegroundColor Green

# Test 1: Health
Write-Host "`n1. Testing /health..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri http://127.0.0.1:8003/health -Method GET
    Write-Host "✅ Health OK: $($response.StatusCode)" -ForegroundColor Green
    Write-Host $response.Content
} catch {
    Write-Host "❌ Health Failed: $_" -ForegroundColor Red
}

# Test 2: RAG Stats
Write-Host "`n2. Testing /rag/stats..." -ForegroundColor Yellow
try {
    $response = Invoke-WebRequest -Uri http://127.0.0.1:8003/rag/stats -Method GET
    Write-Host "✅ RAG Stats OK: $($response.StatusCode)" -ForegroundColor Green
    Write-Host $response.Content
} catch {
    Write-Host "❌ RAG Stats Failed: $_" -ForegroundColor Red
}

Write-Host "`n✅ Tests completed!" -ForegroundColor Green
```

Ejecuta:
```powershell
.\test-backend.ps1
```

---

## 🐛 Errores Comunes

### Error: "ModuleNotFoundError"

```powershell
# Instalar dependencias
cd backend
pip install -r requirements.txt
```

### Error: "SUPABASE_URL no encontrada"

Verifica que exista `backend/.env` con:
```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_KEY=tu_service_key
```

### Error: "Address already in use"

```powershell
# Encontrar y matar el proceso
netstat -ano | findstr :8003
taskkill /PID <PID> /F
```

### Error: "Import Error" en los routers

Verifica que los archivos existan:
- `backend/routers/rag_search.py`

---

## ✅ Verificación Final

### Checklist

- [ ] Backend corriendo en puerto 8003
- [ ] `/health` responde correctamente
- [ ] `/rag/stats` responde correctamente
- [ ] Variables de entorno configuradas
- [ ] Dependencias instaladas

---

## 🚀 Próximos Pasos

Una vez que el backend esté funcionando:

1. **Probar endpoints del backend**
2. **Procesar imágenes existentes**
3. **Implementar búsqueda RAG en frontend**

---

## 💡 Tip Pro

Si el backend sigue reiniciándose constantemente, puede ser por:
- Un error de sintaxis en algún archivo Python
- Una dependencia faltante
- Un problema con las variables de entorno

Revisa los logs del backend para ver el error específico.



