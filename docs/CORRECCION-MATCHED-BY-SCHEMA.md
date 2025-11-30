# ✅ Corrección: Valores de `matched_by` según Schema

## Problema Encontrado

El schema de la base de datos define que el campo `matched_by` en la tabla `matches` solo puede tener estos valores:

```sql
CHECK (matched_by = ANY (ARRAY['ai_visual'::text, 'ai_text'::text, 'manual'::text]))
```

Pero el código estaba usando valores no permitidos:
- ❌ `"n8n_auto_search"` (no permitido)
- ❌ `"auto_clip"` (no permitido)

## Correcciones Realizadas

### 1. `backend/routers/n8n_integration.py`

**Línea 187 y 213:**
- **Antes:** `"matched_by": "n8n_auto_search"`
- **Ahora:** `"matched_by": "ai_visual"` ✅

**Razón:** Usa embeddings de imágenes para búsqueda visual de coincidencias.

### 2. `backend/routers/embeddings_supabase.py`

**Línea 148:**
- **Antes:** `"matched_by": "auto_clip"`
- **Ahora:** `"matched_by": "ai_visual"` ✅

**Razón:** Usa OpenCLIP para generar embeddings de imágenes y compararlos.

## Valores Permitidos

Según el schema, estos son los únicos valores válidos:

1. **`"ai_visual"`**: Para matches generados usando embeddings de imágenes (OpenCLIP, Google Vision, etc.)
2. **`"ai_text"`**: Para matches generados usando análisis de texto (descripciones, embeddings de texto)
3. **`"manual"`**: Para matches creados manualmente por usuarios

## Verificación

Todos los lugares donde se usa `matched_by` ahora usan valores válidos:

- ✅ `backend/routers/n8n_integration.py`: `"ai_visual"` (2 lugares)
- ✅ `backend/routers/embeddings_supabase.py`: `"ai_visual"` (1 lugar)
- ✅ `backend/routers/matches.py`: Solo lee el valor, no lo establece

## Resultado

Ahora el código cumple con el constraint CHECK de la base de datos y no debería generar errores al insertar o actualizar matches.











