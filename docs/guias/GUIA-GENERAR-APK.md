# 📱 Guía para Generar APK de PetAlert

## Resumen de Opciones

| Opción | Ventajas | Desventajas | Tiempo |
|--------|----------|-------------|--------|
| **EAS Build (Cloud)** | Fácil, no requiere configuración local | Requiere cuenta Expo, límite de builds gratuitos | 10-20 min |
| **EAS Build (Local)** | Sin límites, más control | Requiere Android Studio y configuración | 15-30 min |
| **Build de Desarrollo** | Más rápido para pruebas | Solo para desarrollo, no para distribución | 5-10 min |

---

## 🌟 Opción 1: EAS Build en la Nube (RECOMENDADO)

### Paso 1: Instalar EAS CLI

```bash
npm install -g eas-cli
```

### Paso 2: Iniciar Sesión

```bash
eas login
```

Si no tienes cuenta, créala en: https://expo.dev/signup

### Paso 3: Configurar EAS

```bash
eas build:configure
```

Este comando creará automáticamente el archivo `eas.json` (ya está creado en tu proyecto).

### Paso 4: Generar APK

**Para una versión de prueba (Preview):**

```bash
eas build --platform android --profile preview
```

**Para una versión de producción (AAB para Google Play):**

```bash
eas build --platform android --profile production
```

### Paso 5: Descargar el APK

Después del build, recibirás un enlace para descargar el APK. También puedes ver todos tus builds en:

```bash
eas build:list
```

O en el dashboard: https://expo.dev

---

## 💻 Opción 2: EAS Build Local

### Requisitos Previos

1. **Instalar Android Studio:**
   - Descarga desde: https://developer.android.com/studio
   - Instala Android SDK y configura las variables de entorno

2. **Variables de Entorno (Windows):**

```powershell
# Agregar a las variables de entorno del sistema:
ANDROID_HOME = C:\Users\TU_USUARIO\AppData\Local\Android\Sdk
```

Y añadir a PATH:
```
%ANDROID_HOME%\platform-tools
%ANDROID_HOME%\tools
%ANDROID_HOME%\tools\bin
```

### Generar APK Local

```bash
eas build --platform android --profile preview --local
```

---

## 🚀 Opción 3: Build de Desarrollo Rápido

### Para Emulador Android

1. **Abrir Android Studio y crear un emulador**

2. **Ejecutar:**

```bash
npx expo run:android
```

### Para Dispositivo Físico

1. **Habilitar modo desarrollador en tu dispositivo Android:**
   - Ve a Configuración > Acerca del teléfono
   - Toca 7 veces en "Número de compilación"
   - Habilita "Depuración USB" en Opciones de desarrollador

2. **Conectar dispositivo por USB**

3. **Verificar conexión:**

```bash
adb devices
```

4. **Ejecutar:**

```bash
npx expo run:android
```

---

## 📦 Tipos de Build

### APK vs AAB

- **APK (Android Package)**: 
  - Archivo instalable directamente
  - Ideal para distribución manual o testing
  - Tamaño más grande

- **AAB (Android App Bundle)**:
  - Formato optimizado para Google Play Store
  - Google Play genera APKs optimizados para cada dispositivo
  - Tamaño más pequeño para usuarios finales

### Perfiles de Build

El archivo `eas.json` define 3 perfiles:

1. **development**: Para desarrollo con hot reload
2. **preview**: Para testing (genera APK)
3. **production**: Para producción (genera AAB)

---

## 🔧 Configuración Adicional

### Actualizar Versión

Antes de generar un APK de producción, actualiza la versión en `app.json`:

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

- **version**: Versión legible (1.0.1, 1.0.2, etc.)
- **versionCode**: Número entero que se incrementa con cada build

### Configurar Icono y Splash Screen

Ya tienes configurado:
- Icon: `./assets/images/icon.png`
- Splash: `./assets/images/splash-icon.png`

Asegúrate de que estas imágenes existen y tienen el tamaño adecuado:
- Icon: 1024x1024 px
- Splash: 1242x2436 px

---

## 🐛 Solución de Problemas Comunes

### Error: "ANDROID_HOME no está definido"

**Solución:** Configura las variables de entorno de Android SDK.

En PowerShell (Windows):

```powershell
[System.Environment]::SetEnvironmentVariable('ANDROID_HOME', 'C:\Users\TU_USUARIO\AppData\Local\Android\Sdk', 'User')
```

### Error: "Could not find or load main class org.gradle.wrapper.GradleWrapperMain"

**Solución:** Limpia y reconstruye:

```bash
cd android
./gradlew clean
cd ..
npx expo run:android
```

### Error: "SDK location not found"

**Solución:** Crea el archivo `android/local.properties`:

```properties
sdk.dir=C:\\Users\\TU_USUARIO\\AppData\\Local\\Android\\Sdk
```

### Build falla por falta de memoria

**Solución:** Aumenta la memoria de Gradle en `android/gradle.properties`:

```properties
org.gradle.jvmargs=-Xmx4096m -XX:MaxPermSize=512m
```

---

## 📋 Checklist Pre-Build

Antes de generar tu APK final, verifica:

- [ ] Todas las funcionalidades probadas y funcionando
- [ ] Variables de entorno configuradas (backend URL, API keys)
- [ ] Icono y splash screen en su lugar
- [ ] Versión actualizada en `app.json`
- [ ] Permisos correctos configurados
- [ ] App funciona sin errores en desarrollo

---

## 🚀 Comandos Rápidos de Referencia

```bash
# Instalar EAS CLI
npm install -g eas-cli

# Login a Expo
eas login

# Generar APK de prueba (más rápido)
eas build --platform android --profile preview

# Generar AAB de producción
eas build --platform android --profile production

# Ver historial de builds
eas build:list

# Build local
eas build --platform android --profile preview --local

# Build de desarrollo rápido
npx expo run:android

# Limpiar caché de Expo
expo start -c
```

---

## 📱 Distribución del APK

### Para Testing (Beta)

1. **Compartir APK directamente:**
   - Sube el APK a Google Drive, Dropbox, etc.
   - Comparte el enlace con los testers
   - Los usuarios deben permitir "Instalar aplicaciones de fuentes desconocidas"

2. **Usar Firebase App Distribution:**
   - Más profesional y organizado
   - Permite gestionar testers y versiones

### Para Producción

1. **Google Play Store:**
   - Genera un AAB con el perfil `production`
   - Crea una cuenta de desarrollador (costo único de $25 USD)
   - Sube el AAB a Google Play Console

---

## 🎯 Recomendación

Para tu caso, te recomiendo:

1. **Primera vez / Testing**: Usa **EAS Build en la nube** (Opción 1)
   ```bash
   eas build --platform android --profile preview
   ```

2. **Desarrollo continuo**: Usa **Build de desarrollo** (Opción 3)
   ```bash
   npx expo run:android
   ```

3. **Producción final**: Usa **EAS Build producción** (Opción 1)
   ```bash
   eas build --platform android --profile production
   ```

---

## 📞 Recursos Adicionales

- [Documentación oficial EAS Build](https://docs.expo.dev/build/introduction/)
- [Configurar Android Studio](https://docs.expo.dev/workflow/android-studio-emulator/)
- [Publicar en Google Play](https://docs.expo.dev/submit/android/)
- [Dashboard de Expo](https://expo.dev/)

---

**¿Necesitas ayuda?** Revisa la sección de solución de problemas o consulta los logs del build para más detalles.


