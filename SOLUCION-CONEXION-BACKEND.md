# 🔧 Solución: Error de Conexión con Backend

## Problema Identificado

La app móvil está intentando conectarse a `https://neighbourly-minaciously-audry.ngrok-free.dev` pero recibe error 404 (HTML en lugar de JSON).

## ✅ Solución Aplicada

He actualizado la configuración para **priorizar la IP local** sobre ngrok.

### Cambio realizado:

**Archivo:** `src/config/backend.js`

**Antes:**
```javascript
const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL || NGROK_URL || NETWORK_CONFIG?.BACKEND_URL || 'http://127.0.0.1:8003';
```

**Ahora:**
```javascript
const BACKEND_URL = process.env.EXPO_PUBLIC_BACKEND_URL || NETWORK_CONFIG?.BACKEND_URL || NGROK_URL || 'http://127.0.0.1:8003';
```

Ahora la prioridad es:
1. Variable de entorno `EXPO_PUBLIC_BACKEND_URL` (si existe)
2. **IP local** (`http://192.168.0.204:8003`) ← **Prioridad**
3. ngrok (fallback)
4. localhost (último recurso)

---

## 🔍 Verificación

### 1. Verificar que el backend esté accesible desde la IP local

```powershell
Invoke-WebRequest -Uri "http://192.168.0.204:8003/health" -Method GET
```

Debería devolver:
```json
{"status":"ok","message":"PetAlert Vision API activa",...}
```

### 2. Verificar que el backend esté escuchando en todas las interfaces

El backend debe iniciarse con `--host 0.0.0.0` para ser accesible desde la red local:

```powershell
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

### 3. Reiniciar la app móvil

Después de cambiar la configuración, necesitas reiniciar la app móvil (Expo) para que cargue los nuevos cambios.

---

## 📱 Próximos Pasos

1. **Reinicia la app móvil** (Expo)
2. **Intenta crear un reporte nuevamente**
3. **Verifica en los logs** que ahora use `http://192.168.0.204:8003`
4. **Verifica en los logs del backend** que reciba la petición

---

## 🎯 Flujo Actualizado

Cuando crees un reporte ahora:

```
1. App intenta crear reporte → Backend (http://192.168.0.204:8003/reports)
   ↓
2. Backend guarda en Supabase
   ↓
3. Backend genera embedding automáticamente
   ↓
4. Backend envía automáticamente al webhook de n8n ✅
   ↓
5. n8n procesa la imagen
   ↓
6. n8n envía resultados al backend
   ↓
7. Backend actualiza el reporte con labels y colores
```

---

## ⚠️ Si el Backend No Está Accesible

Si el backend sigue sin estar accesible, verifica:

1. **Backend corriendo:**
   ```powershell
   Invoke-WebRequest -Uri "http://127.0.0.1:8003/health" -Method GET
   ```

2. **Backend escuchando en 0.0.0.0:**
   - Debe iniciarse con `--host 0.0.0.0`
   - No solo `--host 127.0.0.1`

3. **Firewall de Windows:**
   - Asegúrate de que el puerto 8003 esté permitido
   - O desactiva temporalmente el firewall para pruebas

4. **Misma red WiFi:**
   - El dispositivo móvil y la computadora deben estar en la misma red WiFi

---

## 🔄 Alternativa: Usar Variable de Entorno

Si quieres forzar una URL específica, crea un archivo `.env` en la raíz del proyecto:

```env
EXPO_PUBLIC_BACKEND_URL=http://192.168.0.204:8003
```

Esto tendrá la máxima prioridad sobre todas las demás configuraciones.









