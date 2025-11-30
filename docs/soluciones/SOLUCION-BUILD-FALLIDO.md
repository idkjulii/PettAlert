# 🔧 Solución: Build EAS Fallido

## Problema
El build falló en la fase "Install dependencies" con error desconocido.

## Pasos para Diagnosticar

### 1. Ver Logs Detallados

Abre el link de los logs:
```
https://expo.dev/accounts/idkjulii/projects/petalert/builds/64c8f019-3db0-4dbd-b8bc-274ec52910ae
```

Busca en los logs:
- Errores de dependencias incompatibles
- Problemas con versiones de Node/npm
- Errores de permisos
- Problemas con archivos faltantes

---

## Posibles Causas y Soluciones

### Problema 1: Incompatibilidad React 19 con React Native 0.81.5

**Síntoma:** React 19.1.0 no es compatible con React Native 0.81.5

**Solución:**

```powershell
# Instalar versión compatible de React
npm install react@18.3.1 react-dom@18.3.1

# O usar expo install para versiones compatibles
npx expo install react react-dom
```

---

### Problema 2: Dependencias Faltantes o Corruptas

**Solución:**

```powershell
# Limpiar todo
rd /s /q node_modules
del package-lock.json
del yarn.lock

# Reinstalar
npm install

# Verificar que no haya errores
npm run lint
```

---

### Problema 3: Archivos .easignore o Configuración EAS

**Verificar si existe `.easignore`:**

```powershell
# Si existe, revisar que no esté excluyendo archivos necesarios
cat .easignore
```

**Verificar `eas.json`:**

```powershell
# Verificar configuración de build
cat eas.json
```

---

### Problema 4: Versión de Node.js Incompatible

EAS Build usa Node 20 por defecto. Verifica que tu proyecto sea compatible.

**Solución:** Asegúrate de que `package.json` no especifique una versión de Node incompatible.

---

## Solución Rápida: Reintentar Build

A veces es un error temporal. Intenta de nuevo:

```powershell
eas build --platform android --profile preview
```

---

## Solución Completa: Verificar y Corregir Dependencias

### Paso 1: Verificar compatibilidad de React

```powershell
# React Native 0.81.5 requiere React 18.x
npm install react@18.3.1 react-dom@18.3.1 --save-exact
```

### Paso 2: Actualizar dependencias de Expo

```powershell
npx expo install --fix
```

### Paso 3: Limpiar y reinstalar

```powershell
rd /s /q node_modules
del package-lock.json
npm install
```

### Paso 4: Verificar que compile localmente

```powershell
npx expo start --no-dev --minify
```

Si compila localmente, el problema puede ser específico de EAS Build.

---

## Ver Logs Completos

1. Abre: https://expo.dev/accounts/idkjulii/projects/petalert/builds/64c8f019-3db0-4dbd-b8bc-274ec52910ae
2. Busca la sección "Install dependencies"
3. Copia el error completo
4. Compártelo para diagnóstico más específico

---

## Alternativa: Build Local

Si EAS Build sigue fallando, puedes compilar localmente:

```powershell
# Requiere Android Studio instalado
npx expo run:android
```

Esto generará un APK localmente.

