# 🔧 Solución: Error Base64 en Google Vision API (n8n)

## Error

```
Bad request - Invalid value at 'requests[0].image.content' (TYPE_BYTES), 
Base64 decoding failed for "=/9j/4AAQ..."
```

El Base64 está empezando con `=` lo cual causa el error.

## Causa

El problema está en cómo se construye el JSON body en el nodo "HTTP Request1". Cuando usas `"={{ $json.imageBase64 }}"` dentro de un string JSON, n8n puede estar agregando un `=` extra o el Base64 puede tener caracteres especiales.

## Solución

### Opción 1: Usar expresiones de n8n correctamente (Recomendado)

En el nodo **"HTTP Request1"**, en el campo **JSON Body**, cambia de:

```json
={
  "requests": [{
    "image": {
      "content": "={{ $json.imageBase64 }}"
    },
    "features": [
      {"type": "LABEL_DETECTION", "maxResults": 10},
      {"type": "IMAGE_PROPERTIES"}
    ]
  }]
}
```

A:

```json
={{ JSON.stringify({
  "requests": [{
    "image": {
      "content": $json.imageBase64
    },
    "features": [
      {"type": "LABEL_DETECTION", "maxResults": 10},
      {"type": "IMAGE_PROPERTIES"}
    ]
  }]
}) }}
```

### Opción 2: Limpiar el Base64 antes de usarlo

En el nodo **"Code in JavaScript"** (el que convierte a Base64), asegúrate de que el Base64 esté limpio:

```javascript
const binaryData = $input.first().binary.data;
let base64Image = binaryData.data.toString('base64');

// Limpiar el Base64 (remover espacios, saltos de línea, etc.)
base64Image = base64Image.replace(/\s/g, '');

// Asegurarse de que no empiece con "="
if (base64Image.startsWith('=')) {
  base64Image = base64Image.substring(1);
}

return {
  json: {
    imageBase64: base64Image,
    originalBody: $input.first().json.body
  },
  binary: { data: binaryData }
};
```

### Opción 3: Usar el modo "Using JSON" con expresiones

En el nodo **"HTTP Request1"**:

1. **Body Content Type**: `JSON`
2. **Specify Body**: `Using JSON`
3. En el campo JSON, usa:

```json
{
  "requests": [
    {
      "image": {
        "content": "={{ $json.imageBase64 }}"
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
    }
  ]
}
```

**IMPORTANTE**: Asegúrate de que el campo JSON Body tenga el formato correcto. Si usas `"content": "={{ $json.imageBase64 }}"`, el Base64 debe estar en `$json.imageBase64` sin caracteres extra.

## Verificación

Para verificar que el Base64 está correcto, agrega un nodo **Code** después de "Code in JavaScript" para inspeccionar:

```javascript
const base64 = $json.imageBase64;

// Verificar que no empiece con "="
if (base64.startsWith('=')) {
  return {
    json: {
      error: "Base64 starts with =",
      firstChars: base64.substring(0, 20),
      length: base64.length
    }
  };
}

// Verificar formato Base64 válido
const base64Regex = /^[A-Za-z0-9+/]*={0,2}$/;
if (!base64Regex.test(base64)) {
  return {
    json: {
      error: "Invalid Base64 format",
      firstChars: base64.substring(0, 20)
    }
  };
}

return {
  json: {
    success: true,
    base64Length: base64.length,
    firstChars: base64.substring(0, 20)
  }
};
```

## Código Corregido Completo para "Code in JavaScript"

```javascript
const binaryData = $input.first().binary.data;

// Convertir a Base64
let base64Image = binaryData.data.toString('base64');

// Limpiar el Base64
base64Image = base64Image.trim().replace(/\s/g, '');

// Verificar que no empiece con "="
if (base64Image.startsWith('=')) {
  base64Image = base64Image.substring(1);
}

return {
  json: {
    imageBase64: base64Image,
    originalBody: $input.first().json.body || $input.first().json
  }
};
```

## JSON Body Corregido para "HTTP Request1"

Si usas el modo "Using JSON", usa esto:

```json
{
  "requests": [
    {
      "image": {
        "content": "={{ $json.imageBase64 }}"
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
    }
  ]
}
```

O si prefieres usar expresiones directas (sin comillas en el content):

```json
={{ 
JSON.stringify({
  "requests": [{
    "image": {
      "content": $json.imageBase64
    },
    "features": [
      {"type": "LABEL_DETECTION", "maxResults": 10},
      {"type": "IMAGE_PROPERTIES"}
    ]
  }]
})
}}
```

## Prueba

Después de hacer los cambios:

1. Guarda el workflow
2. Ejecuta el nodo "HTTP Request1" manualmente
3. Verifica que el Base64 se envíe correctamente
4. Revisa la respuesta de Google Vision









