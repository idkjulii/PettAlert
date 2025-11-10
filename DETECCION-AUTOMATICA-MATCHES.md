# 🔍 Sistema de Detección Automática de Coincidencias

## Resumen

Este sistema detecta automáticamente cuando un reporte de mascota perdida o encontrada coincide con otro reporte existente, usando **lógica profunda** basada en embeddings y análisis de imágenes.

## Flujo Completo

### 1. Creación de Reporte

Cuando un usuario crea un reporte con fotos:

```
1. Usuario crea reporte → Backend recibe datos
2. Backend guarda reporte en Supabase
3. Backend genera embedding automáticamente (OpenCLIP)
4. Backend envía reporte a n8n con embedding incluido
```

### 2. Procesamiento en n8n

El flujo de n8n procesa el reporte:

```
1. n8n recibe webhook con:
   - report_id
   - image_url
   - embedding (vector de 512 dimensiones)
   - report_data (type, species, location)

2. n8n descarga y analiza la imagen:
   - Google Vision para labels y colores
   - Detección de especie

3. Si hay embedding, n8n busca coincidencias:
   - Llama a Supabase RPC: search_similar_reports
   - Filtra por tipo opuesto (lost ↔ found)
   - Filtra por especie
   - Retorna matches con similitud >= 0.7

4. n8n retorna resultado al backend:
   - Labels y colores detectados
   - Matches encontrados (si los hay)
```

### 3. Procesamiento de Matches en Backend

El backend recibe los resultados de n8n:

```
1. Backend recibe respuesta en /n8n/process-result
2. Actualiza el reporte con labels y colores
3. Procesa matches encontrados:
   - Guarda en tabla matches
   - Crea relación lost_report_id ↔ found_report_id
   - Marca como "pending"
   - Evita duplicados
```

### 4. Notificación al Usuario

El usuario puede consultar sus matches:

```
GET /matches/pending?user_id={user_id}
GET /matches/pending?report_id={report_id}
```

## Endpoints del Backend

### Crear Reporte

```http
POST /reports/
Content-Type: application/json

{
  "type": "lost",
  "reporter_id": "uuid",
  "species": "dog",
  "description": "...",
  "photos": ["https://..."],
  "location": {...}
}
```

**Respuesta:**
- El reporte se crea
- Se genera embedding automáticamente
- Se envía a n8n en background
- n8n busca coincidencias automáticamente

### Procesar Resultado de n8n

```http
POST /n8n/process-result
Content-Type: application/json

{
  "report_id": "uuid",
  "analysis": {
    "labels": [...],
    "colors": [...],
    "species_detected": "dog"
  },
  "matches": {
    "matches_found": 2,
    "matches": [
      {
        "report_id": "uuid",
        "similarity_score": 0.85,
        "species": "dog",
        "type": "found",
        "photo": "https://...",
        "description": "..."
      }
    ]
  }
}
```

**Respuesta:**
- Reporte actualizado con labels/colores
- Matches guardados en base de datos
- Estado: `pending` para revisión del usuario

### Obtener Matches Pendientes

```http
GET /matches/pending?user_id={user_id}&status=pending
GET /matches/pending?report_id={report_id}&status=pending
```

**Respuesta:**
```json
{
  "matches": [
    {
      "match_id": "uuid",
      "similarity_score": 0.85,
      "matched_by": "n8n_auto_search",
      "status": "pending",
      "created_at": "2024-...",
      "lost_report": {...},
      "found_report": {...}
    }
  ],
  "count": 1
}
```

### Actualizar Estado de Match

```http
PUT /matches/{match_id}/status?status=accepted
PUT /matches/{match_id}/status?status=rejected
```

## Estructura de Datos

### Tabla `matches`

```sql
CREATE TABLE matches (
  id UUID PRIMARY KEY,
  lost_report_id UUID REFERENCES reports(id),
  found_report_id UUID REFERENCES reports(id),
  similarity_score FLOAT,
  matched_by TEXT,  -- 'n8n_auto_search', 'manual', etc.
  status TEXT,      -- 'pending', 'accepted', 'rejected'
  created_at TIMESTAMP
);
```

### Payload a n8n

```json
{
  "report_id": "uuid",
  "image_url": "https://...",
  "embedding": [0.123, 0.456, ...],  // 512 dimensiones
  "report_data": {
    "type": "lost",
    "species": "dog",
    "location": {...}
  }
}
```

### Respuesta de n8n

```json
{
  "success": true,
  "report_id": "uuid",
  "analysis": {
    "labels": [...],
    "colors": [...],
    "species_detected": "dog"
  },
  "matches": {
    "matches_found": 2,
    "matches": [
      {
        "report_id": "uuid",
        "similarity_score": 0.85,
        "species": "dog",
        "type": "found",
        "photo": "https://...",
        "description": "..."
      }
    ],
    "threshold": 0.7,
    "searched_at": "2024-..."
  }
}
```

## Configuración de n8n

El flujo de n8n debe:

1. **Recibir webhook** con embedding
2. **Analizar imagen** con Google Vision
3. **Buscar coincidencias** si hay embedding:
   ```javascript
   // En n8n, llamar a Supabase RPC
   POST https://{supabase_url}/rest/v1/rpc/search_similar_reports
   {
     "query_embedding": {{ $json.body.embedding }},
     "match_threshold": 0.7,
     "match_count": 10,
     "filter_species": "{{ $json.body.report_data?.species }}",
     "filter_type": "{{ $json.body.report_data?.type === 'lost' ? 'found' : 'lost' }}"
   }
   ```
4. **Retornar resultado** al backend:
   ```javascript
   POST https://{backend_url}/n8n/process-result
   {
     "report_id": "...",
     "analysis": {...},
     "matches": {...}
   }
   ```

## Umbrales y Configuración

- **Umbral de similitud mínimo**: `0.7` (70%)
- **Máximo de matches retornados**: `10`
- **Filtro automático por especie**: Sí
- **Filtro automático por tipo opuesto**: Sí (lost ↔ found)

## Ventajas del Sistema

1. **Automático**: No requiere intervención manual
2. **Rápido**: Búsqueda por embeddings es muy eficiente
3. **Preciso**: Usa similitud coseno de vectores de 512 dimensiones
4. **Escalable**: Funciona con miles de reportes
5. **Inteligente**: Combina embeddings con análisis de Google Vision

## Próximos Pasos

1. **Notificaciones push**: Enviar notificación cuando se detecte un match
2. **Filtros geográficos**: Considerar distancia en la búsqueda
3. **Machine Learning**: Aprender de matches aceptados/rechazados
4. **Dashboard**: Visualización de matches y estadísticas









