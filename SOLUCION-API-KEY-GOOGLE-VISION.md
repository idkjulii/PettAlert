# 🔑 Solución: Error de API Key de Google Vision

## Error

```
Bad request - API key not valid. Please pass a valid API key.
```

## Causa

La API key de Google Vision en el workflow no es válida o ha expirado.

## Solución

### Paso 1: Verificar la API Key en el workflow

En el nodo "HTTP Request1", la URL es:
```
https://vision.googleapis.com/v1/images:annotate?key=aa1b417eeb81fc396c8d30559a03a5a2536b5e63
```

### Paso 2: Obtener una nueva API Key

1. **Ir a Google Cloud Console:**
   - https://console.cloud.google.com/

2. **Seleccionar o crear un proyecto**

3. **Habilitar Google Vision API:**
   - Ir a "APIs & Services" > "Library"
   - Buscar "Cloud Vision API"
   - Hacer clic en "Enable"

4. **Crear API Key:**
   - Ir a "APIs & Services" > "Credentials"
   - Clic en "Create Credentials" > "API Key"
   - Copiar la nueva API key

5. **Restringir la API Key (Recomendado):**
   - Clic en "Restrict Key"
   - En "API restrictions", seleccionar "Restrict key"
   - Elegir "Cloud Vision API"
   - Guardar

### Paso 3: Actualizar el workflow

En el nodo "HTTP Request1":

**Opción A: Actualizar la URL completa**
```
https://vision.googleapis.com/v1/images:annotate?key=TU_NUEVA_API_KEY_AQUI
```

**Opción B: Usar Query Parameters (mejor práctica)**

1. En "HTTP Request1":
   - **Send Query Parameters**: ON
   - **Query Parameters**:
     - Name: `key`
     - Value: `TU_NUEVA_API_KEY_AQUI`

2. **URL** (sin el `?key=`):
   ```
   https://vision.googleapis.com/v1/images:annotate
   ```

**Opción C: Usar Variable de Entorno (más seguro)**

1. En n8n, ir a Settings > Variables
2. Crear variable: `GOOGLE_VISION_API_KEY`
3. En el workflow, usar:
   ```
   https://vision.googleapis.com/v1/images:annotate?key={{ $env.GOOGLE_VISION_API_KEY }}
   ```

### Paso 4: Verificar que funciona

1. Ejecutar el nodo "HTTP Request1"
2. Debe retornar la respuesta de Google Vision con labels y colores

## Verificación de API Key

Puedes probar la API key directamente con curl:

```bash
curl -X POST \
  "https://vision.googleapis.com/v1/images:annotate?key=TU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "requests": [{
      "image": {
        "content": "/9j/4AAQSkZJRgABAQAAAQABAAD/2wBDAAYEBQYFBAYGBQYHBwYIChAKCgkJChQODwwQFxQYGBcUFhYaHSUfGhsjHBYWICwgIyYnKSopGR8tMC0oMCUoKSj/2wBDAQcHBwoIChMKChMoGhYaKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCgoKCj/wAARCAABAAEDASIAAhEBAxEB/8QAFQABAQAAAAAAAAAAAAAAAAAAAAv/xAAUEAEAAAAAAAAAAAAAAAAAAAAA/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAX/xAAUEQEAAAAAAAAAAAAAAAAAAAAA/9oADAMBAAIRAxEAPwCdABmX/9k="
      },
      "features": [{
        "type": "LABEL_DETECTION",
        "maxResults": 10
      }]
    }]
  }'
```

Si la API key es válida, deberías recibir una respuesta JSON con labels.

## Notas Importantes

1. **Límites de cuota:** Google Vision tiene límites gratuitos. Verifica tu cuota en Google Cloud Console.

2. **Facturación:** Asegúrate de tener facturación habilitada si planeas usar más allá del límite gratuito.

3. **Seguridad:** NO compartas tu API key públicamente. Usa variables de entorno o restricciones.

4. **Costo:** Los primeros 1,000 requests/mes son gratuitos, después cobran por uso.

## Si la API Key sigue sin funcionar

1. Verifica que la API key tenga permisos para Cloud Vision API
2. Verifica que la facturación esté habilitada en Google Cloud
3. Verifica que no haya restricciones de IP que bloqueen n8n
4. Revisa los logs en Google Cloud Console para ver errores específicos









