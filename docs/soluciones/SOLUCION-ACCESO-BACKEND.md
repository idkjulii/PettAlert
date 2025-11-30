# 🔧 Solución: Backend No Accesible desde la Red Local

## Problema

El frontend intenta conectarse a `http://192.168.0.204:8003` pero el backend solo está accesible en `http://127.0.0.1:8003` (localhost).

## ✅ Solución

El backend debe iniciarse escuchando en **todas las interfaces de red** (`0.0.0.0`) para que sea accesible desde la IP de la red local.

### Opción 1: Usar el Script de Inicio (Recomendado)

```powershell
.\start-backend.bat
```

Este script ahora inicia el backend con `--host 0.0.0.0` automáticamente.

### Opción 2: Iniciar Manualmente

```powershell
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

**Importante:** Usa `--host 0.0.0.0` (no `127.0.0.1`) para que sea accesible desde la red local.

## Verificación

Después de iniciar el backend, verifica que sea accesible desde ambas IPs:

```powershell
# Desde localhost
Invoke-WebRequest -Uri "http://127.0.0.1:8003/health" -Method GET

# Desde la IP de red local
Invoke-WebRequest -Uri "http://192.168.0.204:8003/health" -Method GET
```

Ambas deberían devolver:
```json
{"status":"ok","message":"PetAlert Vision API activa","supabase":"conectado","google_vision":"configurado"}
```

## Configuración del Frontend

El frontend está configurado para usar:
1. `EXPO_PUBLIC_BACKEND_URL` (si está definida)
2. `NETWORK_CONFIG.BACKEND_URL` (http://192.168.0.204:8003)
3. `http://127.0.0.1:8003` (fallback)

Si quieres forzar el uso de localhost, puedes crear un archivo `.env` en la raíz del proyecto:

```env
EXPO_PUBLIC_BACKEND_URL=http://127.0.0.1:8003
```

O si estás usando la IP de red local, asegúrate de que el backend esté corriendo con `--host 0.0.0.0`.

## Nota de Seguridad

⚠️ **Importante:** Escuchar en `0.0.0.0` hace que el backend sea accesible desde cualquier dispositivo en tu red local. Esto está bien para desarrollo, pero en producción deberías usar un firewall y configurar CORS adecuadamente.
