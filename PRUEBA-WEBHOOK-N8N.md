# 🧪 Prueba de Integración con Webhook de n8n

Esta guía te muestra cómo probar que el backend envíe datos correctamente al webhook de n8n.

## 📋 Flujo Actualizado

```
1. Backend → Webhook de n8n (POST)
   Envía: {report_id, image_url, species, ...}
   
2. n8n procesa la imagen con Google Vision
   Analiza: labels, colors, species
   
3. n8n → Backend (POST /n8n/process-result)
   Envía: {report_id, labels, colors, species, ...}
   
4. Backend actualiza el reporte en Supabase
```

---

## ✅ Paso 1: Verificar Configuración

### 1.1: Verificar que el webhook está configurado

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/health" -Method GET
```

Deberías ver:
```json
{
  "status": "ok",
  "n8n_webhook": "https://n8n.arc-ctes.shop/webhook-test/9f0311e4-6678-4884-b9d1-af2276fe6aec",
  "n8n_status": "reachable",
  ...
}
```

### 1.2: Configurar variable de entorno (opcional)

Si quieres cambiar el webhook, agrega en `backend/.env`:

```env
N8N_WEBHOOK_URL=https://n8n.arc-ctes.shop/webhook-test/9f0311e4-6678-4884-b9d1-af2276fe6aec
```

---

## 🚀 Paso 2: Enviar un Reporte al Webhook

### Opción A: Enviar un reporte específico

```powershell
# Primero, obtén un report_id que tenga imágenes
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/reports/with-images?limit=1" -Method GET
$data = $response.Content | ConvertFrom-Json
$reportId = $data.reports[0].report_id

# Enviar al webhook
$body = @{
    report_id = $reportId
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/send-to-webhook" -Method POST `
    -Body $body `
    -ContentType "application/json"
```

**Resultado esperado:**
```json
{
  "success": true,
  "message": "Reporte ... enviado al webhook de n8n",
  "report_id": "...",
  "total_images": 1,
  "webhook_url": "https://n8n.arc-ctes.shop/webhook-test/...",
  "results": [...]
}
```

### Opción B: Procesar múltiples reportes (batch)

```powershell
$body = @{
    limit = 5
    has_labels = $false
} | ConvertTo-Json

Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/batch-process" -Method POST `
    -Body $body `
    -ContentType "application/json"
```

---

## 🔍 Paso 3: Verificar en n8n

1. Ve a tu workflow en n8n: `https://n8n.arc-ctes.shop`
2. Revisa los logs del workflow
3. Deberías ver que recibió los datos del backend

### Datos que n8n recibirá:

```json
{
  "report_id": "uuid-del-reporte",
  "image_url": "https://...",
  "image_index": 0,
  "total_images": 1,
  "species": "dog",
  "type": "lost",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z",
  "has_labels": false
}
```

---

## 📝 Paso 4: Configurar Workflow en n8n

Tu workflow en n8n debe:

### Nodo 1: Webhook (Trigger)
- Ya está configurado: `https://n8n.arc-ctes.shop/webhook-test/9f0311e4-6678-4884-b9d1-af2276fe6aec`
- Recibe: Datos del reporte desde el backend

### Nodo 2: HTTP Request - Descargar Imagen
- **Method**: `GET`
- **URL**: `{{ $json.image_url }}`
- **Response Format**: `File`

### Nodo 3: Google Cloud Vision
- Analiza la imagen descargada
- Extrae: labels, colors, species

### Nodo 4: Code - Formatear Datos
- Formatea los resultados para enviar al backend

### Nodo 5: HTTP Request - Enviar Resultados al Backend
- **Method**: `POST`
- **URL**: `http://TU_IP:8003/n8n/process-result`
  - ⚠️ **IMPORTANTE**: Cambia `TU_IP` por tu IP local (ej: `192.168.0.204`)
  - O usa ngrok si el backend está en un servidor remoto
- **Body**: `{{ $json }}`

---

## 🧪 Paso 5: Prueba Completa

### Script de prueba automática:

```powershell
# test-webhook-n8n.ps1
Write-Host "=== Prueba de Envío al Webhook de n8n ===" -ForegroundColor Cyan

$BACKEND_URL = "http://127.0.0.1:8003"

# 1. Obtener un reporte
Write-Host "`n1. Obteniendo reporte..." -ForegroundColor Yellow
$response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/reports/with-images?limit=1&has_labels=false" -Method GET
$data = $response.Content | ConvertFrom-Json

if ($data.count -eq 0) {
    Write-Host "   ⚠️ No hay reportes sin procesar" -ForegroundColor Yellow
    exit
}

$reportId = $data.reports[0].report_id
Write-Host "   ✅ Reporte encontrado: $reportId" -ForegroundColor Green

# 2. Enviar al webhook
Write-Host "`n2. Enviando al webhook de n8n..." -ForegroundColor Yellow
$body = @{
    report_id = $reportId
} | ConvertTo-Json

try {
    $response = Invoke-WebRequest -Uri "$BACKEND_URL/n8n/send-to-webhook" -Method POST `
        -Body $body `
        -ContentType "application/json"
    
    $result = $response.Content | ConvertFrom-Json
    Write-Host "   ✅ Enviado exitosamente!" -ForegroundColor Green
    Write-Host "   Webhook: $($result.webhook_url)" -ForegroundColor White
    Write-Host "   Imágenes enviadas: $($result.total_images)" -ForegroundColor White
} catch {
    Write-Host "   ❌ Error: $($_.Exception.Message)" -ForegroundColor Red
}

Write-Host "`n3. Verifica en n8n que recibió los datos" -ForegroundColor Yellow
Write-Host "   Ve a: https://n8n.arc-ctes.shop" -ForegroundColor White
Write-Host "   Revisa los logs del workflow" -ForegroundColor White
```

---

## ✅ Verificación Final

### En n8n:
1. ✅ Workflow activado
2. ✅ Recibe datos del webhook
3. ✅ Procesa imágenes correctamente
4. ✅ Envía resultados al backend

### En el Backend:
1. ✅ Recibe resultados de n8n
2. ✅ Actualiza reportes en Supabase

### En Supabase:
```sql
-- Ver reportes actualizados
SELECT id, labels, colors, species 
FROM reports 
WHERE labels IS NOT NULL 
ORDER BY created_at DESC;
```

---

## 🐛 Solución de Problemas

### "n8n no recibe los datos"

**Verifica:**
1. Que el workflow esté activado en n8n
2. Que la URL del webhook sea correcta
3. Que el backend pueda acceder a internet para enviar al webhook

### "n8n no puede llamar al backend"

**Solución:**
1. Usa ngrok para exponer tu backend públicamente
2. O configura n8n para que pueda acceder a tu red local
3. Actualiza la URL en el nodo HTTP Request del workflow

---

## 🎉 ¡Listo!

Si todo funciona, el flujo es:
1. Backend envía reportes → Webhook de n8n ✅
2. n8n procesa imágenes → Google Vision ✅
3. n8n envía resultados → Backend ✅
4. Backend actualiza → Supabase ✅











