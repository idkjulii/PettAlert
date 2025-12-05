# 🔍 Sistema de Detección Automática de Coincidencias

## Resumen

Este sistema detecta automáticamente cuando un reporte de mascota perdida o encontrada coincide con otro reporte existente, usando **lógica profunda** basada en embeddings y análisis de imágenes.

## Flujo Completo

### 1. Creación de Reporte

Cuando un usuario crea un reporte con fotos:

```
1. Usuario crea reporte → Backend recibe datos
2. Backend guarda reporte en Supabase
3. Backend genera embedding automáticamente (MegaDescriptor)
4. Backend busca coincidencias automáticamente usando el embedding
5. Backend guarda matches encontrados en la tabla matches
```

### 2. Procesamiento Automático de Matches

El backend procesa todo localmente:

```
1. Backend genera embedding con MegaDescriptor:
   - report_id
   - image_url
   - embedding (vector de 2048 dimensiones)
   - report_data (type, species, location)

2. Backend busca coincidencias automáticamente:
   - Usa función find_and_save_matches()
   - Busca reportes del tipo opuesto (lost ↔ found)
   - Filtra por especie si está disponible
   - Calcula similitud usando embeddings
   - Retorna matches con similitud >= threshold (default: 0.1)

3. Backend guarda matches encontrados:
   - Guarda en tabla matches
   - Crea relación lost_report_id ↔ found_report_id
   - Marca como "pending"
   - Evita duplicados
   - Usa matched_by: "ai_visual"
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

### Buscar Matches para un Reporte

```http
POST /direct-matches/find/{report_id}
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
      "matched_by": "ai_visual",
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
  matched_by TEXT,  -- 'ai_visual', 'ai_text', 'manual', etc.
  status TEXT,      -- 'pending', 'accepted', 'rejected'
  created_at TIMESTAMP
);
```

### Procesamiento Interno

```json
{
  "report_id": "uuid",
  "image_url": "https://...",
  "embedding": [0.123, 0.456, ...],  // 2048 dimensiones (MegaDescriptor)
  "report_data": {
    "type": "lost",
    "species": "dog",
    "location": {...}
  }
}
```

### Resultado del Procesamiento

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

## Configuración del Backend

El backend procesa automáticamente:

1. **Generar embedding** con MegaDescriptor cuando se crea un reporte
2. **Buscar coincidencias** automáticamente usando el embedding:
   ```python
   # En el backend, función find_and_save_matches()
   # Busca reportes del tipo opuesto con embeddings
   # Calcula similitud usando numpy
   # Guarda matches en la tabla matches
   ```
3. **Guardar matches** automáticamente:
   ```python
   # El backend guarda matches directamente en Supabase
   # Usa matched_by: "ai_visual"
   # Estado inicial: "pending"
   ```

## Umbrales y Configuración

- **Umbral de similitud mínimo**: `0.7` (70%)
- **Máximo de matches retornados**: `10`
- **Filtro automático por especie**: Sí
- **Filtro automático por tipo opuesto**: Sí (lost ↔ found)

## Ventajas del Sistema

1. **Automático**: No requiere intervención manual
2. **Rápido**: Búsqueda por embeddings es muy eficiente
3. **Preciso**: Usa similitud coseno de vectores de 2048 dimensiones (MegaDescriptor)
4. **Escalable**: Funciona con miles de reportes
5. **Inteligente**: Usa MegaDescriptor especializado en reconocimiento de animales

## Próximos Pasos

1. **Notificaciones push**: Enviar notificación cuando se detecte un match
2. **Filtros geográficos**: Considerar distancia en la búsqueda
3. **Machine Learning**: Aprender de matches aceptados/rechazados
4. **Dashboard**: Visualización de matches y estadísticas











