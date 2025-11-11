# 🔧 Configuración Correcta de HTTP Request2

## Error Actual

```
Could not find the function public.search_similar_reports without parameters in the schema cache
```

## Causa

Supabase no está recibiendo los parámetros en el body. Esto significa que el body no se está enviando correctamente o está vacío.

## Configuración Paso a Paso

### Paso 1: Verificar Headers

En "HTTP Request2", asegúrate de tener estos headers:

```
Header Parameters:
├─ apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
├─ Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
├─ Content-Type: application/json  ← IMPORTANTE
└─ Prefer: return=representation
```

### Paso 2: Configurar Body (CRÍTICO)

1. **Send Body:** Toggle debe estar en **ON** (verde)
2. **Body Content Type:** Selecciona **`Raw`** (NO "JSON")
3. **Content Type (Header):** Déjalo **vacío** (si ya tienes Content-Type en Header Parameters)
4. **Body:** En el campo de texto grande, pega EXACTAMENTE esto:

```javascript
={{ JSON.stringify({
  "query_embedding": $json.body.embedding,
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": $json.body.report_data?.species || null,
  "filter_type": ($json.body.report_data?.type === 'lost') ? 'found' : 'lost'
}) }}
```

**IMPORTANTE:**
- Debe empezar con `={{` (sin espacios antes)
- Debe terminar con `}}` (sin espacios después)
- Todo debe estar en una sola expresión

### Paso 3: Verificar que el Embedding Existe

Antes de "HTTP Request2", agrega un nodo Code para verificar:

```javascript
// Verificar que el embedding existe
const debug = {
  hasBody: !!$json.body,
  hasEmbedding: !!$json.body?.embedding,
  embeddingType: typeof $json.body?.embedding,
  embeddingLength: $json.body?.embedding?.length,
  embeddingPreview: $json.body?.embedding?.slice(0, 5),
  reportDataType: $json.body?.report_data?.type,
  reportDataSpecies: $json.body?.report_data?.species
};

return {
  json: {
    ...$json,
    debug: debug
  }
};
```

Si el embedding no existe, el problema está en el nodo "Code in JavaScript1" que no está pasando el embedding correctamente.

## Verificación del Body que se Envía

Para ver qué se está enviando realmente, puedes:

1. **Abrir las DevTools del navegador** (F12)
2. **Ir a la pestaña Network**
3. **Ejecutar el nodo "HTTP Request2"**
4. **Buscar la petición a Supabase**
5. **Ver el Request Payload**

El payload debe verse así:

```json
{
  "query_embedding": [0.123, 0.456, ...],
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": "dog",
  "filter_type": "found"
}
```

## Si el Body Está Vacío

Si el body está vacío o no se envía, verifica:

1. **"Send Body" está en ON?** ← Verifica esto primero
2. **Hay un campo "Body" visible?** Si no, habilita "Send Body"
3. **El campo Body tiene contenido?** Debe tener la expresión JSON.stringify

## Solución Alternativa: Nodo Code Intermedio

Si el problema persiste, agrega un nodo Code antes de "HTTP Request2":

```javascript
// Construir el body para Supabase
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
    supabaseBody: bodyForSupabase,
    supabaseBodyString: JSON.stringify(bodyForSupabase)
  }
};
```

Luego en "HTTP Request2":
- Body Content Type: `Raw`
- Body: `={{ $json.supabaseBodyString }}`

Esto te asegura que el JSON se genera correctamente antes de enviarlo.











