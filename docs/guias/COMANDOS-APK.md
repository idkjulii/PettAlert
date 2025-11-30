# 🚀 Comandos Rápidos para Generar APK

## 📋 Guía Rápida de 3 Pasos

### 1️⃣ Instalar EAS CLI (solo una vez)

```bash
npm install -g eas-cli
```

### 2️⃣ Iniciar Sesión (solo una vez)

```bash
eas login
```

Si no tienes cuenta: https://expo.dev/signup

### 3️⃣ Generar APK

```bash
eas build --platform android --profile preview
```

¡Listo! En 10-20 minutos tendrás tu APK listo para descargar.

---

## 🎯 Comandos Principales

### Generar APK para Pruebas (Recomendado)

```bash
eas build --platform android --profile preview
```

**Cuándo usar:** Para probar la app o compartir con otros.

---

### Generar AAB para Producción

```bash
eas build --platform android --profile production
```

**Cuándo usar:** Para subir a Google Play Store.

---

### Build de Desarrollo Rápido

```bash
npx expo run:android
```

**Cuándo usar:** Para desarrollo y pruebas rápidas con dispositivo conectado.

---

### Build Local (en tu PC)

```bash
eas build --platform android --profile preview --local
```

**Cuándo usar:** Si prefieres hacer el build en tu computadora.  
**Requisitos:** Android Studio instalado.

---

## 📱 Gestión de Builds

### Ver Lista de Builds

```bash
eas build:list
```

### Ver Detalles de un Build Específico

```bash
eas build:view [BUILD_ID]
```

### Cancelar un Build en Progreso

```bash
eas build:cancel [BUILD_ID]
```

---

## 🛠️ Configuración

### Configurar EAS por Primera Vez

```bash
eas build:configure
```

### Ver Información de tu Cuenta

```bash
eas whoami
```

### Cerrar Sesión

```bash
eas logout
```

---

## 🔧 Comandos de Desarrollo

### Iniciar Servidor de Desarrollo

```bash
npm start
```

O con caché limpio:

```bash
npm run start:clear
```

### Ejecutar en Android (con código nativo)

```bash
npm run android
```

### Limpiar Caché y Reiniciar

```bash
npm run clean
```

---

## 📦 Antes de Generar APK

### 1. Verificar que todo funciona

```bash
npm start
```

Prueba la app en Expo Go o emulador.

### 2. Actualizar versión (para producción)

Edita `app.json`:

```json
{
  "expo": {
    "version": "1.0.1",
    "android": {
      "versionCode": 2
    }
  }
}
```

### 3. Verificar variables de entorno

Asegúrate de tener configuradas:
- URL del backend
- API keys de Supabase
- Otras variables necesarias

---

## 🚨 Solución Rápida de Problemas

### Error: "Not logged in"

```bash
eas login
```

### Error: "Build failed"

1. Revisa los logs del build
2. Verifica `app.json` y `eas.json`
3. Asegúrate de que todas las dependencias estén instaladas

```bash
npm install
```

### Error: "Android SDK not found" (build local)

Configura ANDROID_HOME:

```powershell
# Windows PowerShell
[System.Environment]::SetEnvironmentVariable('ANDROID_HOME', 'C:\Users\TU_USUARIO\AppData\Local\Android\Sdk', 'User')
```

### Limpiar todo y empezar de nuevo

```bash
# Limpiar caché de npm
npm cache clean --force

# Reinstalar dependencias
rm -rf node_modules
npm install

# Limpiar caché de Expo
npm run clean
```

---

## 💡 Consejos Pro

### Build más rápido

Usa el perfil `preview` en lugar de `production` para pruebas:

```bash
eas build --platform android --profile preview
```

### Build automático en cada commit

Configura GitHub Actions con EAS. [Ver documentación](https://docs.expo.dev/build/building-on-ci/)

### Distribución Beta

Usa TestFlight (iOS) o Firebase App Distribution (Android) para distribuir versiones beta.

---

## 📊 Comparación de Métodos

| Método | Tiempo | Dificultad | Uso |
|--------|--------|------------|-----|
| `eas build --profile preview` | 15-20 min | ⭐ Fácil | Testing/Beta |
| `eas build --profile production` | 15-20 min | ⭐ Fácil | Producción |
| `npx expo run:android` | 5-10 min | ⭐⭐ Media | Desarrollo |
| `eas build --local` | 20-30 min | ⭐⭐⭐ Difícil | Build offline |

---

## 🎬 Flujo de Trabajo Recomendado

### Para Desarrollo Diario

```bash
# 1. Iniciar servidor
npm start

# 2. Probar cambios en Expo Go o emulador
# 3. Cuando necesites probar código nativo:
npx expo run:android
```

### Para Testing/Beta

```bash
# Generar APK
eas build --platform android --profile preview

# Esperar build
# Descargar y distribuir APK
```

### Para Producción

```bash
# 1. Actualizar versión en app.json
# 2. Generar AAB
eas build --platform android --profile production

# 3. Descargar AAB
# 4. Subir a Google Play Console
```

---

## 📚 Recursos

- **Documentación Completa:** Ver `GUIA-GENERAR-APK.md`
- **Scripts Automatizados:** 
  - `.\generar-apk.ps1` (PowerShell)
  - `GENERAR-APK.bat` (Batch)
- **Documentación Oficial:** https://docs.expo.dev/build/introduction/
- **Dashboard de Expo:** https://expo.dev/

---

## 🆘 ¿Necesitas Ayuda?

1. Lee `GUIA-GENERAR-APK.md` para guía detallada
2. Revisa la sección de solución de problemas
3. Consulta los logs del build
4. Busca el error específico en la documentación de Expo

---

**Última actualización:** Noviembre 2024


