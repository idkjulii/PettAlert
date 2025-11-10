# ✅ Solución Definitiva: Error RPC Supabase

## Error

```
Could not find the function public.search_similar_reports without parameters in the schema cache
```

## Causa

Cuando usas "Using JSON" con `JSON.stringify()`, n8n puede estar enviando el body de una manera que Supabase no puede parsear correctamente para RPC calls.

## Solución Definitiva

### Opción 1: Usar modo Raw (Recomendado)

En el nodo "HTTP Request2":

1. **Body Content Type:** `Raw`
2. **Content Type (Header):** Déjalo vacío o `application/json` (si ya tienes Content-Type en Header Parameters, déjalo vacío)
3. **Body:** 

```javascript
={{ JSON.stringify({
  "query_embedding": $json.body.embedding,
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": $json.body.report_data?.species || null,
  "filter_type": ($json.body.report_data?.type === 'lost') ? 'found' : 'lost'
}) }}
```

**IMPORTANTE:** El body debe empezar con `={{` y terminar con `}}`.

### Opción 2: Construir el JSON en un nodo Code antes

Agrega un nodo Code antes de "HTTP Request2":

```javascript
// Construir el body para Supabase RPC
const bodyForSupabase = {
  query_embedding: $json.body.embedding,
  match_threshold: 0.7,
  match_count: 10,
  filter_species: $json.body.report_data?.species || null,
  filter_type: ($json.body.report_data?.type === 'lost') ? 'found' : 'lost'
};

return {
  json: {
    ...$json,
    supabaseRpcBody: bodyForSupabase
  }
};
```

Luego en "HTTP Request2":
- Body Content Type: `Raw`
- Body: `={{ JSON.stringify($json.supabaseRpcBody) }}`

### Opción 3: Verificar que la función existe y tiene permisos

Ejecuta en Supabase SQL Editor:

```sql
-- Verificar que la función existe
SELECT 
    p.proname as function_name,
    pg_get_function_arguments(p.oid) as arguments
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public' 
AND p.proname = 'search_similar_reports';

-- Dar permisos si no los tiene
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO anon;
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO authenticated;
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO service_role;
```

## Verificación del Formato

El body que se envía debe ser exactamente:

```json
{
  "query_embedding": [0.123, 0.456, ...],
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": "dog",
  "filter_type": "found"
}
```

**Sin comillas extra, sin arrays anidados, objeto JSON plano.**

## Debugging

Agrega un nodo Code antes de "HTTP Request2" para inspeccionar:

```javascript
const body = {
  query_embedding: $json.body.embedding,
  match_threshold: 0.7,
  match_count: 10,
  filter_species: $json.body.report_data?.species || null,
  filter_type: ($json.body.report_data?.type === 'lost') ? 'found' : 'lost'
};

const bodyString = JSON.stringify(body);

return {
  json: {
    debug: {
      embeddingExists: !!$json.body.embedding,
      embeddingLength: $json.body.embedding?.length,
      embeddingType: typeof $json.body.embedding,
      isArray: Array.isArray($json.body.embedding),
      bodyStringLength: bodyString.length,
      bodyStringPreview: bodyString.substring(0, 300)
    },
    body: body,
    bodyString: bodyString
  }
};
```

Esto te mostrará exactamente qué se está enviando.









