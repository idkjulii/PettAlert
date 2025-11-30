# 📱 Guía Simple: Cómo Ejecutar la App

## 🤔 ¿Qué necesitas hacer?

Tienes **2 opciones** para ejecutar tu app. Te explico ambas:

---

## ✅ OPCIÓN 1: Desarrollo Rápido (Sin Build - Recomendado para empezar)

### **¿Qué es?**
Ejecutar la app usando **Expo Go** (una app que ya está en tu teléfono). No necesitas compilar nada.

### **¿Qué necesitas?**
- ✅ Tu teléfono Android/iOS
- ✅ App **Expo Go** instalada (descárgala de Play Store/App Store)
- ✅ Tu computadora y teléfono en la misma red WiFi

### **Pasos:**

1. **Abre PowerShell** en tu proyecto:
   ```powershell
   cd "C:\Users\maria\OneDrive\Escritorio\lpm\petFindnoborres"
   ```

2. **Regenera configuración** (solo la primera vez o cuando cambies permisos):
   ```powershell
   npx expo prebuild --clean
   ```

3. **Inicia el servidor de desarrollo:**
   ```powershell
   npx expo start --tunnel
   ```
   
   Esto mostrará un **código QR**.

4. **En tu teléfono:**
   - Abre la app **Expo Go**
   - Escanea el código QR que aparece en PowerShell
   - La app se cargará en tu teléfono

### **Ventajas:**
- ✅ No necesitas instalar Android Studio
- ✅ No necesitas compilar (más rápido)
- ✅ Puedes probar cambios al instante

### **Limitaciones:**
- ⚠️ Algunos permisos avanzados pueden no funcionar completamente
- ⚠️ No es la versión final para producción

---

## ✅ OPCIÓN 2: Build Nativo (Para Producción)

### **¿Qué es?**
Compilar la app nativamente para crear un APK (Android) o IPA (iOS). Es la versión "real" de la app.

### **¿Qué necesitas?**
- ✅ **Android Studio** instalado (para Android)
- ✅ **Xcode** instalado (para iOS, solo Mac)
- ✅ Más tiempo (la primera compilación tarda 10-30 minutos)

### **Pasos para Android:**

1. **Instalar Android Studio:**
   - Descarga: https://developer.android.com/studio
   - Instálalo (puede tardar 20-30 minutos)
   - Abre Android Studio y deja que descargue los SDKs

2. **Configurar variables de entorno:**
   - Android Studio → Settings → Appearance & Behavior → System Settings → Android SDK
   - Copia la ruta del "Android SDK Location"
   - Agrega estas variables de entorno en Windows:
     - `ANDROID_HOME` = ruta del SDK
     - Agrega `%ANDROID_HOME%\platform-tools` al PATH

3. **En PowerShell:**
   ```powershell
   # Regenerar configuración
   npx expo prebuild --clean
   
   # Compilar y ejecutar
   npx expo run:android
   ```

### **Ventajas:**
- ✅ Funcionalidad completa
- ✅ Permisos completos de ubicación en background
- ✅ Versión lista para producción

### **Desventajas:**
- ⚠️ Requiere instalar Android Studio (2-3 GB)
- ⚠️ Primera compilación tarda mucho tiempo
- ⚠️ Más complejo

---

## 🎯 ¿Cuál elegir?

### **Para PROBAR y DESARROLLAR:**
→ Usa **OPCIÓN 1** (Expo Go)

### **Para PRODUCCIÓN y FUNCIONALIDAD COMPLETA:**
→ Usa **OPCIÓN 2** (Build nativo)

---

## 📋 Pasos Recomendados (OPCIÓN 1 - Fácil)

### **Paso 1: Instalar Expo Go en tu teléfono**

1. Abre **Play Store** (Android) o **App Store** (iOS)
2. Busca **"Expo Go"**
3. Instálala

### **Paso 2: En tu computadora**

```powershell
# 1. Ir a tu proyecto
cd "C:\Users\maria\OneDrive\Escritorio\lpm\petFindnoborres"

# 2. Regenerar configuración (solo primera vez)
npx expo prebuild --clean

# 3. Iniciar servidor
npx expo start --tunnel
```

### **Paso 3: Conectar tu teléfono**

1. Espera a que aparezca el **código QR** en PowerShell
2. Abre **Expo Go** en tu teléfono
3. Escanea el código QR
4. La app se cargará en tu teléfono

---

## 🐛 Si algo no funciona

### **Error: "expo no se reconoce"**
```powershell
npm install -g expo-cli
```

### **Error: "No se puede conectar"**
- Asegúrate de que tu teléfono y computadora estén en la misma red WiFi
- O usa `--tunnel` para conexión por internet

### **Error: "Android Studio no encontrado" (solo para Opción 2)**
- Instala Android Studio primero
- Configura las variables de entorno

---

## 📱 Para el Sistema de Alertas Geográficas

**Recomendación:** Empieza con **OPCIÓN 1** (Expo Go) para probar la UI y funcionalidad básica. Si todo funciona bien, luego haz el build nativo (OPCIÓN 2) para producción.

---

## ✅ Resumen Simple

**OPCIÓN 1 (Fácil):**
```powershell
npx expo start --tunnel
```
→ Escanea QR con Expo Go → Listo

**OPCIÓN 2 (Completo):**
```powershell
npx expo run:android
```
→ Requiere Android Studio → Crea APK

---

**¿Cuál prefieres probar primero?**

