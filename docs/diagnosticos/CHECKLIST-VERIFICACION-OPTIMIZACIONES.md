# ✅ Checklist de Verificación de Optimizaciones

## 📋 Estado Actual de los Servicios

Basándome en los logs que proporcionaste, aquí está el estado:

### 🟢 Cloudflared (Túnel)
- **Estado**: ✅ Activo
- **URL**: `https://named-determine-liabilities-promote.trycloudflare.com`
- **Líneas 1-174**: Túnel funcionando correctamente

### 🟢 Uvicorn (Backend)
- **Estado**: ✅ Activo
- **Puerto**: 8003
- **Líneas 1-263**: Servidor FastAPI corriendo

### 🟢 Node/Expo (Frontend)
- **Estado**: ✅ Activo
- **Líneas 11-808**: App React Native/Expo cargada

---

## 🔍 Qué Verificar en los Logs

### 1. Backend (Uvicorn) - Buscar estos mensajes:

#### ✅ **Optimizaciones Activas:**
```
✅ MegaDescriptor pre-cargado
🔍 Embedding generado: 2048 dimensiones
🧹 Memoria después: [número] MB
```

#### ❌ **Errores a Evitar:**
```
❌ Error generando embedding
❌ CUDA out of memory
❌ RuntimeError: CUDA error
❌ TimeoutError
```

### 2. Frontend (Node) - Buscar estos mensajes:

#### ✅ **Configuración Correcta:**
```
🔧 [BACKEND CONFIG]
   BACKEND_URL final: https://named-determine-liabilities-promote.trycloudflare.com
```

#### ❌ **Errores a Evitar:**
```
❌ API Error: Network request failed
❌ Error buscando coincidencias
❌ TypeError: Cannot read property
❌ AbortError
```

### 3. Cloudflared - Buscar estos mensajes:

#### ✅ **Túnel Saludable:**
```
INFO Connection registered
INFO Registered tunnel connection
```

#### ❌ **Problemas de Conexión:**
```
ERR Connection dropped
ERR Connection timeout
```

---

## 🧪 Tests Rápidos para Verificar

### Test 1: Verificar que el Backend Responde
```bash
curl https://named-determine-liabilities-promote.trycloudflare.com/health
```
**Esperado:** `{"status":"ok","message":"PetAlert API activa","supabase":"conectado"}`

### Test 2: Verificar Embeddings
```bash
curl -X GET https://named-determine-liabilities-promote.trycloudflare.com/fix-embeddings/check-missing
```
**Esperado:** Debe mostrar estadísticas de embeddings

### Test 3: Búsqueda de Prueba (desde la app)
1. Abre la pantalla de búsqueda con IA
2. Selecciona una imagen
3. Inicia búsqueda
4. **Observa los logs del backend**

**En Backend, deberías ver:**
```
🔄 Generando embedding...
🔍 Embedding generado: 2048 dimensiones
✅ Búsqueda completada
```

---

## 🔴 Indicadores de Problemas

### Problema 1: Backend No Optimizado
**Síntomas en logs:**
- No aparece mensaje de "MegaDescriptor pre-cargado"
- No hay logs de limpieza de memoria
- Uso de memoria aumenta con cada búsqueda

**Solución:**
```bash
# Reiniciar backend con código actualizado
cd backend
git pull  # o asegurarse que tiene los cambios
uvicorn main:app --reload --port 8003 --host 0.0.0.0
```

### Problema 2: Frontend Usa Código Antiguo
**Síntomas en logs:**
- Timeouts después de 30 segundos (no 90)
- No hay mensajes de reintentos
- Errores inmediatos sin esperar

**Solución:**
```bash
# En la terminal de Expo
# Presionar 'r' para reload
# O en el dispositivo: agitar → Reload
```

### Problema 3: Túnel Inestable
**Síntomas en logs:**
- `Connection dropped` frecuente
- `Registered tunnel connection` cada pocos segundos
- Requests intermitentes

**Solución:**
```bash
# Reiniciar cloudflared
# Ctrl+C para detener
cloudflared tunnel --url http://localhost:8003
# Actualizar .env con la nueva URL
```

---

## 📊 Monitoreo Durante Búsquedas

### En Backend (Uvicorn):
Busca esta secuencia para cada búsqueda:

```
INFO:     127.0.0.1:XXXXX - "POST /embeddings/search_image?top_k=10 HTTP/1.1" 200 OK
🔍 [direct-match] Buscando coincidencias para reporte XXXX
   Tipo base: lost, buscando: found
   Especie: dog
   Dimensiones embedding: 2048
   Candidatos encontrados: X
   ✅ Encontradas X coincidencias
```

### Tiempos Esperados:
- **Primera búsqueda**: 10-60 segundos (carga del modelo)
- **Búsquedas subsecuentes**: 5-15 segundos
- **Timeout máximo**: 90 segundos

### En Frontend (Node):
Busca esta secuencia:

```
🌐 API Request: POST https://named-determine-liabilities-promote.trycloudflare.com/embeddings/search_image
🔗 URL completa: https://...
✅ API Response: {...}
```

---

## ✅ Checklist de Verificación

Marca cada item después de verificarlo:

### Backend:
- [ ] Backend corriendo en puerto 8003
- [ ] Mensaje "MegaDescriptor pre-cargado" en startup
- [ ] Variable `GENERATE_EMBEDDINGS_LOCALLY=true` en .env
- [ ] Cloudflare tunnel conectado correctamente
- [ ] Health endpoint responde: `/health`

### Frontend:
- [ ] .env tiene la URL correcta de Cloudflare
- [ ] Console muestra URL final correcta
- [ ] No hay errores de importación (vision.js)
- [ ] Timeouts configurados en 90s (no 30s)

### Funcionalidad:
- [ ] Primera búsqueda completa (puede tardar 60s)
- [ ] Segunda búsqueda más rápida (~10s)
- [ ] Tercera búsqueda exitosa
- [ ] Cuarta búsqueda exitosa
- [ ] Quinta búsqueda exitosa
- [ ] **Sin crashes después de múltiples búsquedas** ✅

### Memoria:
- [ ] Uso de RAM constante en backend
- [ ] No aumenta con cada búsqueda
- [ ] GPU memory (si aplica) estable

---

## 🐛 Debugging Avanzado

### Si las búsquedas siguen fallando:

#### 1. Verificar versión del código
```bash
# En backend/services/embeddings.py debe haber:
grep -n "del img, img_tensor, feats" backend/services/embeddings.py
grep -n "_inference_semaphore" backend/services/embeddings.py
```

**Esperado:** Ambos comandos deben encontrar las líneas

#### 2. Verificar timeouts en frontend
```bash
# En src/services/searchImage.js debe haber:
grep -n "TIMEOUT_MS = 90000" src/services/searchImage.js
grep -n "MAX_RETRIES" src/services/searchImage.js
```

**Esperado:** Ambos comandos deben encontrar las líneas

#### 3. Ver uso de memoria en tiempo real
```bash
# Linux/Mac
watch -n 1 'ps aux | grep uvicorn'

# Windows PowerShell
while($true) { Get-Process python | Where-Object {$_.MainWindowTitle -eq ""} | Select-Object WS,CPU,Id; Start-Sleep 2; Clear-Host }
```

**Esperado:** Uso de memoria (WS) debe ser constante

---

## 📝 Log de Pruebas

Registra aquí los resultados de tus pruebas:

### Búsqueda 1:
- Tiempo: ___ segundos
- Resultado: ✅ / ❌
- Errores: ___

### Búsqueda 2:
- Tiempo: ___ segundos
- Resultado: ✅ / ❌
- Errores: ___

### Búsqueda 3:
- Tiempo: ___ segundos
- Resultado: ✅ / ❌
- Errores: ___

### Búsqueda 4:
- Tiempo: ___ segundos
- Resultado: ✅ / ❌
- Errores: ___

### Búsqueda 5:
- Tiempo: ___ segundos
- Resultado: ✅ / ❌
- Errores: ___

---

## 🎯 Siguiente Paso

**Si todos los checks pasan:** ✅ Las optimizaciones están funcionando correctamente!

**Si algunos fallan:** 
1. Identificar qué checks fallaron
2. Aplicar la solución correspondiente
3. Reiniciar servicios afectados
4. Volver a probar

---

## 📞 Soporte

Si después de verificar todo sigue habiendo problemas:

1. **Captura los logs** de las 3 terminales durante una búsqueda que falle
2. **Anota el mensaje de error** exacto
3. **Verifica** qué archivos fueron modificados vs. los originales
4. **Comparte** los logs completos

---

**Fecha de creación:** 2025-11-19  
**Estado:** 🔄 Pendiente de verificación


