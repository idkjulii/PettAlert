# 🔧 Solución: Error "Empty or invalid json" en HTTP Request2

## Error

```
Bad request - please check your parameters
Empty or invalid json
```

## Causa

El header `Content-Type` está configurado como `text/html` en lugar de `application/json`. Esto hace que Supabase no pueda parsear el JSON correctamente.

## Solución

En el nodo "HTTP Request2":

### Paso 1: Verificar Headers

En la sección **"Header Parameters"**, asegúrate de tener:

1. **Name:** `Content-Type`
2. **Value:** `application/json` (NO `text/html`)

### Paso 2: Verificar Content Type (Header)

Si hay un campo separado **"Content Type (Header)"** o **"Content Type"** (fuera de Header Parameters):

- **Déjalo vacío** O
- **Configúralo como:** `application/json`

### Paso 3: Verificar el Body

El body debe estar configurado así:

- **Body Content Type:** `Raw`
- **Body:** 
```javascript
={{ JSON.stringify({
  "query_embedding": $json.body.embedding,
  "match_threshold": 0.7,
  "match_count": 10,
  "filter_species": $json.body.report_data?.species || null,
  "filter_type": ($json.body.report_data?.type === 'lost') ? 'found' : 'lost'
}) }}
```

## Configuración Correcta Completa

```
HTTP Request2:
├─ Method: POST
├─ URL: https://eamsbroadstwkrkjcuvo.supabase.co/rest/v1/rpc/search_similar_reports
├─ Send Headers: ON
├─ Header Parameters:
│  ├─ Name: apikey
│  │  Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
│  ├─ Name: Authorization
│  │  Value: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
│  ├─ Name: Content-Type          ← IMPORTANTE
│  │  Value: application/json     ← Debe ser application/json
│  └─ Name: Prefer
│     Value: return=representation
├─ Send Body: ON
├─ Body Content Type: Raw
├─ Content Type (Header): [vacío] o application/json  ← Verificar esto
└─ Body: ={{ JSON.stringify({...}) }}
```

## Verificación

Después de cambiar el Content-Type a `application/json`:

1. **Ejecuta el nodo "HTTP Request2"** manualmente
2. **Verifica el Output:** Debe retornar los matches de Supabase
3. **Si sigue dando error:** Revisa que el embedding esté en el formato correcto (array de números)

## Nota Importante

Si hay **dos campos** de Content-Type:
- Uno en "Header Parameters" → debe ser `application/json`
- Otro campo separado "Content Type" → déjalo vacío o también `application/json`

El campo separado puede estar sobrescribiendo el header correcto.











