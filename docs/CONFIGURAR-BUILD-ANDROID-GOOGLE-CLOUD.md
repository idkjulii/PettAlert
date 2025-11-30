# 📱 Configurar Build Android con Backend en Google Cloud

## 🎯 Resumen

Para que el build de Android funcione **sin necesidad de tener el backend corriendo localmente**, necesitas:

1. ✅ Desplegar el backend en Google Cloud VM
2. ✅ Obtener la IP pública del backend
3. ✅ Configurar esa IP en `eas.json`
4. ✅ Reconstruir el APK

---

## 📋 Paso a Paso

### 1️⃣ Desplegar Backend en Google Cloud

Sigue la guía completa: [`docs/guias/GUIA-DEPLOY-GOOGLE-CLOUD.md`](../guias/GUIA-DEPLOY-GOOGLE-CLOUD.md)

**Resumen rápido:**
- Crear VM en Google Cloud (e2-medium, Ubuntu 22.04)
- Configurar firewall (puerto 8003)
- Subir proyecto y credenciales
- Ejecutar `deploy-vm.sh`

### 2️⃣ Obtener la IP Pública

Después del deploy, obtén la IP pública de tu VM:

**Opción A - Desde Google Cloud Console:**
1. Ve a **Compute Engine** → **VM instances**
2. Busca tu VM `petalert-backend`
3. Copia la **External IP** (ejemplo: `34.123.45.67`)

**Opción B - Desde la VM:**
```bash
curl -H "Metadata-Flavor: Google" \
  http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip
```

**⚠️ IMPORTANTE:** Reserva una IP estática para que no cambie al reiniciar la VM:
1. Ve a **VPC network** → **External IP addresses**
2. Click en **RESERVE STATIC ADDRESS**
3. Selecciona tu VM y reserva la IP

### 3️⃣ Verificar que el Backend Funciona

Prueba que el backend sea accesible desde internet:

```bash
# Reemplaza TU_IP con tu IP pública
curl http://TU_IP:8003/health
```

Deberías recibir:
```json
{
  "status": "ok",
  "message": "PetAlert Vision API activa",
  "supabase": "conectado",
  "google_vision": "configurado"
}
```

### 4️⃣ Configurar `eas.json`

Edita el archivo `eas.json` y reemplaza `TU_IP_GOOGLE_CLOUD` con tu IP real:

```json
{
  "build": {
    "preview": {
      "env": {
        "EXPO_PUBLIC_BACKEND_URL": "http://34.123.45.67:8003"
      }
    },
    "production": {
      "env": {
        "EXPO_PUBLIC_BACKEND_URL": "http://34.123.45.67:8003"
      }
    }
  }
}
```

**Ejemplo real:**
```json
"EXPO_PUBLIC_BACKEND_URL": "http://34.123.45.67:8003"
```

### 5️⃣ Reconstruir el APK

Después de configurar la IP, reconstruye el APK:

```bash
eas build --platform android --profile preview
```

El nuevo build incluirá la URL del backend en Google Cloud y funcionará sin necesidad de tener el backend local corriendo.

---

## 🔍 Verificación

### Verificar en el Build

Cuando ejecutes la app, revisa los logs. Deberías ver:

```
🔧 [BACKEND CONFIG]
   EXPO_PUBLIC_BACKEND_URL: http://34.123.45.67:8003
   BACKEND_URL final: http://34.123.45.67:8003
```

### Probar Funcionalidad

1. Instala el APK en tu dispositivo Android
2. Intenta crear un reporte de mascota perdida
3. Verifica que se conecte al backend en Google Cloud
4. Revisa los logs del backend en la VM para confirmar las peticiones

---

## 🌐 Usar Dominio Personalizado (Opcional)

Si quieres usar un dominio en lugar de la IP (ej: `api.petalert.com`):

### Opción 1: Cloud DNS de Google Cloud
1. Ve a **Network Services** → **Cloud DNS**
2. Crea una zona DNS
3. Agrega un registro A apuntando a tu IP estática
4. Configura tu dominio para usar los nameservers de Google Cloud

### Opción 2: Servicio de DNS externo
1. En tu proveedor de dominio, crea un registro A
2. Apunta a tu IP estática de Google Cloud
3. Actualiza `eas.json` con el dominio:
   ```json
   "EXPO_PUBLIC_BACKEND_URL": "http://api.petalert.com:8003"
   ```

---

## 🔒 Seguridad (Recomendado)

### 1. Configurar HTTPS

Para producción, deberías usar HTTPS. Opciones:

**Opción A - Load Balancer con SSL:**
- Crea un Load Balancer en Google Cloud
- Configura certificado SSL
- Apunta a tu VM backend

**Opción B - Nginx como reverse proxy:**
- Instala Nginx en la VM
- Configura SSL con Let's Encrypt
- Nginx redirige a tu backend en puerto 8003

### 2. Restringir CORS

En `backend/.env`, configura `ALLOWED_ORIGINS` con tu dominio:

```env
ALLOWED_ORIGINS=https://petalert.com,https://app.petalert.com
```

### 3. Firewall

Asegúrate de que el firewall solo permita el puerto 8003 desde internet.

---

## 📊 Arquitectura Final

```
┌─────────────────────────────────────────────────┐
│         Dispositivo Android                     │
│         (APK instalado)                         │
└──────────────────┬──────────────────────────────┘
                   │ HTTP/HTTPS
                   │ http://34.123.45.67:8003
                   ▼
┌─────────────────────────────────────────────────┐
│         Google Cloud VM                         │
│         (Ubuntu 22.04)                          │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │         Docker Container                   │ │
│  │         Backend FastAPI                    │ │
│  │         Puerto: 8003                       │ │
│  └───────────────────────────────────────────┘ │
└──────────────────┬──────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────┐
│         Supabase                                │
│         (Base de datos)                         │
└─────────────────────────────────────────────────┘
```

---

## 🐛 Solución de Problemas

### El backend no responde desde internet

1. **Verifica el firewall:**
   ```bash
   # En Google Cloud Console
   # VPC network → Firewall → Verifica regla allow-petalert-backend
   ```

2. **Verifica que la VM tenga el tag:**
   - La VM debe tener el tag `petalert-backend`
   - Edita la VM y agrega el tag si falta

3. **Verifica que el backend esté corriendo:**
   ```bash
   # En la VM
   docker-compose ps
   curl http://localhost:8003/health
   ```

### La app no se conecta al backend

1. **Verifica la IP en `eas.json`:**
   - Asegúrate de que la IP sea correcta
   - No uses `localhost` o IPs locales

2. **Verifica los logs de la app:**
   - Busca el mensaje `🔧 [BACKEND CONFIG]`
   - Confirma que use la IP de Google Cloud

3. **Verifica CORS:**
   - En `backend/.env`, `ALLOWED_ORIGINS` debe permitir tu app
   - Para testing: `ALLOWED_ORIGINS=*`
   - Para producción: especifica dominios exactos

### El build sigue usando IP local

1. **Limpia el caché de EAS:**
   ```bash
   eas build --platform android --profile preview --clear-cache
   ```

2. **Verifica que `eas.json` esté guardado:**
   - Confirma que los cambios estén en el repositorio
   - EAS lee `eas.json` del repositorio, no local

---

## 💰 Costos Estimados

- **VM e2-medium:** ~$35-50/mes
- **IP estática:** Gratis (si la VM está corriendo)
- **Tráfico:** Primeros 1TB/mes gratis, luego ~$0.12/GB

**Total estimado:** ~$35-50/mes para desarrollo/testing

---

## ✅ Checklist Final

- [ ] Backend desplegado en Google Cloud VM
- [ ] IP pública obtenida y reservada (estática)
- [ ] Backend accesible desde internet (`curl http://IP:8003/health`)
- [ ] `eas.json` actualizado con la IP correcta
- [ ] APK reconstruido con `eas build`
- [ ] App probada y funcionando con backend en Google Cloud

---

## 📚 Referencias

- [Guía completa de deploy en Google Cloud](../guias/GUIA-DEPLOY-GOOGLE-CLOUD.md)
- [Deploy rápido](../deploy/DEPLOY-RAPIDO.md)
- [Documentación de EAS Build](https://docs.expo.dev/build/introduction/)


