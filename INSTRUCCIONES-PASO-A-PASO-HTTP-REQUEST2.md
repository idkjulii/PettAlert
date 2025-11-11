# 📋 Instrucciones Paso a Paso: Configurar HTTP Request2

## Error Actual
"JSON parameter needs to be valid JSON"

Esto significa que estás en modo "JSON" y el JSON está mal formado.

## Solución: Cambiar a Modo Raw

### Paso 1: Abrir el Nodo HTTP Request2
1. Haz clic en el nodo "HTTP Request2" en tu workflow

### Paso 2: Ir a la Pestaña "Parameters"
1. Asegúrate de estar en la pestaña "Parameters" (no "Settings")

### Paso 3: Encontrar "Send Body"
1. Baja hasta encontrar la sección "Send Body"
2. Verifica que el toggle esté en **ON** (verde)

### Paso 4: Cambiar "Body Content Type"
1. Busca el campo "Body Content Type"
2. Actualmente debe decir "JSON"
3. **Cambia** a **"Raw"** (selecciona "Raw" del dropdown)

### Paso 5: Configurar "Content Type"
1. Busca el campo "Content Type" (debe estar cerca de "Body Content Type")
2. Escribe: `application/json`

### Paso 6: Limpiar y Configurar el Campo "Body"
1. Busca el campo grande "Body" (texto grande)
2. **BORRA TODO** el contenido actual
3. **Pega exactamente esto** (sin espacios antes o después):

```
={{ $json.supabaseRpcBodyString }}
```

### Paso 7: Verificar Headers
1. Busca "Header Parameters" (debe estar antes de "Send Body")
2. Verifica que tengas estos headers:
   - `apikey`: [tu api key]
   - `Authorization`: [tu service role key]
   - `Content-Type`: `application/json`
   - `Prefer`: `return=representation`

### Paso 8: Guardar y Probar
1. Haz clic fuera del nodo para guardar
2. Haz clic en "Execute step" (botón rojo arriba a la derecha)

## Verificación Visual

Después de configurar, deberías ver:

```
┌─────────────────────────────────┐
│ HTTP Request2                   │
├─────────────────────────────────┤
│ Send Body: ON ✅                │
│ Body Content Type: Raw ✅       │
│ Content Type: application/json ✅│
│ Body: ={{ $json.supabaseRpcBodyString }} ✅
└─────────────────────────────────┘
```

## Si Sigue Fallando

1. **Verifica que "Code in JavaScript3" esté generando `supabaseRpcBodyString`:**
   - Ejecuta el nodo "Code in JavaScript3"
   - Verifica que en el OUTPUT exista `supabaseRpcBodyString`

2. **Verifica que el Body Content Type sea "Raw":**
   - NO debe decir "JSON"
   - DEBE decir "Raw"

3. **Verifica que el Body tenga exactamente:**
   - `={{ $json.supabaseRpcBodyString }}`
   - Sin espacios extra
   - Sin comillas adicionales
   - Sin `JSON.stringify()` adicional











