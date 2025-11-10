# 🔍 Debugging: Error PGRST202 en Supabase RPC

## Error Actual

```
PGRST202: Could not find the function public.search_similar_reports without parameters 
in the schema cache
```

## Análisis del Error

Este error de Supabase (PostgREST) indica que:
1. **La función existe** pero no se está llamando con los parámetros correctos
2. **El body no se está enviando** o está vacío
3. **El formato del body es incorrecto** para Supabase RPC

## Verificación Paso a Paso

### 1. Verificar que la función existe en Supabase

Ejecuta en el SQL Editor de Supabase:

```sql
SELECT 
    p.proname as function_name,
    pg_get_function_arguments(p.oid) as arguments,
    pg_get_functiondef(p.oid) as definition
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public' 
AND p.proname = 'search_similar_reports';
```

Deberías ver la función con sus parámetros:
- `query_embedding vector(512)`
- `match_threshold float`
- `match_count int`
- `filter_species text`
- `filter_type text`

### 2. Verificar el Body que se está enviando

En n8n, ejecuta el nodo **"Code in JavaScript4"** y verifica:

1. **¿Existe `supabaseRpcBodyString`?**
   - Debe existir en el OUTPUT
   - Debe ser un string (no null/undefined)

2. **¿Tiene contenido?**
   - `TEST_supabaseRpcBodyString_length` debe ser > 0
   - Debe ser un JSON válido

3. **¿El formato es correcto?**
   - Debe verse así: `{"query_embedding":[...], "match_threshold":0.7, ...}`

### 3. Verificar Headers en HTTP Request2

Asegúrate de tener:
- ✅ `apikey`
- ✅ `Authorization: Bearer ...` (service_role)
- ✅ `Content-Type: application/json`
- ✅ `Prefer: return=representation`

### 4. Verificar el Body en HTTP Request2

El campo "Body" debe tener:
```
={{ $json.supabaseRpcBodyString }}
```

**NO debe tener:**
- `=={{` (dos signos de igual)
- Espacios antes o después
- `JSON.stringify()` adicional (ya está en Code in JavaScript3)

## Solución: Verificar con DevTools

### Opción 1: Ver el Request en n8n

1. Abre las **DevTools** del navegador (F12)
2. Ve a la pestaña **Network**
3. Ejecuta el workflow
4. Busca la petición a `search_similar_reports`
5. Haz clic en ella
6. Ve a la pestaña **Payload** o **Request**

**Verifica:**
- ¿Se está enviando un body?
- ¿El body tiene el formato correcto?
- ¿El Content-Type está en los headers?

### Opción 2: Agregar Logging

Agrega un nodo Code ANTES de "HTTP Request2" para loggear:

```javascript
// Log completo del body
console.log('=== BODY PARA SUPABASE ===');
console.log('supabaseRpcBodyString:', $json.supabaseRpcBodyString);
console.log('supabaseRpcBody:', $json.supabaseRpcBody);
console.log('Length:', $json.supabaseRpcBodyString?.length);

// Verificar que el embedding existe
if ($json.supabaseRpcBody?.query_embedding) {
  console.log('Embedding length:', $json.supabaseRpcBody.query_embedding.length);
  console.log('Embedding preview:', $json.supabaseRpcBody.query_embedding.slice(0, 5));
} else {
  console.error('❌ NO HAY EMBEDDING!');
}

return {
  json: {
    ...$json,
    // Mantener los datos originales
  }
};
```

## Solución Alternativa: Usar JSON Body en lugar de Raw

Si el modo Raw no funciona, prueba usar "Using JSON":

1. En "HTTP Request2":
   - **Body Content Type**: Cambia de "Raw" a **"JSON"**
   - **Body**: Usa el objeto directamente:

```json
{
  "query_embedding": {{ $json.supabaseRpcBody.query_embedding }},
  "match_threshold": {{ $json.supabaseRpcBody.match_threshold }},
  "match_count": {{ $json.supabaseRpcBody.match_count }},
  "filter_species": {{ $json.supabaseRpcBody.filter_species }},
  "filter_type": {{ $json.supabaseRpcBody.filter_type }}
}
```

## Solución: Verificar Permisos de la Función

Ejecuta en Supabase SQL Editor:

```sql
-- Verificar permisos
SELECT 
    p.proname as function_name,
    n.nspname as schema,
    CASE 
        WHEN has_function_privilege('anon', 'public.search_similar_reports(vector, float, int, text, text)', 'EXECUTE') 
        THEN 'YES' 
        ELSE 'NO' 
    END as anon_can_execute,
    CASE 
        WHEN has_function_privilege('authenticated', 'public.search_similar_reports(vector, float, int, text, text)', 'EXECUTE') 
        THEN 'YES' 
        ELSE 'NO' 
    END as authenticated_can_execute,
    CASE 
        WHEN has_function_privilege('service_role', 'public.search_similar_reports(vector, float, int, text, text)', 'EXECUTE') 
        THEN 'YES' 
        ELSE 'NO' 
    END as service_role_can_execute
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public' 
AND p.proname = 'search_similar_reports';
```

## Checklist Final

- [ ] La función existe en Supabase
- [ ] La función tiene los parámetros correctos
- [ ] Los permisos están correctos (EXECUTE para anon/service_role)
- [ ] El nodo "Code in JavaScript3" genera `supabaseRpcBodyString`
- [ ] El nodo "Code in JavaScript4" muestra que `supabaseRpcBodyString` existe
- [ ] El Body en "HTTP Request2" es `={{ $json.supabaseRpcBodyString }}` (sin `==`)
- [ ] El header `Content-Type: application/json` está configurado
- [ ] El header `Authorization` usa service_role key

## Próximo Paso

**Ejecuta el nodo "Code in JavaScript4" y comparte el OUTPUT completo.** Esto nos dirá si el problema está en:
1. La generación del body (Code in JavaScript3)
2. El envío del body (HTTP Request2)
3. La función en Supabase (permisos o definición)









