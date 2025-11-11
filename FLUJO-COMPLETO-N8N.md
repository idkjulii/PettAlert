# 🔄 Flujo Completo de la Integración con n8n

Este documento explica paso a paso cómo funciona toda la integración con n8n.

---

## 📊 Diagrama del Flujo Completo

```
┌─────────────────────────────────────────────────────────────────┐
│                    INICIO: Crear Reporte                        │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 1. Usuario crea reporte en la app móvil                        │
│    - Sube foto de la mascota                                   │
│    - Completa información (especie, color, etc.)               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 2. App móvil → Backend (POST /reports)                         │
│    Envía: {photos: [...], species: "dog", ...}                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 3. Backend guarda reporte en Supabase                          │
│    - Reporte creado con ID único                               │
│    - Fotos guardadas en Supabase Storage                       │
│    - URLs de las fotos guardadas en campo photos[]             │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 4. Backend genera embedding automáticamente                    │
│    (Esto es independiente de n8n, se hace en paralelo)         │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 5. OPCIÓN A: Envío Automático (si está configurado)           │
│    OPCIÓN B: Envío Manual (desde admin o script)               │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 6. Backend → Webhook de n8n (POST)                             │
│    URL: https://n8n.arc-ctes.shop/webhook-test/...             │
│    Body: {                                                      │
│      report_id: "uuid",                                         │
│      image_url: "https://...",                                  │
│      species: "dog",                                            │
│      type: "lost",                                              │
│      ...                                                        │
│    }                                                            │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. n8n recibe datos en el nodo Webhook                         │
│    - Activa el workflow automáticamente                        │
│    - Datos disponibles en $json                                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 8. n8n: HTTP Request - Descargar Imagen                        │
│    GET {{ $json.image_url }}                                    │
│    - Descarga la imagen desde Supabase Storage                 │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 9. n8n: Google Cloud Vision - Análisis                         │
│    - Analiza la imagen descargada                              │
│    - Detecta labels: ["dog", "pet", "golden retriever"]        │
│    - Detecta colores: ["#FFD700", "#8B4513"]                   │
│    - Determina especie: "dog"                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 10. n8n: Code - Formatear Datos                                │
│     - Extrae labels, colores, especie del resultado            │
│     - Prepara payload para enviar al backend                   │
│     {                                                           │
│       report_id: "uuid",                                        │
│       labels: [...],                                            │
│       colors: [...],                                            │
│       species: "dog"                                            │
│     }                                                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 11. n8n → Backend (POST /n8n/process-result)                   │
│     URL: http://TU_IP:8003/n8n/process-result                  │
│     Body: {                                                     │
│       report_id: "uuid",                                        │
│       image_url: "https://...",                                 │
│       labels: [{label: "dog", score: 95}, ...],                │
│       colors: ["#FFD700", "#8B4513"],                          │
│       species: "dog"                                            │
│     }                                                           │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│ 12. Backend actualiza reporte en Supabase                      │
│     - Guarda labels en columna labels (JSONB)                  │
│     - Guarda colores en columna colors (TEXT[])                │
│     - Actualiza especie si no estaba definida                  │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                    FIN: Reporte Actualizado                     │
│  El reporte ahora tiene labels y colores para búsqueda IA      │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📝 Descripción Detallada de Cada Paso

### Paso 1-3: Creación del Reporte

**Usuario crea reporte** → **App envía al backend** → **Backend guarda en Supabase**

- El usuario sube una foto y completa información
- La app envía los datos al endpoint `POST /reports`
- El backend guarda el reporte en Supabase con las URLs de las fotos

**Estado del reporte:**
```json
{
  "id": "uuid-123",
  "photos": ["https://supabase.co/storage/.../foto1.jpg"],
  "species": "dog",
  "labels": null,  // ← Aún no tiene labels
  "colors": null   // ← Aún no tiene colores
}
```

---

### Paso 4: Generación de Embedding (Paralelo)

**Backend genera embedding automáticamente**

- Esto es independiente de n8n
- Se hace automáticamente cuando se crea un reporte con fotos
- Genera un vector de 512 dimensiones para búsqueda por similitud visual

---

### Paso 5: Decisión de Envío

**Hay dos formas de enviar reportes a n8n:**

#### Opción A: Envío Manual
```powershell
# Desde PowerShell o script
POST /n8n/send-to-webhook
{
  "report_id": "uuid-123"
}
```

#### Opción B: Envío Automático (si se configura)
- Se puede configurar para que se envíe automáticamente al crear reportes
- O usar un Schedule Trigger en n8n para procesar reportes periódicamente

#### Opción C: Procesamiento Batch
```powershell
# Procesar múltiples reportes a la vez
POST /n8n/batch-process
{
  "limit": 10,
  "has_labels": false
}
```

---

### Paso 6: Envío al Webhook de n8n

**Backend → Webhook de n8n**

**URL del webhook:**
```
https://n8n.arc-ctes.shop/webhook-test/9f0311e4-6678-4884-b9d1-af2276fe6aec
```

**Datos enviados (POST):**
```json
{
  "report_id": "uuid-123",
  "image_url": "https://supabase.co/storage/.../foto1.jpg",
  "image_index": 0,
  "total_images": 1,
  "species": "dog",
  "type": "lost",
  "status": "active",
  "created_at": "2024-01-01T00:00:00Z",
  "has_labels": false
}
```

**Nota:** Si un reporte tiene múltiples fotos, se envía una petición por cada foto.

---

### Paso 7-9: Procesamiento en n8n

**n8n recibe → Descarga imagen → Analiza con Google Vision**

1. **Webhook recibe datos**: El workflow se activa automáticamente
2. **Descarga imagen**: HTTP Request GET a `image_url`
3. **Análisis con Google Vision**: Detecta labels, colores, especie

**Resultado de Google Vision:**
```json
{
  "labels": [
    {"label": "Dog", "score": 0.95},
    {"label": "Pet", "score": 0.92},
    {"label": "Golden Retriever", "score": 0.88}
  ],
  "colors": [
    {"red": 255, "green": 215, "blue": 0},   // #FFD700
    {"red": 139, "green": 69, "blue": 19}    // #8B4513
  ]
}
```

---

### Paso 10: Formateo de Datos en n8n

**Code Node formatea los resultados**

Transforma los datos de Google Vision al formato que espera el backend:

```json
{
  "report_id": "uuid-123",
  "image_url": "https://...",
  "labels": [
    {"label": "Dog", "score": 95.0},
    {"label": "Pet", "score": 92.0}
  ],
  "colors": ["#FFD700", "#8B4513"],
  "species": "dog",
  "analysis_metadata": {
    "processed_at": "2024-01-01T12:00:00Z"
  }
}
```

---

### Paso 11: n8n Envía Resultados al Backend

**n8n → Backend (POST /n8n/process-result)**

**URL del backend:**
```
http://TU_IP_LOCAL:8003/n8n/process-result
```

**⚠️ IMPORTANTE:** 
- Cambia `TU_IP_LOCAL` por tu IP local (ej: `192.168.0.204`)
- O usa ngrok si el backend está en un servidor remoto

**Body enviado:**
```json
{
  "report_id": "uuid-123",
  "image_url": "https://...",
  "labels": [...],
  "colors": [...],
  "species": "dog"
}
```

---

### Paso 12: Backend Actualiza Supabase

**Backend guarda los resultados en la base de datos**

El endpoint `/n8n/process-result`:
1. Recibe los resultados de n8n
2. Obtiene el reporte actual de Supabase
3. Actualiza los campos:
   - `labels`: Guarda los labels detectados
   - `colors`: Guarda los colores dominantes
   - `species`: Actualiza si no estaba definida

**Estado final del reporte:**
```json
{
  "id": "uuid-123",
  "photos": ["https://..."],
  "species": "dog",
  "labels": {
    "labels": [
      {"label": "Dog", "score": 95.0},
      {"label": "Pet", "score": 92.0}
    ],
    "source": "n8n_google_vision",
    "processed_at": "2024-01-01T12:00:00Z"
  },
  "colors": ["#FFD700", "#8B4513"]
}
```

---

## 🔄 Flujos Adicionales

### Flujo de Procesamiento Batch

```
1. POST /n8n/batch-process
   {
     "limit": 10,
     "has_labels": false
   }

2. Backend obtiene 10 reportes sin procesar

3. Backend envía cada reporte al webhook de n8n
   (en background, no bloquea)

4. n8n procesa cada uno independientemente

5. n8n envía resultados de vuelta al backend

6. Backend actualiza cada reporte
```

---

### Flujo con Múltiples Imágenes

Si un reporte tiene 3 fotos:

```
Backend envía:
  - Foto 1 → Webhook n8n
  - Foto 2 → Webhook n8n  
  - Foto 3 → Webhook n8n

n8n procesa cada una independientemente

n8n envía resultados:
  - Resultado foto 1 → Backend
  - Resultado foto 2 → Backend
  - Resultado foto 3 → Backend

Backend actualiza el reporte con el mejor análisis
```

---

## 🎯 Casos de Uso

### Caso 1: Procesar Reportes Existentes

```powershell
# Procesar todos los reportes sin labels
POST /n8n/batch-process
{
  "limit": 100,
  "has_labels": false
}
```

### Caso 2: Procesar un Reporte Específico

```powershell
POST /n8n/send-to-webhook
{
  "report_id": "uuid-especifico"
}
```

### Caso 3: Procesamiento Automático Periódico

1. Configurar Schedule Trigger en n8n (cada hora)
2. n8n llama a: `GET /n8n/reports/with-images?has_labels=false&limit=10`
3. n8n procesa cada reporte
4. n8n envía resultados al backend

---

## ⚡ Puntos Clave

1. **El backend envía datos** al webhook de n8n (push)
2. **n8n procesa** las imágenes con Google Vision
3. **n8n envía resultados** al backend (callback)
4. **Backend actualiza** Supabase con los resultados

---

## 🔗 Endpoints Involucrados

| Endpoint | Dirección | Propósito |
|----------|-----------|-----------|
| Webhook n8n | `https://n8n.arc-ctes.shop/webhook-test/...` | Recibe datos del backend |
| `/n8n/send-to-webhook` | Backend | Envía reporte a n8n |
| `/n8n/batch-process` | Backend | Procesa múltiples reportes |
| `/n8n/process-result` | Backend | Recibe resultados de n8n |
| `/n8n/reports/with-images` | Backend | Lista reportes para procesar |

---

## ✅ Checklist del Flujo

- [ ] Reporte creado en Supabase
- [ ] Backend envía datos al webhook de n8n
- [ ] n8n recibe datos correctamente
- [ ] n8n descarga imagen exitosamente
- [ ] Google Vision analiza la imagen
- [ ] n8n formatea los resultados
- [ ] n8n envía resultados al backend
- [ ] Backend actualiza reporte en Supabase
- [ ] Reporte tiene labels y colores guardados

---

¿Necesitas ayuda con algún paso específico del flujo?











