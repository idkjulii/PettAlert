# ✅ Solución Definitiva: Error Base64 en Google Vision (n8n)

## El Problema

El error `Base64 decoding failed for "=/9j/4AAQ..."` ocurre porque cuando usas:
```json
"content": "={{ $json.imageBase64 }}"
```

n8n está tratando la expresión como un **string literal** en lugar de evaluarla, resultando en que el Base64 se envía con caracteres extra.

## Solución Definitiva: Opción 1 Mejorada

En el nodo **"HTTP Request1"**, cambia completamente el campo **JSON Body**:

### Paso 1: Cambiar el modo de especificar el body

En "HTTP Request1":
1. **Body Content Type**: `JSON`
2. **Specify Body**: Cambia a **"Using Fields Below"** (NO "Using JSON")
3. En el campo que aparece, usa:

```json
={{ JSON.stringify({
  "requests": [{
    "image": {
      "content": $json.imageBase64
    },
    "features": [
      {
        "type": "LABEL_DETECTION",
        "maxResults": 10
      },
      {
        "type": "IMAGE_PROPERTIES"
      }
    ]
  }]
}) }}
```

**IMPORTANTE**: 
- `$json.imageBase64` **SIN comillas**
- Todo envuelto en `JSON.stringify()`
- El campo debe empezar con `={{` y terminar con `}}`

### Paso 2: Alternativa si "Using Fields Below" no funciona

Si el modo anterior no funciona, usa esta configuración:

1. **Body Content Type**: `Raw`
2. **Specify Body**: `Using Fields Below`
3. En el campo de texto, pega:

```json
={{ JSON.stringify({
  "requests": [{
    "image": {
      "content": $json.imageBase64
    },
    "features": [
      {
        "type": "LABEL_DETECTION",
        "maxResults": 10
      },
      {
        "type": "IMAGE_PROPERTIES"
      }
    ]
  }]
}) }}
```

4. **Headers**: Agrega manualmente:
   - `Content-Type`: `application/json`

## Solución Alternativa: Usar un nodo Code antes

Si las opciones anteriores no funcionan, agrega un nodo **Code** entre "Code in JavaScript" y "HTTP Request1":

### Nuevo nodo "Code" (antes de HTTP Request1):

```javascript
// Obtener el Base64 del nodo anterior
const base64Image = $json.imageBase64;

// Construir el objeto completo para Google Vision
const requestBody = {
  "requests": [{
    "image": {
      "content": base64Image
    },
    "features": [
      {
        "type": "LABEL_DETECTION",
        "maxResults": 10
      },
      {
        "type": "IMAGE_PROPERTIES"
      }
    ]
  }]
};

return {
  json: {
    requestBody: requestBody,
    originalBody: $json.originalBody
  }
};
```

### Luego en "HTTP Request1":

1. **Body Content Type**: `JSON`
2. **Specify Body**: `Using JSON`
3. En el campo JSON, usa:

```json
={{ $json.requestBody }}
```

## Verificación

Después de aplicar la solución:

1. **Ejecuta manualmente** el nodo "HTTP Request1"
2. **Verifica el Output**: Debe mostrar la respuesta de Google Vision con labels y colores
3. **Revisa el error**: Si persiste, verifica que el Base64 no tenga caracteres extra

## Código de Verificación (opcional)

Puedes agregar un nodo Code antes de "HTTP Request1" para verificar el Base64:

```javascript
const base64 = $json.imageBase64;

// Verificar formato
const checks = {
  startsWithEquals: base64.startsWith('='),
  startsWithSlash: base64.startsWith('/'),
  length: base64.length,
  firstChars: base64.substring(0, 30),
  isValidBase64: /^[A-Za-z0-9+/]*={0,2}$/.test(base64)
};

return {
  json: {
    ...checks,
    base64: base64.substring(0, 50) + '...'
  }
};
```

El Base64 válido debe:
- ✅ Empezar con `/` (para JPEG: `/9j/4AAQ...`)
- ✅ NO empezar con `=`
- ✅ Tener solo caracteres A-Z, a-z, 0-9, +, /, y = al final (padding)









