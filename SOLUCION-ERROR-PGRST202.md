# 🔧 Solución: Error PGRST202 - "without parameters"

## Error

```
PGRST202: Could not find the function public.search_similar_reports without parameters 
in the schema cache
```

## Causa

Supabase **no está recibiendo los parámetros** en el body. Esto significa que el body está vacío o no se está enviando correctamente.

## Solución Paso a Paso

### Paso 1: Verificar que el Body se está Generando

En n8n, ejecuta el nodo **"Code in JavaScript4"** y verifica en el OUTPUT:

1. **¿Existe `TEST_supabaseRpcBodyString`?**
   - Si no existe: el problema está en "Code in JavaScript3"
   - Si existe: continúa

2. **¿Tiene contenido?**
   - `TEST_supabaseRpcBodyString_length` debe ser > 0
   - Si es 0 o null: el problema está en "Code in JavaScript3"

3. **¿Es un JSON válido?**
   - Debe verse así: `{"query_embedding":[...], "match_threshold":0.7, ...}`

### Paso 2: Verificar el Body en HTTP Request2

En el nodo "HTTP Request2":

1. **Baja hasta "Send Body"**
2. **Verifica que "Send Body" esté en ON** (verde)
3. **Body Content Type:** debe ser `Raw`
4. **Body:** debe ser `={{ $json.supabaseRpcBodyString }}`

**IMPORTANTE:** 
- Debe ser `={{` (un signo de igual, dos llaves)
- NO debe ser `=={{` (dos signos de igual)

### Paso 3: Verificar Headers

En "Header Parameters", asegúrate de tener:

1. **apikey**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`
2. **Authorization**: `eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...` (service_role)
3. **Content-Type**: `application/json` ← **CRÍTICO**
4. **Prefer**: `return=representation`

### Paso 4: Solución Alternativa - Construir Body Directamente en HTTP Request2

Si el problema persiste, construye el body directamente en "HTTP Request2":

1. **Body Content Type:** `Raw`
2. **Body:** Pega esto:

```javascript
={{ JSON.stringify({
  "query_embedding": $json.body?.embedding || $json.supabaseRpcBody?.query_embedding || [],
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": $json.body?.report_data?.species || $json.supabaseRpcBody?.filter_species || null,
  "filter_type": ($json.body?.report_data?.type === 'lost') ? 'found' : (($json.body?.report_data?.type === 'found') ? 'lost' : null)
}) }}
```

Esto asegura que el body se construya directamente sin depender de nodos intermedios.

### Paso 5: Verificar con DevTools

1. Abre **DevTools** (F12)
2. Ve a **Network**
3. Ejecuta el workflow
4. Busca la petición a `search_similar_reports`
5. Haz clic en ella
6. Ve a **Payload** o **Request**

**Verifica:**
- ¿Se está enviando un body?
- ¿El body tiene el formato correcto?
- ¿El Content-Type está en los headers?

## Solución: Verificar que la Función Existe

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
```

Si no existe, créala con este script:

```sql
CREATE OR REPLACE FUNCTION public.search_similar_reports(
    query_embedding vector(512),
    match_threshold float DEFAULT 0.7,
    match_count int DEFAULT 10,
    filter_species text DEFAULT NULL,
    filter_type text DEFAULT NULL
)
RETURNS TABLE (
    id uuid,
    similarity_score float,
    species text,
    type text,
    photos text[],
    description text,
    location jsonb,
    created_at timestamptz
) AS $$
BEGIN
    RETURN QUERY
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
        r.embedding IS NOT NULL
        AND r.status = 'active'
        AND (1 - (r.embedding <#> query_embedding)) >= match_threshold
        AND (filter_species IS NULL OR r.species = filter_species)
        AND (filter_type IS NULL OR r.type = filter_type)
    ORDER BY r.embedding <#> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;

-- Dar permisos
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO anon;
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO authenticated;
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO service_role;
```

## Checklist Final

- [ ] El nodo "Code in JavaScript3" genera `supabaseRpcBodyString`
- [ ] El nodo "Code in JavaScript4" muestra que `supabaseRpcBodyString` existe y tiene contenido
- [ ] El Body en "HTTP Request2" es `={{ $json.supabaseRpcBodyString }}` (sin `==`)
- [ ] El header `Content-Type: application/json` está en "Header Parameters"
- [ ] La función `search_similar_reports` existe en Supabase
- [ ] Los permisos de la función están correctos

## Próximo Paso

**Ejecuta el nodo "Code in JavaScript4" y comparte el OUTPUT completo.** Esto nos dirá exactamente qué está pasando con el body.









