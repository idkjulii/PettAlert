# ✅ Verificación de Permisos RPC en Supabase

## Comandos a Ejecutar

Ejecuta estos comandos en el **SQL Editor de Supabase**:

```sql
-- Dar permisos a la función RPC
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO anon;
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO authenticated;
GRANT EXECUTE ON FUNCTION public.search_similar_reports TO service_role;
```

## Verificación

Después de ejecutar los comandos, verifica que funcionaron:

### 1. Verificar que la función existe

```sql
SELECT 
    p.proname as function_name,
    pg_get_function_arguments(p.oid) as arguments
FROM pg_proc p
JOIN pg_namespace n ON p.pronamespace = n.oid
WHERE n.nspname = 'public' 
AND p.proname = 'search_similar_reports';
```

Deberías ver:
```
function_name: search_similar_reports
arguments: query_embedding vector, match_threshold double precision DEFAULT 0.7, match_count integer DEFAULT 10, filter_species text DEFAULT NULL::text, filter_type text DEFAULT NULL::text
```

### 2. Verificar permisos

```sql
SELECT 
    proname as function_name,
    proacl as permissions
FROM pg_proc 
WHERE proname = 'search_similar_reports';
```

### 3. Probar la función directamente

```sql
-- Obtener un embedding de prueba
SELECT embedding FROM reports WHERE embedding IS NOT NULL LIMIT 1;
```

Luego prueba la función:

```sql
SELECT * FROM search_similar_reports(
  query_embedding := (SELECT embedding FROM reports WHERE embedding IS NOT NULL LIMIT 1),
  match_threshold := 0.7,
  match_count := 5,
  filter_species := 'dog',
  filter_type := 'found'
) LIMIT 5;
```

Si esto funciona, la función está correctamente configurada.

## Después de Ejecutar los Permisos

1. **Ejecuta los comandos GRANT** en Supabase SQL Editor
2. **Verifica que no haya errores**
3. **Prueba el nodo "HTTP Request2" en n8n** de nuevo
4. **Debería funcionar correctamente**

## Si Sigue Dando Error

Si después de dar permisos sigue dando error, verifica:

1. **Formato del Body:** Asegúrate de usar modo Raw con JSON.stringify()
2. **Headers:** Content-Type debe ser application/json
3. **Embedding:** Debe ser un array de 512 números
4. **URL:** Debe ser exactamente `https://eamsbroadstwkrkjcuvo.supabase.co/rest/v1/rpc/search_similar_reports`











