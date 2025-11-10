# 🧪 Guía de Pruebas: Integración con n8n

Esta guía te llevará paso a paso para probar toda la integración con n8n.

## 📋 Índice

1. [Preparación](#preparación)
2. [Paso 1: Verificar Backend](#paso-1-verificar-backend)
3. [Paso 2: Probar Endpoints](#paso-2-probar-endpoints)
4. [Paso 3: Probar con un Reporte Real](#paso-3-probar-con-un-reporte-real)
5. [Paso 4: Configurar Workflow en n8n](#paso-4-configurar-workflow-en-n8n)
6. [Paso 5: Probar Workflow Completo](#paso-5-probar-workflow-completo)
7. [Verificación Final](#verificación-final)

---

## 🔧 Preparación

### 1. Asegúrate de que el backend esté corriendo

```powershell
# En una terminal, ve a la carpeta backend
cd backend

# Inicia el backend
python -m uvicorn main:app --reload --port 8003
```

Deberías ver algo como:
```
INFO:     Uvicorn running on http://127.0.0.1:8003
```

### 2. Verifica que tengas reportes con imágenes en Supabase

Si no tienes reportes, puedes crear uno desde la app móvil o directamente desde Supabase.

---

## ✅ Paso 1: Verificar Backend

### Test 1.1: Health Check General

Abre PowerShell y ejecuta:

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8003/health" -Method GET
```

**Resultado esperado:**
```json
{
  "status": "ok",
  "message": "PetAlert Vision API activa",
  "supabase": "conectado",
  "google_vision": "configurado"
}
```

### Test 1.2: Health Check de n8n

```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/health" -Method GET
```

**Resultado esperado:**
```json
{
  "status": "ok",
  "message": "Integración con n8n funcionando correctamente",
  "supabase": "conectado",
  "reports_with_images": 5,
  "total_active_reports": 10,
  "endpoints": {
    "get_reports": "/n8n/reports/with-images",
    "process_result": "/n8n/process-result",
    "health": "/n8n/health"
  }
}
```

**✅ Si ves esto, el backend está funcionando correctamente.**

---

## 🔍 Paso 2: Probar Endpoints

### Test 2.1: Obtener Reportes con Imágenes

```powershell
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/reports/with-images?limit=5" -Method GET
$data = $response.Content | ConvertFrom-Json
$data | ConvertTo-Json -Depth 10
```

**Resultado esperado:**
```json
{
  "reports": [
    {
      "report_id": "uuid-del-reporte",
      "image_url": "https://...",
      "image_index": 0,
      "total_images": 1,
      "species": "dog",
      "type": "lost",
      "status": "active",
      "created_at": "2024-01-01T00:00:00Z",
      "has_labels": false,
      "current_labels": null
    }
  ],
  "count": 5,
  "pagination": {
    "limit": 5,
    "offset": 0,
    "has_more": true
  }
}
```

**✅ Si ves reportes con URLs de imágenes, el endpoint funciona.**

### Test 2.2: Obtener Solo Reportes Sin Procesar

```powershell
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/reports/with-images?has_labels=false&limit=10" -Method GET
$data = $response.Content | ConvertFrom-Json
Write-Host "Reportes sin procesar: $($data.count)"
```

**✅ Esto te muestra cuántos reportes necesitan ser procesados.**

### Test 2.3: Usar el Script de Prueba Automático

Ejecuta el script que creamos:

```powershell
.\test-n8n-integration.ps1
```

Este script ejecuta todos los tests automáticamente y te muestra un resumen.

---

## 🎯 Paso 3: Probar con un Reporte Real

### Test 3.1: Simular Procesamiento Manual

Vamos a simular lo que n8n haría, paso a paso:

#### 3.1.1: Obtener un Reporte

```powershell
# Obtener un reporte con imagen
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/reports/with-images?limit=1" -Method GET
$data = $response.Content | ConvertFrom-Json
$report = $data.reports[0]

Write-Host "Report ID: $($report.report_id)"
Write-Host "Image URL: $($report.image_url)"
```

**Guarda estos valores para el siguiente paso.**

#### 3.1.2: Simular Análisis con Google Vision (Manual)

Para este paso, necesitarías tener acceso a Google Vision API. Si no lo tienes, puedes simular los datos:

```powershell
# Datos simulados (en producción, esto vendría de Google Vision)
$mockAnalysis = @{
    report_id = $report.report_id
    image_url = $report.image_url
    labels = @(
        @{ label = "Dog"; score = 95.5 },
        @{ label = "Pet"; score = 92.3 },
        @{ label = "Golden Retriever"; score = 88.7 }
    )
    colors = @("#FFD700", "#8B4513", "#FFFFFF")
    species = "dog"
    analysis_metadata = @{
        processed_at = (Get-Date).ToUniversalTime().ToString("o")
    }
} | ConvertTo-Json -Depth 10
```

#### 3.1.3: Enviar Resultados al Backend

```powershell
$body = $mockAnalysis
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/process-result" -Method POST -Body $body -ContentType "application/json"
$response.Content | ConvertFrom-Json
```

**Resultado esperado:**
```json
{
  "success": true,
  "message": "Reporte actualizado exitosamente",
  "report_id": "uuid-del-reporte",
  "updated_fields": ["labels", "colors", "species"]
}
```

#### 3.1.4: Verificar que se Actualizó en Supabase

Ve a Supabase y ejecuta:

```sql
SELECT id, labels, colors, species 
FROM reports 
WHERE id = 'TU_REPORT_ID_AQUI';
```

**✅ Deberías ver los labels y colores actualizados.**

---

## 🔄 Paso 4: Configurar Workflow en n8n

### 4.1: Acceder a n8n

1. Ve a: `https://n8n.arc-ctes.shop`
2. Inicia sesión
3. Crea un nuevo workflow

### 4.2: Configurar Nodos Básicos (Versión Simplificada para Prueba)

#### Nodo 1: Manual Trigger (para pruebas)
- Arrastra **"Manual Trigger"**
- Este nodo te permite ejecutar el workflow manualmente

#### Nodo 2: HTTP Request - Obtener Reportes
- Arrastra **"HTTP Request"**
- Conecta desde Manual Trigger
- Configura:
  ```
  Method: GET
  URL: http://TU_IP:8003/n8n/reports/with-images?limit=1
  Response Format: JSON
  ```
  ⚠️ **Cambia TU_IP** por tu IP local (ej: `192.168.0.204`)

#### Nodo 3: HTTP Request - Descargar Imagen
- Arrastra **"HTTP Request"**
- Conecta desde el nodo anterior
- Configura:
  ```
  Method: GET
  URL: {{ $json.reports[0].image_url }}
  Response Format: File
  ```

#### Nodo 4: Google Cloud Vision (o HTTP Request)
- Si tienes el nodo de Google Cloud Vision, úsalo
- Si no, usa HTTP Request para llamar a la API:
  ```
  Method: POST
  URL: https://vision.googleapis.com/v1/images:annotate?key=TU_API_KEY
  Body (JSON):
  {
    "requests": [{
      "image": {
        "content": "{{ $binary.data.toString('base64') }}"
      },
      "features": [
        {"type": "LABEL_DETECTION", "maxResults": 10},
        {"type": "IMAGE_PROPERTIES", "maxResults": 1}
      ]
    }]
  }
  ```

#### Nodo 5: Code - Formatear Datos
- Arrastra **"Code"**
- Pega el código de formateo (ver GUIA-INTEGRACION-N8N.md)

#### Nodo 6: HTTP Request - Enviar Resultados
- Arrastra **"HTTP Request"**
- Conecta desde Code
- Configura:
  ```
  Method: POST
  URL: http://TU_IP:8003/n8n/process-result
  Body: {{ $json }}
  Content Type: JSON
  ```

### 4.3: Guardar y Activar

1. **Guarda** el workflow (Ctrl+S)
2. **Activa** el workflow (toggle en la esquina superior derecha)

---

## 🚀 Paso 5: Probar Workflow Completo

### Test 5.1: Ejecutar Workflow Manualmente

1. En n8n, haz clic en **"Execute Workflow"** (o en el nodo Manual Trigger)
2. Monitorea cada paso en tiempo real
3. Verifica que cada nodo se complete exitosamente

### Test 5.2: Verificar Resultados

Después de ejecutar el workflow:

#### En Supabase:
```sql
SELECT id, labels, colors, species, created_at
FROM reports 
WHERE labels IS NOT NULL
ORDER BY created_at DESC
LIMIT 5;
```

#### En PowerShell:
```powershell
# Verificar que el reporte ahora tiene labels
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/reports/with-images?has_labels=true&limit=1" -Method GET
$data = $response.Content | ConvertFrom-Json
$data.reports[0].current_labels
```

---

## ✅ Verificación Final

### Checklist de Pruebas

- [ ] **Backend funcionando**: Health check responde OK
- [ ] **Endpoints accesibles**: Puedes obtener reportes con imágenes
- [ ] **Procesamiento manual**: Puedes enviar resultados y se actualizan
- [ ] **Workflow en n8n**: Se ejecuta sin errores
- [ ] **Resultados en BD**: Los reportes se actualizan correctamente
- [ ] **Labels guardados**: Se pueden ver en Supabase

### Test de Rendimiento (Opcional)

Prueba procesar múltiples reportes:

```powershell
# Obtener 10 reportes
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/reports/with-images?limit=10" -Method GET
$data = $response.Content | ConvertFrom-Json
Write-Host "Total de reportes a procesar: $($data.count)"
```

Luego ejecuta el workflow en n8n (asegúrate de aumentar el límite en el nodo HTTP Request).

---

## 🐛 Solución de Problemas Durante las Pruebas

### Problema: "Connection refused" al llamar al backend

**Solución:**
1. Verifica que el backend esté corriendo: `http://127.0.0.1:8003/health`
2. Usa tu IP local en lugar de `localhost` en n8n
3. Verifica que n8n pueda acceder a tu red local

### Problema: "No se encontraron reportes"

**Solución:**
1. Verifica que tengas reportes activos en Supabase
2. Verifica que los reportes tengan fotos (campo `photos` no vacío)
3. Revisa el filtro `status` en la query

### Problema: "Error al procesar resultado"

**Solución:**
1. Verifica que el `report_id` sea válido
2. Verifica el formato del JSON que envías
3. Revisa los logs del backend para ver el error específico

### Problema: "Google Vision API error"

**Solución:**
1. Verifica que la API key sea válida
2. Verifica que la cuenta tenga facturación habilitada
3. Verifica que Vision API esté habilitada en tu proyecto

---

## 📊 Monitoreo Continuo

Una vez que todo funcione, puedes monitorear el progreso:

```powershell
# Script de monitoreo
$response = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/health" -Method GET
$data = $response.Content | ConvertFrom-Json

Write-Host "📊 Estado de la Integración" -ForegroundColor Cyan
Write-Host "   Total reportes activos: $($data.total_active_reports)"
Write-Host "   Reportes con imágenes: $($data.reports_with_images)"

# Reportes sin procesar
$response2 = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/reports/with-images?has_labels=false" -Method GET
$data2 = $response2.Content | ConvertFrom-Json
Write-Host "   Reportes sin procesar: $($data2.count)" -ForegroundColor Yellow

# Reportes procesados
$response3 = Invoke-WebRequest -Uri "http://127.0.0.1:8003/n8n/reports/with-images?has_labels=true" -Method GET
$data3 = $response3.Content | ConvertFrom-Json
Write-Host "   Reportes procesados: $($data3.count)" -ForegroundColor Green
```

---

## 🎉 ¡Listo!

Si todos los tests pasan, tu integración con n8n está funcionando correctamente. Ahora puedes:

1. **Configurar Schedule Trigger** para procesar automáticamente
2. **Procesar todos los reportes existentes** ejecutando el workflow múltiples veces
3. **Monitorear el progreso** usando los scripts de verificación

¿Necesitas ayuda con algún paso específico?









