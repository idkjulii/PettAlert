# 🔍 ¿Cómo n8n Busca las Coincidencias?

## Respuesta Corta

**n8n busca las coincidencias directamente en Supabase** usando una función SQL especial que compara embeddings. No busca en otra base de datos, busca en la misma tabla `reports` de tu proyecto.

## Flujo Detallado

### 1. n8n Recibe el Embedding

Cuando el backend envía el reporte a n8n, incluye el **embedding** (vector de 512 números):

```json
{
  "report_id": "uuid",
  "image_url": "https://...",
  "embedding": [0.123, 0.456, -0.789, ...],  // 512 números
  "report_data": {
    "type": "lost",
    "species": "dog"
  }
}
```

### 2. n8n Llama a Supabase

n8n hace una petición HTTP **directamente a tu base de datos Supabase**:

```
POST https://eamsbroadstwkrkjcuvo.supabase.co/rest/v1/rpc/search_similar_reports
```

**Body que envía n8n:**
```json
{
  "query_embedding": [0.123, 0.456, ...],  // El embedding del nuevo reporte
  "match_threshold": 0.7,                   // Mínimo 70% de similitud
  "match_count": 10,                        // Máximo 10 resultados
  "filter_species": "dog",                  // Solo buscar perros
  "filter_type": "found"                    // Si el reporte es "lost", busca "found"
}
```

### 3. Supabase Busca en la Tabla `reports`

La función SQL `search_similar_reports` busca **directamente en tu tabla `reports`**:

```sql
SELECT 
    r.id,
    1 - (r.embedding <#> query_embedding) as similarity_score,
    r.species,
    r.type,
    r.photos,
    r.description,
    r.location,
    r.created_at
FROM public.reports r
WHERE 
    r.embedding IS NOT NULL              -- Solo reportes que tienen embedding
    AND r.status = 'active'              -- Solo reportes activos
    AND (1 - (r.embedding <#> query_embedding)) >= 0.7  -- Similitud >= 70%
    AND r.species = 'dog'                -- Misma especie
    AND r.type = 'found'                 -- Tipo opuesto (lost ↔ found)
ORDER BY r.embedding <#> query_embedding  -- Más similares primero
LIMIT 10;
```

### 4. ¿Cómo Funciona la Comparación?

La función usa **pgvector** (extensión de PostgreSQL) para comparar vectores:

- `<#>` es el operador de distancia coseno negativa
- `1 - (embedding1 <#> embedding2)` da el **score de similitud** (0 a 1)
- **0.0** = completamente diferente
- **1.0** = idéntico
- **0.7** = 70% similar (umbral mínimo)

### 5. Supabase Retorna los Matches

Supabase retorna los reportes más similares:

```json
[
  {
    "id": "uuid-1",
    "similarity_score": 0.85,
    "species": "dog",
    "type": "found",
    "photos": ["https://..."],
    "description": "...",
    "location": {...},
    "created_at": "2024-..."
  },
  {
    "id": "uuid-2",
    "similarity_score": 0.78,
    "species": "dog",
    "type": "found",
    ...
  }
]
```

### 6. n8n Formatea y Retorna

n8n formatea los resultados y los retorna al backend:

```json
{
  "matches_found": 2,
  "matches": [
    {
      "report_id": "uuid-1",
      "similarity_score": 0.85,
      "species": "dog",
      "type": "found",
      "photo": "https://...",
      "description": "..."
    }
  ]
}
```

## Resumen Visual

```
┌─────────────────┐
│  Backend        │
│  (Tu app)       │
└────────┬────────┘
         │
         │ 1. Envía reporte con embedding
         │
         ▼
┌─────────────────┐
│  n8n            │
│  (Webhook)      │
└────────┬────────┘
         │
         │ 2. Llama a Supabase RPC
         │    search_similar_reports()
         │
         ▼
┌─────────────────────────────────┐
│  Supabase                       │
│  (Tu base de datos)             │
│                                 │
│  Tabla: reports                 │
│  ├─ id: uuid-1                 │
│  ├─ embedding: [0.1, 0.2, ...] │ ← Compara con todos estos
│  ├─ type: "found"               │
│  └─ species: "dog"              │
│                                 │
│  ├─ id: uuid-2                 │
│  ├─ embedding: [0.3, 0.4, ...] │ ← Compara con todos estos
│  ├─ type: "found"               │
│  └─ species: "dog"              │
│                                 │
│  ... (más reportes)             │
└────────┬────────────────────────┘
         │
         │ 3. Retorna matches encontrados
         │
         ▼
┌─────────────────┐
│  n8n            │
│  (Formatea)     │
└────────┬────────┘
         │
         │ 4. Retorna al backend
         │
         ▼
┌─────────────────┐
│  Backend        │
│  (Guarda matches│
│   en tabla)     │
└─────────────────┘
```

## Puntos Clave

1. **n8n NO tiene su propia base de datos** - busca en **tu Supabase**
2. **Busca en la tabla `reports`** - la misma donde guardas los reportes
3. **Compara embeddings** - usa pgvector para comparar vectores de 512 dimensiones
4. **Filtra automáticamente** - por especie y tipo opuesto (lost ↔ found)
5. **Solo reportes activos** - ignora reportes resueltos o cancelados

## Configuración Necesaria

Para que funcione, necesitas:

1. ✅ **Tabla `reports`** con columna `embedding` tipo `vector(512)`
2. ✅ **Extensión pgvector** habilitada en Supabase
3. ✅ **Función SQL** `search_similar_reports` creada (ya está en `003_rag_functions.sql`)
4. ✅ **n8n configurado** con la URL de Supabase y las credenciales

## Verificar que Funciona

Puedes probar directamente desde Supabase:

```sql
-- Buscar coincidencias manualmente
SELECT * FROM search_similar_reports(
  query_embedding := (SELECT embedding FROM reports WHERE id = 'tu-report-id'),
  match_threshold := 0.7,
  match_count := 10,
  filter_species := 'dog',
  filter_type := 'found'
);
```

Esto te mostrará exactamente qué encuentra n8n cuando busca coincidencias.









