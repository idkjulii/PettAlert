# 🔍 Debugging: Error RPC Supabase "without parameters"

## Error Persistente

```
Could not find the function public.search_similar_reports without parameters in the schema cache
```

## Diagnóstico

Este error significa que Supabase **NO está recibiendo los parámetros** en el body. Aunque el body esté configurado, algo está mal.

## Checklist de Verificación

### 1. Verificar Headers Completos

En "HTTP Request2", asegúrate de tener **TODOS** estos headers:

```
Header Parameters:
├─ apikey: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
├─ Authorization: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
├─ Content-Type: application/json  ← DEBE ESTAR AQUÍ
└─ Prefer: return=representation
```

**IMPORTANTE:** El header `Content-Type: application/json` DEBE estar en "Header Parameters", no solo en el campo "Content Type" del body.

### 2. Verificar Body

El body debe estar así:

```
Body Content Type: Raw
Content Type: [vacío] o application/json
Body: ={{ JSON.stringify({...}) }}
```

### 3. Verificar que el Embedding Existe

Agrega un nodo Code ANTES de "HTTP Request2" para verificar:

```javascript
// Verificar datos antes de enviar a Supabase
const debug = {
  hasBody: !!$json.body,
  hasEmbedding: !!$json.body?.embedding,
  embeddingType: typeof $json.body?.embedding,
  isArray: Array.isArray($json.body?.embedding),
  embeddingLength: $json.body?.embedding?.length,
  embeddingPreview: $json.body?.embedding?.slice(0, 3),
  reportDataType: $json.body?.report_data?.type,
  reportDataSpecies: $json.body?.report_data?.species,
  allKeys: Object.keys($json.body || {})
};

// Construir el body para Supabase
const bodyForSupabase = {
  query_embedding: $json.body?.embedding,
  match_threshold: 0.7,
  match_count: 10,
  filter_species: $json.body?.report_data?.species || null,
  filter_type: ($json.body?.report_data?.type === 'lost') ? 'found' : 'lost'
};

const bodyString = JSON.stringify(bodyForSupabase);

return {
  json: {
    ...$json,
    debug: debug,
    supabaseBody: bodyForSupabase,
    supabaseBodyString: bodyString,
    bodyStringLength: bodyString.length,
    bodyStringPreview: bodyString.substring(0, 200)
  }
};
```

Luego en "HTTP Request2":
- Body: `={{ $json.supabaseBodyString }}`

### 4. Verificar en DevTools del Navegador

1. Abre las **DevTools** (F12)
2. Ve a la pestaña **Network**
3. Ejecuta el nodo "HTTP Request2"
4. Busca la petición a `search_similar_reports`
5. Haz clic en ella
6. Ve a la pestaña **Payload** o **Request**

**Verifica:**
- ¿Se está enviando un body?
- ¿El body tiene el formato correcto?
- ¿El Content-Type está en los headers?

## Solución: Verificar Headers

El problema más común es que falta el header `Content-Type` en "Header Parameters".

**Asegúrate de tener:**
1. `apikey` en Header Parameters
2. `Authorization` en Header Parameters  
3. `Content-Type: application/json` en Header Parameters ← **VERIFICAR ESTO**
4. `Prefer: return=representation` en Header Parameters

## Solución Alternativa: Probar desde el Backend

Si n8n sigue sin funcionar, puedes probar desde el backend directamente:

```python
# En backend/routers/rag_search.py ya existe un endpoint
# POST /rag/search
# Que llama a la misma función RPC
```

Esto te permitirá verificar que la función RPC funciona correctamente.

## Debugging con Nodo Code

Agrega este nodo Code ANTES de "HTTP Request2":

```javascript
// Log completo para debugging
console.log('=== DEBUG HTTP Request2 ===');
console.log('Body exists:', !!$json.body);
console.log('Embedding exists:', !!$json.body?.embedding);
console.log('Embedding length:', $json.body?.embedding?.length);
console.log('Report data:', $json.body?.report_data);

const body = {
  query_embedding: $json.body?.embedding || [],
  match_threshold: 0.7,
  match_count: 10,
  filter_species: $json.body?.report_data?.species || null,
  filter_type: ($json.body?.report_data?.type === 'lost') ? 'found' : 'lost'
};

console.log('Body to send:', JSON.stringify(body).substring(0, 200));

return {
  json: {
    ...$json,
    bodyForSupabase: body
  }
};
```

Luego en "HTTP Request2", usa:
- Body: `={{ JSON.stringify($json.bodyForSupabase) }}`

Esto te ayudará a ver exactamente qué se está enviando.











