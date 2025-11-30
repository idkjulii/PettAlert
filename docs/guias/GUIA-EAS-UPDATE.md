# 🚀 Guía de EAS Update (Actualizaciones Over-The-Air)

## ¿Qué es EAS Update?

EAS Update te permite actualizar el código JavaScript de tu app **sin generar un nuevo APK**. Los usuarios reciben las actualizaciones automáticamente cuando abren la app.

---

## ✅ Configuración Completada

Ya está configurado en tu proyecto:
- ✅ Project ID configurado: `6e590065-3e19-4855-8a01-c7966333cc89`
- ✅ Updates URL configurada en `app.config.js`
- ✅ Runtime version configurada (usa la versión de la app)

---

## 📝 Cómo Usar EAS Update

### 1. Hacer Cambios en el Código

Haz tus cambios normalmente en:
- Componentes React
- Hooks
- Servicios
- Estilos
- Lógica de negocio

### 2. Publicar Actualización

**Para Preview (desarrollo):**
```powershell
npm run update:preview "Descripción de los cambios"
```

O directamente:
```powershell
eas update --branch preview --message "Agregué nuevo botón en perfil"
```

**Para Production:**
```powershell
npm run update:production "Descripción de los cambios"
```

O directamente:
```powershell
eas update --branch production --message "Corrección de bug en reportes"
```

### 3. Los Usuarios Reciben la Actualización

- La próxima vez que abran la app, recibirán la actualización automáticamente
- No necesitan reinstalar la app
- La actualización es transparente

---

## 🔄 Flujo de Trabajo Recomendado

### Desarrollo Diario:

```powershell
# 1. Hacer cambios en código
# (editar componentes, hooks, etc.)

# 2. Probar localmente
npm start

# 3. Si todo funciona, publicar actualización
npm run update:preview "Nuevas características agregadas"

# 4. Los usuarios reciben la actualización automáticamente
```

### Cuando Agregas Dependencias Nativas:

```powershell
# 1. Agregar dependencia nativa
npx expo install nueva-dependencia-nativa

# 2. Generar nuevo build (requiere reinstalar)
eas build --platform android --profile preview

# 3. Distribuir nuevo APK
```

---

## 📋 Comandos Útiles

### Ver Actualizaciones Publicadas:
```powershell
eas update:list
```

### Ver Detalles de una Actualización:
```powershell
eas update:view UPDATE_ID
```

### Revertir una Actualización:
```powershell
eas update:republish --branch preview --message "Revertir cambios"
```

---

## ⚠️ Limitaciones

### NO se pueden actualizar sin nuevo build:
- ❌ Agregar nuevas dependencias nativas
- ❌ Cambiar configuración en `app.json`/`app.config.js`
- ❌ Cambiar permisos
- ❌ Cambiar icono o splash screen
- ❌ Cambiar versión de Expo SDK

### SÍ se pueden actualizar sin nuevo build:
- ✅ Código JavaScript/TypeScript
- ✅ Componentes React
- ✅ Estilos/CSS
- ✅ Imágenes y assets
- ✅ Lógica de negocio

---

## 🎯 Ejemplo Práctico

### Escenario: Agregar un nuevo botón

```powershell
# 1. Editar el componente
# (cambiar código JavaScript)

# 2. Probar localmente
npm start

# 3. Publicar actualización
npm run update:preview "Agregado botón de configuración en perfil"

# 4. Los usuarios reciben el cambio automáticamente
# (sin reinstalar la app)
```

---

## 🔍 Verificar que Funciona

### 1. Publicar una actualización de prueba:
```powershell
eas update --branch preview --message "Actualización de prueba"
```

### 2. Abrir la app en tu teléfono:
- La app debería descargar la actualización automáticamente
- Puedes ver en los logs de Expo si se descargó

### 3. Verificar en el dashboard:
- Ve a: https://expo.dev/accounts/idkjulii/projects/petalert/updates
- Deberías ver la actualización publicada

---

## 📝 Notas Importantes

1. **Runtime Version**: Las actualizaciones solo se aplican a builds con la misma `runtimeVersion`. Si cambias la versión de la app (`1.0.0`), necesitas un nuevo build.

2. **Branches**: 
   - `preview`: Para desarrollo y testing
   - `production`: Para usuarios finales

3. **Primera Vez**: El primer build debe incluir la configuración de updates (ya está configurado).

---

## 🎉 ¡Listo!

Ya puedes actualizar tu app sin generar nuevos builds para cambios de código JavaScript. Solo recuerda:

- **Cambios de código** → `eas update`
- **Cambios nativos** → `eas build`

