# 📋 Resumen del Flujo n8n Completo

## Flujo Actual

```
1. Webhook
   ↓ Recibe datos del backend
2. HTTP Request
   ↓ Descarga imagen desde image_url
3. Code in JavaScript
   ↓ Convierte imagen a Base64
4. Preparar JSON para Google Vision
   ↓ Construye JSON para Google Vision API
5. HTTP Request1
   ↓ Llama a Google Vision API
6. Code in JavaScript1
   ↓ Procesa respuesta (labels, colores, especie)
7. If
   ↓ Verifica si hay embedding
   ├─ SÍ → HTTP Request2 (busca matches)
   └─ NO → Merge (sin matches)
8. HTTP Request2 (si hay embedding)
   ↓ Busca coincidencias en Supabase
9. Formatear matches
   ↓ Formatea resultados de matches
10. Merge
    ↓ Une resultados (análisis + matches)
11. Respond to Webhook
    ↓ Retorna respuesta al backend
```

## Estado de Cada Nodo

### ✅ 1. Webhook
- **Recibe:** Datos del backend con `report_id`, `image_url`, `embedding`, etc.
- **Estado:** OK

### ✅ 2. HTTP Request
- **Descarga:** Imagen desde `$json.body.image_url`
- **Formato:** File (binary)
- **Estado:** OK

### ✅ 3. Code in JavaScript
- **Convierte:** Imagen binary → Base64
- **Limpia:** Base64 (remueve espacios, verifica que no empiece con `=`)
- **Retorna:** `imageBase64`, `originalBody`
- **Estado:** OK

### ✅ 4. Preparar JSON para Google Vision
- **Construye:** JSON para Google Vision API
- **Retorna:** `googleVisionBody`, `originalBody`
- **Estado:** OK

### ✅ 5. HTTP Request1
- **URL:** Google Vision API
- **Body:** Raw con `JSON.stringify($json.googleVisionBody)`
- **API Key:** ✅ Funcionando
- **Estado:** ✅ **FUNCIONANDO** (ya probado exitosamente)

### ✅ 6. Code in JavaScript1
- **Procesa:** Respuesta de Google Vision
- **Extrae:**
  - Labels (etiquetas)
  - Colores dominantes
  - Especie detectada
- **Retorna:**
  - `analysis` (labels, colors, species_detected)
  - `metadata`
  - `body` (con embedding para el nodo If)
- **Estado:** ✅ **CÓDIGO ACTUALIZADO CORRECTAMENTE**

### ⚠️ 7. If
- **Verifica:** Si existe `$json.body.embedding`
- **Problema potencial:** El embedding debe estar en `$json.body.embedding`
- **Estado:** Verificar que Code in JavaScript1 pase el embedding correctamente

### ✅ 8. HTTP Request2
- **URL:** Supabase RPC `search_similar_reports`
- **Body:** Query con embedding, threshold, filters
- **Estado:** OK (siempre que el embedding llegue)

### ✅ 9. Formatear matches
- **Formatea:** Respuesta de Supabase
- **Filtra:** Matches con similitud >= 0.7
- **Ordena:** Por similitud descendente
- **Estado:** OK

### ✅ 10. Merge
- **Une:** Resultados de análisis + matches
- **Estado:** OK

### ✅ 11. Respond to Webhook
- **Retorna:** Respuesta completa al backend
- **Estado:** OK

## Verificaciones Necesarias

### 1. Verificar que el embedding llegue correctamente

El nodo "If" busca `$json.body.embedding`. Asegúrate de que:

1. El backend envíe el embedding en el webhook:
   ```json
   {
     "report_id": "...",
     "image_url": "...",
     "embedding": [0.123, 0.456, ...]
   }
   ```

2. El nodo "Code in JavaScript1" lo pase correctamente:
   ```javascript
   body: {
     embedding: webhookData.embedding || webhookData.body?.embedding,
     report_data: webhookData.report_data || webhookData
   }
   ```

### 2. Verificar formato de respuesta final

El nodo "Respond to Webhook" debe retornar:
```json
{
  "success": true,
  "report_id": "...",
  "analysis": {
    "labels": [...],
    "colors": [...],
    "species_detected": "dog"
  },
  "matches": {
    "matches_found": 2,
    "matches": [...]
  }
}
```

## Pruebas Recomendadas

### Prueba 1: Flujo completo con embedding
1. Enviar webhook con embedding
2. Verificar que Google Vision procese correctamente
3. Verificar que busque matches en Supabase
4. Verificar respuesta final

### Prueba 2: Flujo sin embedding
1. Enviar webhook sin embedding
2. Verificar que Google Vision procese correctamente
3. Verificar que NO busque matches (debe ir directo a Merge)
4. Verificar respuesta final sin matches

## Posibles Mejoras

1. **Manejo de errores:** Agregar try-catch en nodos críticos
2. **Logging:** Agregar logs para debugging
3. **Validación:** Validar que el Base64 sea válido antes de enviar
4. **Timeout:** Configurar timeouts apropiados para cada request

## Flujo de Datos Completo

```
Webhook recibe:
{
  report_id: "uuid",
  image_url: "https://...",
  embedding: [0.123, ...],
  report_data: { type: "lost", species: "dog" }
}
   ↓
HTTP Request descarga imagen
   ↓
Code in JavaScript convierte a Base64
   ↓
Preparar JSON construye request para Google Vision
   ↓
HTTP Request1 → Google Vision API
   ↓ Retorna:
{
  responses: [{
    labelAnnotations: [...],
    imagePropertiesAnnotation: {...}
  }]
}
   ↓
Code in JavaScript1 procesa y retorna:
{
  analysis: { labels, colors, species_detected },
  body: { embedding, report_data }
}
   ↓
If verifica embedding
   ├─ SÍ → HTTP Request2 busca matches
   │   ↓ Retorna matches de Supabase
   │   ↓ Formatear matches
   └─ NO → Va directo a Merge
   ↓
Merge une resultados
   ↓
Respond to Webhook retorna al backend:
{
  analysis: {...},
  matches: {...}
}
```









