# 🔧 Instalar Supabase CLI en Windows

## ⚠️ Problema

Supabase CLI **NO** se puede instalar con `npm install -g` en Windows. Necesitas usar otro método.

---

## ✅ SOLUCIÓN 1: Usar Scoop (Recomendado - Más Fácil)

### **Paso 1: Instalar Scoop (si no lo tienes)**

Abre PowerShell **como Administrador** y ejecuta:

```powershell
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
irm get.scoop.sh | iex
```

### **Paso 2: Instalar Supabase CLI**

```powershell
scoop bucket add supabase https://github.com/supabase/scoop-bucket.git
scoop install supabase
```

### **Paso 3: Verificar**

```powershell
supabase --version
```

---

## ✅ SOLUCIÓN 2: Descargar Binario Directamente

### **Paso 1: Descargar el binario**

1. Ve a: https://github.com/supabase/cli/releases/latest
2. Busca el archivo para Windows: `supabase_X.X.X_windows_amd64.zip`
3. Descárgalo

### **Paso 2: Extraer y mover**

1. Extrae el ZIP
2. Copia el archivo `supabase.exe` a una carpeta en tu PATH, por ejemplo:
   ```
   C:\Users\maria\AppData\Local\Programs\supabase\
   ```

### **Paso 3: Agregar al PATH**

1. Presiona `Windows + R`
2. Escribe: `sysdm.cpl` y presiona Enter
3. Click en la pestaña **"Opciones avanzadas"**
4. Click en **"Variables de entorno"**
5. En "Variables del sistema", busca **Path** y click en **Editar**
6. Click en **Nuevo**
7. Agrega la ruta donde pusiste `supabase.exe` (ej: `C:\Users\maria\AppData\Local\Programs\supabase`)
8. Click **Aceptar** en todas las ventanas
9. **Cierra y vuelve a abrir PowerShell**

### **Paso 4: Verificar**

```powershell
supabase --version
```

---

## ✅ SOLUCIÓN 3: Usar Chocolatey (Si lo tienes instalado)

```powershell
choco install supabase
```

---

## ✅ SOLUCIÓN 4: Usar npx (Sin instalar globalmente)

Si no puedes instalar Supabase CLI, puedes usar `npx` para ejecutarlo sin instalarlo:

```powershell
# En lugar de: supabase functions deploy
npx supabase functions deploy send-geo-alerts --project-ref eamsbroadstwkrkjcuvo

# En lugar de: supabase login
npx supabase login

# En lugar de: supabase --version
npx supabase --version
```

**Nota:** Esto descargará el CLI cada vez que lo uses, pero funciona sin instalación.

---

## 🎯 Recomendación

**Usa la SOLUCIÓN 1 (Scoop)** si no lo tienes, o **SOLUCIÓN 4 (npx)** si quieres algo rápido sin instalar nada.

---

## 📋 Después de Instalar

Una vez que `supabase --version` funcione, continúa con:

```powershell
# 1. Login
supabase login

# 2. Desplegar función
supabase functions deploy send-geo-alerts --project-ref eamsbroadstwkrkjcuvo
```

---

## 🐛 Si Aún No Funciona

1. **Cierra y vuelve a abrir PowerShell** después de instalar
2. **Verifica el PATH:**
   ```powershell
   $env:PATH
   ```
   Deberías ver la ruta donde está supabase.exe

3. **Prueba con la ruta completa:**
   ```powershell
   C:\Users\maria\AppData\Local\Programs\supabase\supabase.exe --version
   ```

