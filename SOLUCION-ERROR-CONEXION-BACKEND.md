# 🔧 Solución: Error de Conexión al Backend

## ❌ Error
```
API Error: https://publications-publishers-calculations-act.trycloudflare.com/reports/ 
TypeError: Network request failed
```

## 🔍 Causa
El túnel de Cloudflare hardcodeado en la configuración ya no está activo. Los túneles temporales se cierran cuando detienes el servicio.

## ✅ Solución

### 1. Iniciar el Backend

Primero, asegúrate de que el backend esté corriendo:

```bash
cd backend
uvicorn main:app --reload --port 8003
```

Deberías ver:
```
INFO:     Uvicorn running on http://127.0.0.1:8003
```

### 2. Configurar la URL del Backend

Tienes **3 opciones** según tu caso:

#### **Opción A: Desarrollo en el mismo dispositivo** (Emulador en PC)
Crear archivo `.env` en la raíz del proyecto:

```env
EXPO_PUBLIC_BACKEND_URL=http://127.0.0.1:8003
```

#### **Opción B: Desarrollo en dispositivo físico** (Celular real en misma red WiFi)

1. **Obtén tu IP local:**
   - Windows: `ipconfig` → busca "IPv4 Address"
   - Mac/Linux: `ifconfig` → busca "inet"
   - Ejemplo: `192.168.0.204`

2. **Configura el .env:**
```env
EXPO_PUBLIC_BACKEND_URL=http://192.168.0.204:8003
```

#### **Opción C: Usar un túnel temporal** (Para testing externo)

1. **Iniciar túnel Cloudflare:**
```bash
cd backend
cloudflared tunnel --url http://localhost:8003
```

2. **Copiar la URL que te da** (ejemplo: `https://xyz-abc.trycloudflare.com`)

3. **Configurar el .env:**
```env
EXPO_PUBLIC_TUNNEL_URL=https://xyz-abc.trycloudflare.com
```

### 3. Reiniciar la App

Después de crear/modificar el `.env`:

```bash
# Limpiar caché y reiniciar
npm run start:clear

# O simplemente reiniciar
npm start
```

### 4. Verificar la Conexión

En los logs de Expo deberías ver:

```
🔧 [BACKEND CONFIG]
   EXPO_PUBLIC_BACKEND_URL: http://192.168.0.204:8003
   BACKEND_URL final: http://192.168.0.204:8003
```

## 🎯 Verificación Rápida

**Probar el backend directamente:**

```bash
# Desde tu navegador o curl:
curl http://127.0.0.1:8003/health

# Respuesta esperada:
{"status":"ok","message":"PetAlert API activa","supabase":"conectado"}
```

## 📝 Notas Importantes

1. **No commitear el `.env`** - Está en `.gitignore` por seguridad
2. **Túneles son temporales** - Si reinicias cloudflared, cambia la URL
3. **Mismo WiFi** - Para dispositivos físicos, PC y celular deben estar en la misma red
4. **Firewall** - Asegúrate de que el puerto 8003 no esté bloqueado

## 🔄 Cambios Realizados

✅ Removido el túnel hardcodeado de la configuración  
✅ Configuración ahora usa variables de entorno  
✅ Fallback a localhost por defecto  
✅ Actualizado `env.example` con ejemplos  

## 📚 Archivos Modificados

- `src/config/backend.js` - Configuración del backend URL
- `env.example` - Ejemplos de configuración


