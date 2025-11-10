# 🔧 Solución: Error RPC Function en Supabase

## Error

```
Could not find the function public.search_similar_reports without parameters in the schema cache
```

## Causa

Supabase está recibiendo la petición pero **no está reconociendo los parámetros**. Esto puede deberse a:

1. El formato del embedding no es correcto
2. Los parámetros no se están enviando correctamente
3. La función RPC necesita permisos específicos

## Soluciones

### ✅ Solución 1: Verificar formato del Body (más probable)

Cuando llamas a una función RPC de Supabase, el body debe ser un **objeto JSON plano** con los nombres exactos de los parámetros.

**En el nodo "HTTP Request2":**

1. **Body Content Type:** `Raw`
2. **Content Type Header:** `application/json`
3. **Body:** Usa esta expresión:

```javascript
={{ JSON.stringify({
  "query_embedding": $json.body.embedding,
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": $json.body.report_data?.species || null,
  "filter_type": ($json.body.report_data?.type === 'lost') ? 'found' : 'lost'
}) }}
```

### ✅ Solución 2: Verificar que la función existe en Supabase

Ejecuta este SQL en Supabase para verificar que la función existe:

```sql
SELECT 
    p.proname as function_name,
    pg_get_function_arguments(p.oid) as arguments
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public' 
AND p.proname = 'search_similar_reports';
```

### ✅ Solución 3: Verificar permisos de la función

En Supabase, la función debe tener permisos para ser ejecutada. Ejecuta:

```sql
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO anon;
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO authenticated;
```

### ✅ Solución 4: Probar la función directamente

Prueba llamar la función directamente desde Supabase SQL Editor:

```sql
SELECT * FROM search_similar_reports(
  query_embedding := (SELECT embedding FROM reports LIMIT 1),
  match_threshold := 0.7,
  match_count := 10,
  filter_species := 'dog',
  filter_type := 'found'
);
```

Si esto funciona, el problema está en cómo n8n está enviando los parámetros.

### ✅ Solución 5: Usar formato alternativo del Body

Si el problema persiste, prueba enviar el body sin `JSON.stringify()` usando modo JSON:

1. **Body Content Type:** `JSON`
2. **Specify Body:** `Using JSON`
3. **JSON Body:** Construye el objeto directamente:

```json
{
  "query_embedding": {{ $json.body.embedding }},
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": {{ $json.body.report_data?.species || null }},
  "filter_type": {{ $json.body.report_data?.type === 'lost' ? 'found' : 'lost' }}
}
```

**Nota:** Este formato puede no funcionar si el embedding es un array grande.

## Formato Esperado por Supabase

Supabase espera que el body sea exactamente:

```json
{
  "query_embedding": [0.123, 0.456, ...],  // Array de 512 números
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": "dog",
  "filter_type": "found"
}
```

## Debugging

Agrega un nodo Code antes de "HTTP Request2" para verificar el formato:

```javascript
const body = {
  query_embedding: $json.body.embedding,
  match_threshold: 0.7,
  match_count: 10,
  filter_species: $json.body.report_data?.species || null,
  filter_type: ($json.body.report_data?.type === 'lost') ? 'found' : 'lost'
};

return {
  json: {
    debug: {
      embeddingLength: $json.body.embedding?.length,
      embeddingType: typeof $json.body.embedding,
      isArray: Array.isArray($json.body.embedding),
      bodyString: JSON.stringify(body).substring(0, 200)
    },
    body: body
  }
};
```

Esto te ayudará a verificar que el embedding esté en el formato correcto antes de enviarlo.









