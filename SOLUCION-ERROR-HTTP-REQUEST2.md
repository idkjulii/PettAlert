# 🔧 Solución: Error "invalid syntax" en HTTP Request2

## Error

```
invalid syntax
```

## Causa

El nodo "HTTP Request2" está usando expresiones de n8n dentro de un JSON string, lo que genera un JSON inválido cuando se evalúa.

**Problema actual:**
```json
{
  "query_embedding": {{ $json.body.embedding }},  // ❌ Esto genera JSON inválido
  "filter_species": "{{ $json.body.report_data?.species }}"
}
```

Cuando n8n evalúa `{{ $json.body.embedding }}`, si es un array, lo convierte directamente sin comillas, generando JSON inválido.

## Solución

### Opción 1: Usar modo Raw con JSON.stringify() (Recomendado)

En el nodo "HTTP Request2":

1. **Body Content Type:** Cambia a `Raw`
2. **Body:** Usa esta expresión:

```javascript
={{ JSON.stringify({
  "query_embedding": $json.body.embedding,
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": $json.body.report_data?.species || null,
  "filter_type": ($json.body.report_data?.type === 'lost' || $json.body.report_data?.type === 'lost') ? 'found' : 'lost'
}) }}
```

3. **Headers:** Asegúrate de tener `Content-Type: application/json`

### Opción 2: Construir el JSON en un nodo Code antes

Agrega un nodo Code antes de "HTTP Request2":

```javascript
// Construir el body para Supabase RPC
const body = {
  query_embedding: $json.body.embedding,
  match_threshold: 0.7,
  match_count: 10,
  filter_species: $json.body.report_data?.species || null,
  filter_type: ($json.body.report_data?.type === 'lost') ? 'found' : 'lost'
};

return {
  json: {
    ...$json,
    supabaseBody: body
  }
};
```

Luego en "HTTP Request2":
- Body Content Type: `JSON`
- Specify Body: `Using JSON`
- JSON Body: `={{ $json.supabaseBody }}`

## Solución Recomendada (Opción 1)

**Cambia la configuración de "HTTP Request2":**

1. **Send Body:** ON
2. **Body Content Type:** `Raw` (cambiar de JSON a Raw)
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

4. **Headers:** Asegúrate de tener:
   - `Content-Type: application/json`
   - `apikey: ...`
   - `Authorization: ...`
   - `Prefer: return=representation`

Esto generará un JSON válido que Supabase puede procesar correctamente.











