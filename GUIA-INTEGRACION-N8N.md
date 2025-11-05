# 🚀 Guía Completa: Integración de n8n para Procesamiento de Imágenes

Esta guía te explica cómo configurar n8n para procesar automáticamente todas las imágenes de los reportes en tu base de datos usando Google Vision API.

## 📋 Tabla de Contenidos

1. [Visión General](#visión-general)
2. [Requisitos Previos](#requisitos-previos)
3. [Configuración del Backend](#configuración-del-backend)
4. [Configuración del Workflow en n8n](#configuración-del-workflow-en-n8n)
5. [Pruebas y Verificación](#pruebas-y-verificación)
6. [Solución de Problemas](#solución-de-problemas)

---

## 🎯 Visión General

### ¿Qué hace esta integración?

1. **n8n obtiene reportes con imágenes** desde tu backend
2. **Procesa cada imagen** con Google Vision API para detectar:
   - Etiquetas (labels): "dog", "pet", "golden retriever", etc.
   - Colores dominantes: "#FFD700", "#8B4513", etc.
   - Especie: "dog", "cat", "bird", etc.
3. **Actualiza la base de datos** con los resultados del análisis

### Flujo del Sistema

```
┌─────────────────────────────────────────────────────────┐
│ 1. n8n solicita reportes con imágenes                  │
│    GET /n8n/reports/with-images                        │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│ 2. Backend retorna lista de reportes con URLs de imágenes│
│    [{report_id, image_url, species, ...}, ...]         │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│ 3. n8n procesa cada imagen con Google Vision           │
│    - Descarga imagen desde URL                         │
│    - Analiza con Google Vision API                     │
│    - Extrae labels, colores, especie                   │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│ 4. n8n envía resultados al backend                     │
│    POST /n8n/process-result                            │
│    {report_id, labels, colors, species, ...}           │
└───────────────┬─────────────────────────────────────────┘
                │
                ▼
┌─────────────────────────────────────────────────────────┐
│ 5. Backend actualiza el reporte en Supabase            │
│    - Guarda labels en columna labels                   │
│    - Guarda colores en columna colors                  │
│    - Actualiza especie si no estaba definida           │
└─────────────────────────────────────────────────────────┘
```

---

## 📋 Requisitos Previos

### 1. Backend funcionando
- ✅ Backend corriendo en `http://localhost:8003` (o tu URL)
- ✅ Variables de entorno configuradas en `backend/.env`

### 2. Cuenta de n8n
- ✅ Acceso a n8n: `https://n8n.arc-ctes.shop`
- ✅ Webhook configurado: `https://n8n.arc-ctes.shop/webhook-test/9f0311e4-6678-4884-b9d1-af2276fe6aec`

### 3. Google Cloud Vision API
- ✅ API Key de Google Vision configurada
- ✅ Cuenta de Google Cloud con Vision API habilitada

---

## ⚙️ Configuración del Backend

### 1. Verificar que el router esté incluido

El router de n8n ya está incluido en `backend/main.py`. Verifica que esté presente:

```python
from routers import n8n_integration as n8n_router
# ...
app.include_router(n8n_router.router)
```

### 2. Verificar endpoints

Reinicia el backend y verifica que los endpoints funcionen:

```powershell
# Verificar salud del endpoint
Invoke-WebRequest -Uri "http://localhost:8003/n8n/health" -Method GET

# Obtener reportes con imágenes
Invoke-WebRequest -Uri "http://localhost:8003/n8n/reports/with-images?limit=10" -Method GET
```

### 3. Endpoints disponibles

| Endpoint | Método | Descripción |
|----------|--------|-------------|
| `/n8n/health` | GET | Verifica el estado de la integración |
| `/n8n/reports/with-images` | GET | Obtiene reportes con imágenes para procesar |
| `/n8n/process-result` | POST | Recibe resultados del análisis de n8n |
| `/n8n/batch-process` | POST | Inicia procesamiento batch (opcional) |

---

## 🔧 Configuración del Workflow en n8n

### Paso 1: Crear nuevo workflow

1. Ve a `https://n8n.arc-ctes.shop`
2. Haz clic en **"New Workflow"**
3. Nombra el workflow: **"Procesar Imágenes de Reportes"**

### Paso 2: Configurar Nodo 1 - Webhook (Trigger)

1. Arrastra el nodo **"Webhook"** al canvas
2. Configura:
   - **HTTP Method**: `GET`
   - **Path**: `process-reports` (o el que prefieras)
   - **Response Mode**: `Using 'Respond to Webhook' Node`
3. **Activa el workflow** (toggle en la esquina superior derecha)
4. Copia la URL del webhook (aparecerá en el nodo)

**Nota**: Este webhook se puede usar para activar el procesamiento manualmente. También puedes usar un **Schedule Trigger** para ejecutarlo automáticamente.

### Paso 3: Configurar Nodo 2 - HTTP Request (Obtener Reportes)

1. Arrastra el nodo **"HTTP Request"**
2. Conecta desde el nodo Webhook
3. Configura:
   - **Method**: `GET`
   - **URL**: `http://TU_IP_LOCAL:8003/n8n/reports/with-images?limit=10`
     - ⚠️ **IMPORTANTE**: Cambia `TU_IP_LOCAL` por tu IP local (ej: `192.168.0.204`)
     - O usa ngrok si el backend está en un servidor remoto
   - **Authentication**: None (si el backend no requiere auth)
   - **Response Format**: `JSON`

### Paso 4: Configurar Nodo 3 - Split In Batches (Procesar en lotes)

1. Arrastra el nodo **"Split In Batches"**
2. Conecta desde el nodo HTTP Request
3. Configura:
   - **Batch Size**: `5` (procesa 5 imágenes a la vez)
   - **Field to Split Out**: `reports` (el campo que contiene el array de reportes)

### Paso 5: Configurar Nodo 4 - HTTP Request (Descargar Imagen)

1. Arrastra el nodo **"HTTP Request"**
2. Conecta desde el nodo Split In Batches
3. Configura:
   - **Method**: `GET`
   - **URL**: `{{ $json.image_url }}`
   - **Options → Response Format**: `File`

### Paso 6: Configurar Nodo 5 - Google Cloud Vision (Análisis)

1. Arrastra el nodo **"Google Cloud Vision"**
2. Conecta desde el nodo HTTP Request
3. Configura:
   - **Operation**: `Label Detection`
   - **Authentication**: Usa tus credenciales de Google Cloud
   - **Image**: `{{ $binary.data }}`

**Nota**: Si no tienes el nodo de Google Cloud Vision, puedes usar **HTTP Request** para llamar a la API directamente:

```javascript
// URL: https://vision.googleapis.com/v1/images:annotate?key=TU_API_KEY
// Method: POST
// Body:
{
  "requests": [{
    "image": {
      "content": "{{ $binary.data.toString('base64') }}"
    },
    "features": [
      {
        "type": "LABEL_DETECTION",
        "maxResults": 10
      },
      {
        "type": "IMAGE_PROPERTIES",
        "maxResults": 1
      }
    ]
  }]
}
```

### Paso 7: Configurar Nodo 6 - Code (Formatear Datos)

1. Arrastra el nodo **"Code"**
2. Conecta desde el nodo Google Cloud Vision
3. Configura el código JavaScript:

```javascript
// Obtener datos del reporte original (del paso 2)
const reportData = $('Split In Batches').json;
const visionResponse = $json;

// Extraer labels
const labels = visionResponse.responses[0].labelAnnotations.map(label => ({
  label: label.description,
  score: Math.round(label.score * 100 * 100) / 100
}));

// Extraer colores dominantes
let colors = [];
if (visionResponse.responses[0].imagePropertiesAnnotation) {
  const dominantColors = visionResponse.responses[0].imagePropertiesAnnotation.dominantColors.colors;
  colors = dominantColors.slice(0, 3).map(color => {
    const r = Math.round(color.color.red);
    const g = Math.round(color.color.green);
    const b = Math.round(color.color.blue);
    return `#${r.toString(16).padStart(2, '0')}${g.toString(16).padStart(2, '0')}${b.toString(16).padStart(2, '0')}`;
  });
}

// Determinar especie
let species = null;
for (const label of labels) {
  const labelText = label.label.toLowerCase();
  if (labelText.includes('dog') || labelText.includes('perro')) {
    species = 'dog';
    break;
  } else if (labelText.includes('cat') || labelText.includes('gato')) {
    species = 'cat';
    break;
  } else if (labelText.includes('bird') || labelText.includes('pájaro') || labelText.includes('ave')) {
    species = 'bird';
    break;
  } else if (labelText.includes('rabbit') || labelText.includes('conejo')) {
    species = 'rabbit';
    break;
  }
}

if (!species) {
  species = 'other';
}

// Preparar payload para enviar al backend
return {
  json: {
    report_id: reportData.report_id,
    image_url: reportData.image_url,
    labels: labels,
    colors: colors,
    species: species,
    analysis_metadata: {
      processed_at: new Date().toISOString(),
      image_index: reportData.image_index,
      total_images: reportData.total_images
    }
  }
};
```

### Paso 8: Configurar Nodo 7 - HTTP Request (Enviar Resultados)

1. Arrastra el nodo **"HTTP Request"**
2. Conecta desde el nodo Code
3. Configura:
   - **Method**: `POST`
   - **URL**: `http://TU_IP_LOCAL:8003/n8n/process-result`
     - ⚠️ **IMPORTANTE**: Cambia `TU_IP_LOCAL` por tu IP local
   - **Authentication**: None
   - **Body Content Type**: `JSON`
   - **Body**: `{{ $json }}`

### Paso 9: Configurar Nodo 8 - Respond to Webhook (Opcional)

Si usaste un webhook GET para activar el workflow:

1. Arrastra el nodo **"Respond to Webhook"**
2. Conecta desde el nodo HTTP Request (o desde Split In Batches si quieres responder antes)
3. Configura:
   - **Response Code**: `200`
   - **Response Body**: `{{ { "success": true, "processed": $json.report_id } }}`

### Paso 10: Activar y Guardar

1. **Guarda el workflow** (Ctrl+S o Cmd+S)
2. **Activa el workflow** (toggle en la esquina superior derecha)
3. El workflow está listo para procesar imágenes

---

## 🧪 Pruebas y Verificación

### 1. Probar el endpoint de salud

```powershell
Invoke-WebRequest -Uri "http://localhost:8003/n8n/health" -Method GET
```

Deberías ver:
```json
{
  "status": "ok",
  "message": "Integración con n8n funcionando correctamente",
  "supabase": "conectado",
  "reports_with_images": 15,
  "total_active_reports": 20
}
```

### 2. Obtener reportes con imágenes

```powershell
Invoke-WebRequest -Uri "http://localhost:8003/n8n/reports/with-images?limit=5" -Method GET
```

Deberías ver una lista de reportes con sus URLs de imágenes.

### 3. Ejecutar el workflow manualmente

1. Ve a tu workflow en n8n
2. Haz clic en **"Execute Workflow"** (o activa el webhook si usaste uno)
3. Monitorea la ejecución en tiempo real
4. Verifica que cada paso se complete exitosamente

### 4. Verificar resultados en Supabase

1. Ve a tu base de datos en Supabase
2. Consulta la tabla `reports`:
```sql
SELECT id, labels, colors, species 
FROM reports 
WHERE labels IS NOT NULL 
LIMIT 10;
```

Deberías ver los reportes actualizados con los labels y colores detectados.

---

## 🔄 Automatización con Schedule Trigger

Para procesar automáticamente nuevos reportes cada cierto tiempo:

1. **Reemplaza el nodo Webhook** con un nodo **"Schedule Trigger"**
2. Configura:
   - **Trigger Times**: `Every hour` (o la frecuencia que prefieras)
   - **Cron Expression**: (opcional) para horarios específicos

---

## 🐛 Solución de Problemas

### Error: "Connection refused" al llamar al backend

**Problema**: n8n no puede acceder a `http://localhost:8003`

**Solución**:
1. Usa tu IP local en lugar de `localhost`: `http://192.168.0.204:8003`
2. O configura ngrok para exponer el backend públicamente
3. O usa un servidor remoto donde n8n pueda acceder

### Error: "Google Vision API key invalid"

**Problema**: La API key no está configurada correctamente

**Solución**:
1. Verifica que la API key esté en las credenciales de n8n
2. Asegúrate de que la API key tenga permisos para Vision API
3. Verifica que la cuenta de Google Cloud tenga facturación habilitada

### Error: "Reporte no encontrado" en process-result

**Problema**: El `report_id` no existe en la base de datos

**Solución**:
1. Verifica que el `report_id` se esté pasando correctamente desde el nodo Code
2. Asegúrate de que el reporte no haya sido eliminado

### El workflow procesa muy lento

**Solución**:
1. Aumenta el `Batch Size` en el nodo Split In Batches
2. Reduce el `limit` en la query inicial para procesar menos a la vez
3. Considera procesar solo reportes nuevos usando el filtro `has_labels=false`

---

## 📊 Monitoreo y Estadísticas

### Ver cuántos reportes faltan por procesar

```powershell
# Reportes sin labels
Invoke-WebRequest -Uri "http://localhost:8003/n8n/reports/with-images?has_labels=false&limit=1000" -Method GET
```

### Ver reportes ya procesados

```powershell
# Reportes con labels
Invoke-WebRequest -Uri "http://localhost:8003/n8n/reports/with-images?has_labels=true&limit=1000" -Method GET
```

---

## ✅ Checklist Final

- [ ] Backend corriendo y accesible desde n8n
- [ ] Endpoint `/n8n/health` responde correctamente
- [ ] Workflow creado en n8n con todos los nodos
- [ ] Google Cloud Vision API configurado
- [ ] Workflow activado y probado manualmente
- [ ] Resultados verificados en Supabase
- [ ] Schedule Trigger configurado (opcional)

---

## 🎉 ¡Listo!

Tu integración con n8n está configurada. Ahora n8n procesará automáticamente todas las imágenes de tus reportes y actualizará la base de datos con los análisis de Google Vision.

**Próximos pasos**:
- Configura un Schedule Trigger para procesar automáticamente nuevos reportes
- Monitorea el progreso verificando cuántos reportes tienen labels
- Ajusta los parámetros según tus necesidades

