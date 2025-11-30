# 📋 Guía Paso a Paso: Configuración de Supabase para Autenticación

## 🎯 Objetivo
Configurar completamente Supabase para que el sistema de autenticación funcione correctamente.

---

## 📍 PASO 1: Crear o Acceder a tu Proyecto Supabase

### 1.1. Ir a Supabase
1. Abre tu navegador y ve a: **https://supabase.com**
2. Si no tienes cuenta:
   - Haz clic en **"Sign Up"** o **"Start your project"**
   - Regístrate con GitHub, Google, o email
3. Si ya tienes cuenta:
   - Haz clic en **"Sign In"**
   - Inicia sesión

### 1.2. Crear Nuevo Proyecto (si no tienes uno)
1. En el dashboard, haz clic en **"New Project"** (botón verde)
2. Completa el formulario:
   - **Name**: `petalert` (o el nombre que prefieras)
   - **Database Password**: 
     - Genera una contraseña segura
     - **¡GUÁRDALA EN UN LUGAR SEGURO!** La necesitarás para acceder a la base de datos
   - **Region**: Selecciona la región más cercana a ti
   - **Pricing Plan**: Selecciona "Free" (plan gratuito)
3. Haz clic en **"Create new project"**
4. **Espera 2-3 minutos** mientras se crea el proyecto

---

## 🔑 PASO 2: Obtener las Credenciales de API

### 2.1. Acceder a la Configuración de API
1. En el menú lateral izquierdo, haz clic en **⚙️ Settings** (Configuración)
2. Haz clic en **"API"** en el submenú

### 2.2. Copiar las Credenciales
Verás dos secciones importantes:

#### **Project URL**
- Copia la URL completa que aparece (ejemplo: `https://xxxxxxxxxxxxx.supabase.co`)
- Esta es tu **EXPO_PUBLIC_SUPABASE_URL**

#### **Project API keys**
Encontrarás varias claves, necesitas estas dos:

1. **`anon` `public`** key:
   - Esta es la clave pública (segura para usar en el frontend)
   - Copia toda la clave (es muy larga, empieza con `eyJhbGci...`)
   - Esta es tu **EXPO_PUBLIC_SUPABASE_ANON_KEY**

2. **`service_role` `secret`** key (opcional, solo para backend):
   - ⚠️ **¡NUNCA la expongas en el frontend!**
   - Solo se usa en el backend
   - Si tienes backend, cópiala también

### 2.3. Guardar las Credenciales
Crea un archivo `.env` en la raíz de tu proyecto con:

```env
EXPO_PUBLIC_SUPABASE_URL=https://tu-proyecto-id.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=tu-clave-anon-public-completa-aqui
```

**Ejemplo real:**
```env
EXPO_PUBLIC_SUPABASE_URL=https://eamsbroadstwkrkjcuvo.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVhbXNicm9hZHN0d2tya2pjdXZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3MjQ3ODgsImV4cCI6MjA3NTMwMDc4OH0.bzFaxK25SPMKE5REMxRyK9jPj1n8ocDrn_u6qyMTXEw
```

---

## 🗄️ PASO 3: Crear la Tabla de Perfiles

### 3.1. Abrir el SQL Editor
1. En el menú lateral izquierdo, haz clic en **"SQL Editor"** (ícono de base de datos)
2. Haz clic en **"New query"** (botón verde en la parte superior)

### 3.2. Ejecutar el Script SQL
Copia y pega este script completo en el editor:

```sql
-- ==============================================
-- CREAR TABLA DE PERFILES
-- ==============================================

-- Crear la tabla profiles si no existe
CREATE TABLE IF NOT EXISTS profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    full_name TEXT,
    avatar_url TEXT,
    phone TEXT,
    location GEOMETRY(POINT, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar Row Level Security (RLS)
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Política: Cualquiera puede ver perfiles
CREATE POLICY "Users can view all profiles" 
ON profiles FOR SELECT 
USING (true);

-- Política: Usuarios pueden actualizar su propio perfil
CREATE POLICY "Users can update own profile" 
ON profiles FOR UPDATE 
USING (auth.uid() = id);

-- Política: Usuarios pueden insertar su propio perfil
CREATE POLICY "Users can insert own profile" 
ON profiles FOR INSERT 
WITH CHECK (auth.uid() = id);

-- Crear índice para mejorar rendimiento
CREATE INDEX IF NOT EXISTS idx_profiles_location ON profiles USING GIST (location);
```

### 3.3. Ejecutar el Script
1. Haz clic en el botón **"Run"** (▶️) en la parte inferior derecha
2. O presiona `Ctrl + Enter` (Windows) o `Cmd + Enter` (Mac)
3. Deberías ver un mensaje de éxito: **"Success. No rows returned"**

---

## 🔐 PASO 4: Configurar Autenticación

### 4.1. Acceder a Configuración de Autenticación
1. En el menú lateral, haz clic en **"Authentication"** (ícono de candado)
2. Haz clic en **"Settings"** (Configuración) en el submenú

### 4.2. Configurar URLs de Redirección

#### **Site URL**
1. Busca el campo **"Site URL"**
2. Para desarrollo local con Expo, usa:
   ```
   exp://localhost:8081
   ```
   O si usas una IP específica:
   ```
   exp://192.168.0.204:8081
   ```
   (Reemplaza con tu IP local si es necesario)

#### **Redirect URLs**
1. Busca la sección **"Redirect URLs"**
2. Haz clic en **"Add URL"**
3. Agrega estas URLs (una por una):
   - `exp://localhost:8081`
   - `exp://localhost:8081/--/(auth)/login`
   - `exp://localhost:8081/--/(auth)/reset-password`
   - Si usas IP local, también agrega:
     - `exp://192.168.0.204:8081`
     - `exp://192.168.0.204:8081/--/(auth)/login`
     - `exp://192.168.0.204:8081/--/(auth)/reset-password`

### 4.3. Configurar Email (Opcional pero Recomendado)

#### **Email Templates**
1. En la misma página de Settings, busca **"Email Templates"**
2. Puedes personalizar los templates o dejarlos por defecto
3. Los templates disponibles son:
   - **Confirm signup** - Email de confirmación de registro
   - **Reset password** - Email de recuperación de contraseña
   - **Magic Link** - Si usas magic links

#### **Email Confirmation (Confirmación de Email)**
1. Busca la sección **"Email Auth"**
2. Decide si quieres:
   - **"Enable email confirmations"** ✅ (Recomendado para producción)
   - O deshabilitarlo para desarrollo rápido ⚠️

**Para desarrollo rápido:**
- Desactiva "Enable email confirmations" temporalmente
- Los usuarios podrán iniciar sesión sin confirmar email

**Para producción:**
- Activa "Enable email confirmations"
- Los usuarios deben confirmar su email antes de iniciar sesión

### 4.4. Configurar Proveedores de Autenticación
1. En el menú lateral, dentro de **"Authentication"**, haz clic en **"Providers"**
2. Por defecto, **"Email"** está habilitado ✅
3. Puedes habilitar otros proveedores si lo deseas:
   - Google
   - GitHub
   - Apple
   - etc.

---

## 🧪 PASO 5: Verificar la Configuración

### 5.1. Verificar que la Tabla Existe
1. En el menú lateral, haz clic en **"Table Editor"**
2. Deberías ver la tabla **"profiles"** en la lista
3. Haz clic en ella para ver su estructura

### 5.2. Verificar Políticas RLS
1. En **"Table Editor"**, haz clic en la tabla **"profiles"**
2. Haz clic en la pestaña **"Policies"** (arriba)
3. Deberías ver 3 políticas:
   - "Users can view all profiles"
   - "Users can update own profile"
   - "Users can insert own profile"

### 5.3. Probar la Autenticación (Opcional)
1. En el menú lateral, haz clic en **"Authentication"** > **"Users"**
2. Aquí verás todos los usuarios registrados
3. Inicialmente estará vacío
4. Después de que alguien se registre, aparecerá aquí

---

## 🔧 PASO 6: Configurar Variables de Entorno en tu Proyecto

### 6.1. Crear Archivo .env
1. En la raíz de tu proyecto (donde está `package.json`)
2. Crea un archivo llamado `.env` (sin extensión)
3. Si ya existe, ábrelo

### 6.2. Agregar las Credenciales
Abre el archivo `.env` y agrega:

```env
# Supabase Configuration (Frontend)
EXPO_PUBLIC_SUPABASE_URL=https://tu-proyecto-id.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=tu-clave-anon-public-completa

# App Configuration
EXPO_PUBLIC_APP_NAME=PetAlert
EXPO_PUBLIC_APP_VERSION=1.0.0
```

**⚠️ IMPORTANTE:**
- Reemplaza `https://tu-proyecto-id.supabase.co` con tu URL real
- Reemplaza `tu-clave-anon-public-completa` con tu clave real
- No dejes espacios alrededor del `=`
- No uses comillas alrededor de los valores

### 6.3. Verificar que .env está en .gitignore
1. Abre el archivo `.gitignore` en la raíz del proyecto
2. Asegúrate de que tenga esta línea:
   ```
   .env
   ```
3. Si no está, agrégalo (esto evita que subas tus credenciales a GitHub)

---

## 🚀 PASO 7: Reiniciar la Aplicación

### 7.1. Detener la Aplicación
Si tienes la app corriendo:
1. Presiona `Ctrl + C` en la terminal donde está corriendo Expo

### 7.2. Limpiar Caché y Reiniciar
Ejecuta estos comandos en la terminal:

```bash
# Limpiar caché
npx expo start --clear
```

O si prefieres:

```bash
# Limpiar node_modules y reinstalar (solo si hay problemas)
rm -rf node_modules
npm install
npx expo start --clear
```

### 7.3. Verificar en la Consola
Cuando la app inicie, deberías ver en la consola:

```
🔧 Configuración de Supabase:
URL: https://tu-proyecto-id.supabase.co
Key: eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...
```

Si ves errores sobre credenciales, verifica el archivo `.env`

---

## ✅ PASO 8: Probar el Sistema

### 8.1. Probar Registro
1. Abre la app
2. Ve a la pantalla de registro
3. Completa el formulario:
   - Nombre completo
   - Email válido
   - Contraseña (mínimo 6 caracteres)
4. Haz clic en "Crear Cuenta"
5. Deberías ver un mensaje de éxito

### 8.2. Verificar Usuario Creado
1. Ve a Supabase Dashboard
2. **Authentication** > **Users**
3. Deberías ver el nuevo usuario en la lista
4. El email debería aparecer como "Unconfirmed" o "Confirmed" según tu configuración

### 8.3. Verificar Perfil Creado
1. En Supabase Dashboard
2. **Table Editor** > **profiles**
3. Deberías ver una fila con el `id` del usuario
4. El `full_name` debería tener el nombre que ingresaste

### 8.4. Probar Login
1. En la app, ve a la pantalla de login
2. Ingresa el email y contraseña que usaste para registrarte
3. Haz clic en "Iniciar Sesión"
4. Deberías ser redirigido a la pantalla principal

### 8.5. Probar Recuperación de Contraseña
1. En la pantalla de login, haz clic en "¿Olvidaste tu contraseña?"
2. Ingresa tu email
3. Haz clic en "Enviar Email de Recuperación"
4. Revisa tu email (y la carpeta de spam)
5. Deberías recibir un email de Supabase con un enlace

---

## 🐛 Solución de Problemas Comunes

### Problema: "Invalid API key"
**Solución:**
- Verifica que copiaste la clave completa (es muy larga)
- Asegúrate de que no hay espacios al inicio o final
- Verifica que el archivo `.env` está en la raíz del proyecto
- Reinicia la app con `npx expo start --clear`

### Problema: "Email not confirmed"
**Solución:**
- Ve a **Authentication** > **Settings** en Supabase
- Desactiva temporalmente "Enable email confirmations" para desarrollo
- O verifica tu email y haz clic en el enlace de confirmación

### Problema: "Failed to create profile"
**Solución:**
- Verifica que ejecutaste el script SQL del Paso 3
- Verifica que las políticas RLS están creadas
- Revisa los logs en Supabase Dashboard > **Logs** > **Postgres Logs**

### Problema: "Redirect URL mismatch"
**Solución:**
- Ve a **Authentication** > **Settings** > **Redirect URLs**
- Asegúrate de agregar todas las URLs que uses
- Para desarrollo, agrega: `exp://localhost:8081`

### Problema: No se crea el perfil automáticamente
**Solución:**
- Verifica que la tabla `profiles` existe
- Verifica las políticas RLS
- Revisa la consola de la app para ver errores específicos
- El perfil se crea automáticamente, pero puede haber un pequeño delay

---

## 📝 Checklist Final

Antes de considerar que todo está configurado, verifica:

- [ ] Proyecto creado en Supabase
- [ ] Credenciales copiadas (URL y anon key)
- [ ] Archivo `.env` creado con las credenciales
- [ ] Tabla `profiles` creada (verificar en Table Editor)
- [ ] Políticas RLS configuradas (3 políticas visibles)
- [ ] URLs de redirección configuradas en Authentication Settings
- [ ] Email confirmation configurado según tus necesidades
- [ ] App reiniciada con `--clear`
- [ ] Registro de usuario funciona
- [ ] Login funciona
- [ ] Perfil se crea automáticamente
- [ ] Recuperación de contraseña funciona

---

## 🎉 ¡Listo!

Si completaste todos los pasos y el checklist, tu sistema de autenticación debería estar funcionando completamente.

**¿Necesitas ayuda?** Revisa la sección de "Solución de Problemas" o los logs en Supabase Dashboard.

---

**Última actualización**: Guía completa paso a paso para configuración de Supabase.

