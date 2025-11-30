# 🔐 Guía Personalizada: Configuración de Autenticación en Supabase

## 📊 Estado Actual de tu Proyecto

Basándome en tu código, veo que ya tienes:

✅ **Proyecto de Supabase creado**: `https://eamsbroadstwkrkjcuvo.supabase.co`  
✅ **Credenciales configuradas** (aunque deberían estar en `.env`)  
✅ **Scripts SQL** para crear tablas (`script-sql-mejorado.sql`)  
✅ **Migraciones adicionales** en `backend/migrations/`  
✅ **Tabla `profiles`** definida en los scripts  
✅ **Políticas RLS** configuradas en los scripts  

---

## 🔍 PASO 1: Verificar qué ya está hecho en Supabase

### 1.1. Acceder a tu Proyecto
1. Ve a [supabase.com](https://supabase.com) e inicia sesión
2. Selecciona tu proyecto: **eamsbroadstwkrkjcuvo**

### 1.2. Verificar Tablas Existentes
1. En el menú lateral, haz clic en **"Table Editor"**
2. Verifica si estas tablas existen:
   - ✅ `profiles` - ¿Existe?
   - ✅ `pets` - ¿Existe?
   - ✅ `reports` - ¿Existe?
   - ✅ `conversations` - ¿Existe?
   - ✅ `messages` - ¿Existe?

**Anota qué tablas ya existen y cuáles faltan.**

### 1.3. Verificar Políticas RLS
1. En **"Table Editor"**, haz clic en la tabla `profiles`
2. Haz clic en la pestaña **"Policies"** (arriba)
3. Verifica si existen estas políticas:
   - ✅ "Users can view all profiles"
   - ✅ "Users can update own profile"
   - ✅ "Users can insert own profile"

**Si faltan políticas, las crearemos en el siguiente paso.**

### 1.4. Verificar Configuración de Autenticación
1. En el menú lateral, haz clic en **"Authentication"**
2. Haz clic en **"Settings"**
3. Verifica:
   - **Site URL**: ¿Está configurada?
   - **Redirect URLs**: ¿Hay URLs configuradas?
   - **Email Auth**: ¿Está habilitada?

---

## 🎯 PASO 2: Configurar lo que FALTA para Autenticación

### 2.1. Si la tabla `profiles` NO existe

Ve a **SQL Editor** → **New Query** y ejecuta esto:

```sql
-- Crear tabla profiles si no existe
CREATE TABLE IF NOT EXISTS profiles (
    id UUID REFERENCES auth.users(id) ON DELETE CASCADE PRIMARY KEY,
    full_name TEXT,
    avatar_url TEXT,
    phone TEXT,
    location GEOMETRY(POINT, 4326),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Habilitar RLS
ALTER TABLE profiles ENABLE ROW LEVEL SECURITY;

-- Crear políticas (solo si no existen)
DO $$ 
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'profiles' 
        AND policyname = 'Users can view all profiles'
    ) THEN
        CREATE POLICY "Users can view all profiles" 
        ON profiles FOR SELECT USING (true);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'profiles' 
        AND policyname = 'Users can update own profile'
    ) THEN
        CREATE POLICY "Users can update own profile" 
        ON profiles FOR UPDATE USING (auth.uid() = id);
    END IF;

    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'profiles' 
        AND policyname = 'Users can insert own profile'
    ) THEN
        CREATE POLICY "Users can insert own profile" 
        ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
    END IF;
END $$;
```

### 2.2. Si la tabla `profiles` SÍ existe pero faltan políticas

Ejecuta solo la parte de políticas:

```sql
-- Verificar y crear políticas si no existen
DO $$ 
BEGIN
    -- Política de SELECT
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'profiles' 
        AND policyname = 'Users can view all profiles'
    ) THEN
        CREATE POLICY "Users can view all profiles" 
        ON profiles FOR SELECT USING (true);
    END IF;

    -- Política de UPDATE
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'profiles' 
        AND policyname = 'Users can update own profile'
    ) THEN
        CREATE POLICY "Users can update own profile" 
        ON profiles FOR UPDATE USING (auth.uid() = id);
    END IF;

    -- Política de INSERT
    IF NOT EXISTS (
        SELECT 1 FROM pg_policies 
        WHERE tablename = 'profiles' 
        AND policyname = 'Users can insert own profile'
    ) THEN
        CREATE POLICY "Users can insert own profile" 
        ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
    END IF;
END $$;
```

---

## 🔐 PASO 3: Configurar URLs de Redirección (CRÍTICO)

### 3.1. Acceder a Configuración de Autenticación
1. En el menú lateral: **Authentication** → **Settings**

### 3.2. Configurar Site URL
1. Busca el campo **"Site URL"**
2. Configúralo según tu entorno:

**Para desarrollo local:**
```
exp://localhost:8081
```

**O si usas una IP específica (reemplaza con tu IP):**
```
exp://192.168.0.204:8081
```

### 3.3. Configurar Redirect URLs
1. Busca la sección **"Redirect URLs"**
2. Haz clic en **"Add URL"** y agrega estas URLs (una por una):

```
exp://localhost:8081
exp://localhost:8081/--/(auth)/login
exp://localhost:8081/--/(auth)/reset-password
```

**Si usas IP local, también agrega:**
```
exp://192.168.0.204:8081
exp://192.168.0.204:8081/--/(auth)/login
exp://192.168.0.204:8081/--/(auth)/reset-password
```

**⚠️ IMPORTANTE**: Reemplaza `192.168.0.204` con tu IP local real. Para encontrarla:
- Windows: `ipconfig` en CMD
- Mac/Linux: `ifconfig` o `ip addr`

### 3.4. Configurar Email Confirmation (Opcional)

**Para desarrollo rápido:**
1. Busca **"Enable email confirmations"**
2. **Desactívalo** temporalmente (los usuarios podrán iniciar sesión sin confirmar email)

**Para producción:**
- Déjalo **activado** (los usuarios deben confirmar email antes de iniciar sesión)

---

## 📝 PASO 4: Verificar/Crear Archivo .env

### 4.1. Verificar si existe .env
En la raíz de tu proyecto, verifica si existe el archivo `.env`

### 4.2. Si NO existe, créalo:
Crea un archivo `.env` en la raíz del proyecto con:

```env
# Supabase Configuration (Frontend)
EXPO_PUBLIC_SUPABASE_URL=https://eamsbroadstwkrkjcuvo.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImVhbXNicm9hZHN0d2tya2pjdXZvIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NTk3MjQ3ODgsImV4cCI6MjA3NTMwMDc4OH0.bzFaxK25SPMKE5REMxRyK9jPj1n8ocDrn_u6qyMTXEw

# App Configuration
EXPO_PUBLIC_APP_NAME=PetAlert
EXPO_PUBLIC_APP_VERSION=1.0.0
```

**⚠️ NOTA**: Las credenciales ya están en tu código, pero es mejor tenerlas en `.env` por seguridad.

### 4.3. Si ya existe .env
Verifica que tenga estas líneas (puedes actualizar las credenciales si son diferentes):

```env
EXPO_PUBLIC_SUPABASE_URL=https://eamsbroadstwkrkjcuvo.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=tu-clave-completa-aqui
```

---

## ✅ PASO 5: Verificación Final

### 5.1. Verificar en Supabase Dashboard

Ejecuta esta consulta en **SQL Editor** para verificar que todo está bien:

```sql
-- Verificar que la tabla profiles existe y tiene las columnas correctas
SELECT 
    column_name, 
    data_type,
    is_nullable
FROM information_schema.columns 
WHERE table_name = 'profiles'
ORDER BY ordinal_position;

-- Verificar que las políticas RLS existen
SELECT 
    policyname,
    cmd,
    qual
FROM pg_policies 
WHERE tablename = 'profiles';

-- Verificar que RLS está habilitado
SELECT 
    tablename,
    rowsecurity
FROM pg_tables 
WHERE schemaname = 'public' 
AND tablename = 'profiles';
```

**Resultado esperado:**
- Deberías ver las columnas: `id`, `full_name`, `avatar_url`, `phone`, `location`, `created_at`, `updated_at`
- Deberías ver 3 políticas: SELECT, UPDATE, INSERT
- `rowsecurity` debería ser `true`

### 5.2. Probar Registro de Usuario

1. Reinicia tu app:
   ```bash
   npx expo start --clear
   ```

2. Intenta registrarte con un email nuevo
3. Verifica en Supabase:
   - **Authentication** → **Users**: Deberías ver el nuevo usuario
   - **Table Editor** → **profiles**: Deberías ver un perfil creado automáticamente

### 5.3. Probar Login

1. Intenta iniciar sesión con el usuario que acabas de crear
2. Deberías ser redirigido a la pantalla principal

---

## 🐛 Solución de Problemas Específicos

### Problema: "Error al crear perfil automáticamente"

**Causa**: Falta la política de INSERT en `profiles`

**Solución**: Ejecuta el script del Paso 2.2 para crear las políticas faltantes

### Problema: "Redirect URL mismatch"

**Causa**: Las URLs de redirección no están configuradas correctamente

**Solución**: 
1. Ve a **Authentication** → **Settings**
2. Agrega todas las URLs que uses (ver Paso 3.3)
3. Asegúrate de usar la IP correcta

### Problema: "Email not confirmed"

**Causa**: Email confirmation está habilitado pero el usuario no confirmó

**Solución**:
- Opción 1: Desactiva temporalmente "Enable email confirmations" (Paso 3.4)
- Opción 2: Verifica tu email y haz clic en el enlace de confirmación

### Problema: "No se crea el perfil al registrarse"

**Causa**: Falta la política de INSERT o hay un error en la función `ensureProfile`

**Solución**:
1. Verifica las políticas RLS (Paso 5.1)
2. Revisa los logs en Supabase: **Logs** → **Postgres Logs**
3. Verifica que la función `profileService.ensureProfile()` esté siendo llamada

---

## 📋 Checklist de Verificación

Antes de considerar que la autenticación está lista, verifica:

- [ ] Proyecto de Supabase accesible
- [ ] Tabla `profiles` existe
- [ ] Políticas RLS configuradas (3 políticas: SELECT, UPDATE, INSERT)
- [ ] RLS habilitado en `profiles`
- [ ] Site URL configurada en Authentication Settings
- [ ] Redirect URLs configuradas (al menos 3 URLs)
- [ ] Email confirmation configurado según tus necesidades
- [ ] Archivo `.env` creado con credenciales
- [ ] App reiniciada con `--clear`
- [ ] Registro de usuario funciona
- [ ] Perfil se crea automáticamente al registrarse
- [ ] Login funciona correctamente
- [ ] Usuario es redirigido correctamente después de login

---

## 🎯 Resumen: Qué Hacer AHORA

Basándome en tu código, esto es lo que **probablemente necesitas hacer**:

1. ✅ **Verificar** que la tabla `profiles` existe (Paso 1.2)
2. ✅ **Verificar** que las políticas RLS existen (Paso 1.3)
3. ⚠️ **Configurar URLs de redirección** (Paso 3) - **ESTO ES CRÍTICO**
4. ⚠️ **Crear/verificar archivo `.env`** (Paso 4)
5. ✅ **Probar** registro y login (Paso 5)

**Lo más probable es que solo necesites:**
- Configurar las URLs de redirección en Authentication Settings
- Verificar que el archivo `.env` existe

---

## 📞 ¿Necesitas Ayuda?

Si encuentras algún problema:

1. Revisa los **Logs** en Supabase: **Logs** → **Postgres Logs**
2. Revisa la consola de tu app para errores específicos
3. Verifica que todas las políticas RLS estén creadas correctamente

---

**Última actualización**: Guía personalizada basada en tu configuración actual.

