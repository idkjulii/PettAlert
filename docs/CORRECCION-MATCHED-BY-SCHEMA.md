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

### 1. Código Actualizado

**Todos los lugares donde se crean matches:**
- **Antes:** `"matched_by": "n8n_auto_search"` o `"auto_clip"`
- **Ahora:** `"matched_by": "ai_visual"` ✅

**Razón:** Usa embeddings de imágenes (MegaDescriptor) para búsqueda visual de coincidencias.

### 2. `backend/routers/embeddings_supabase.py`

**Línea 148:**
- **Antes:** `"matched_by": "auto_clip"`
- **Ahora:** `"matched_by": "ai_visual"` ✅

**Razón:** Usa MegaDescriptor para generar embeddings de imágenes y compararlos.

## Valores Permitidos

Según el schema, estos son los únicos valores válidos:

1. **`"ai_visual"`**: Para matches generados usando embeddings de imágenes (MegaDescriptor)
2. **`"ai_text"`**: Para matches generados usando análisis de texto (descripciones, embeddings de texto)
3. **`"manual"`**: Para matches creados manualmente por usuarios

## Verificación

Todos los lugares donde se usa `matched_by` ahora usan valores válidos:

- ✅ `backend/routers/embeddings_supabase.py`: `"ai_visual"`
- ✅ `backend/routers/direct_matches.py`: `"ai_visual"`
- ✅ `backend/routers/reports.py`: `"ai_visual"` (en find_and_save_matches)
- ✅ `backend/routers/matches.py`: Solo lee el valor, no lo establece

## Resultado

Ahora el código cumple con el constraint CHECK de la base de datos y no debería generar errores al insertar o actualizar matches.











