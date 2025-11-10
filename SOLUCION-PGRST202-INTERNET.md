# 🔍 Solución PGRST202 Basada en Búsqueda Web

## Error PGRST202

El error **PGRST202** de Supabase indica que:
> "Searched for the function public.search_similar_reports **without parameters**"

Esto significa que **Supabase NO está recibiendo el body** con los parámetros.

## Causas Comunes (Según Búsqueda Web)

1. **El body no se está enviando correctamente**
2. **El Content-Type no está configurado correctamente**
3. **Los parámetros no coinciden con la firma de la función**
4. **La función no existe o no tiene permisos**

## Soluciones Encontradas

### Solución 1: Verificar que el Body se Está Enviando

**Problema:** Aunque el body esté configurado, n8n puede no estar enviándolo.

**Solución:**
1. Abre **DevTools** del navegador (F12)
2. Ve a la pestaña **Network**
3. Ejecuta el nodo "HTTP Request2"
4. Busca la petición a `search_similar_reports`
5. Haz clic en ella
6. Ve a **Payload** o **Request**

**Verifica:**
- ¿Se está enviando un body?
- ¿El body tiene el contenido correcto?
- ¿El Content-Type está en los headers?

### Solución 2: Usar "Using JSON" en lugar de "Raw"

Si el modo Raw no funciona, prueba usar "Using JSON":

1. En "HTTP Request2":
   - **Body Content Type:** Cambia de "Raw" a **"JSON"**
   - **Body:** Usa el objeto directamente (no como string):

```json
{
  "query_embedding": {{ $json.supabaseRpcBody.query_embedding }},
  "match_threshold": {{ $json.supabaseRpcBody.match_threshold }},
  "match_count": {{ $json.supabaseRpcBody.match_count }},
  "filter_species": "{{ $json.supabaseRpcBody.filter_species }}",
  "filter_type": "{{ $json.supabaseRpcBody.filter_type }}"
}
```

### Solución 3: Verificar que la Función Existe y Tiene Permisos

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

-- Verificar permisos
GRANT EXECUTE ON FUNCTION public.search_similar_reports(vector, float, int, text, text) TO anon;
GRANT EXECUTE ON FUNCTION public.search_similar_reports(vector, float, int, text, text) TO authenticated;
GRANT EXECUTE ON FUNCTION public.search_similar_reports(vector, float, int, text, text) TO service_role;
```

### Solución 4: Usar Query Parameters en lugar de Body

Algunos usuarios reportan que usar query parameters funciona mejor:

**URL:**
```
https://eamsbroadstwkrkjcuvo.supabase.co/rest/v1/rpc/search_similar_reports?query_embedding=...
```

**Pero esto NO funciona para embeddings** porque son arrays grandes.

### Solución 5: Verificar que el Content-Type Está en los Headers

**CRÍTICO:** El header `Content-Type: application/json` DEBE estar en "Header Parameters", no solo en el campo "Content Type" del body.

**Verifica:**
1. En "HTTP Request2" → "Header Parameters"
2. Debe existir una entrada con:
   - **Name:** `Content-Type`
   - **Value:** `application/json`

Si no está, agrégalo.

### Solución 6: Probar con cURL Directo

Para verificar que la función funciona, prueba desde terminal:

```bash
curl -X POST 'https://eamsbroadstwkrkjcuvo.supabase.co/rest/v1/rpc/search_similar_reports' \
  -H 'apikey: TU_API_KEY' \
  -H 'Authorization: Bearer TU_SERVICE_ROLE_KEY' \
  -H 'Content-Type: application/json' \
  -H 'Prefer: return=representation' \
  -d '{
    "query_embedding": [0.1, 0.2, ...],
    "match_threshold": 0.7,
    "match_count": 10,
    "filter_species": "dog",
    "filter_type": "found"
  }'
```

Si esto funciona, el problema está en n8n. Si no funciona, el problema está en Supabase.

## Solución Recomendada para n8n

Basado en la búsqueda, el problema más común es que **n8n no está enviando el body correctamente en modo Raw**.

**Prueba esto:**

1. **En "HTTP Request2":**
   - **Send Body:** ON
   - **Body Content Type:** `Raw`
   - **Content Type (Header):** `application/json`
   - **Body:** `={{ $json.supabaseRpcBodyString }}`

2. **Asegúrate de que en "Header Parameters" también tengas:**
   - `Content-Type: application/json`

3. **Si no funciona, prueba con "JSON" en lugar de "Raw":**
   - **Body Content Type:** `JSON`
   - **Body:** Usa el objeto `$json.supabaseRpcBody` directamente

## Verificación Final

Después de hacer los cambios:

1. Abre DevTools (F12) → Network
2. Ejecuta el workflow
3. Busca la petición a `search_similar_reports`
4. Verifica el **Request Payload**
5. Verifica los **Request Headers**

Si el body está vacío o no se envía, el problema está en la configuración de n8n.
Si el body está presente pero Supabase dice "without parameters", el problema está en el formato o la función.









