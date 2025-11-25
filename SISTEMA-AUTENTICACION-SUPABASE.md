# 🔐 Sistema Completo de Autenticación con Supabase

## 📋 Resumen

Este documento describe el sistema completo de autenticación implementado con Supabase para la aplicación PetAlert. El sistema incluye registro, inicio de sesión, recuperación de contraseña, y gestión automática de perfiles de usuario.

## 🏗️ Arquitectura

### Componentes Principales

1. **`src/services/supabase.js`** - Cliente de Supabase y servicios de autenticación
2. **`src/stores/authStore.js`** - Store de Zustand para gestión de estado de autenticación
3. **`app/_layout.jsx`** - Layout principal con protección de rutas
4. **`app/(auth)/login.jsx`** - Pantalla de inicio de sesión
5. **`app/(auth)/register.jsx`** - Pantalla de registro
6. **`app/(auth)/forgot-password.jsx`** - Pantalla de recuperación de contraseña

## 🔧 Funcionalidades Implementadas

### 1. Registro de Usuario (`signUp`)

- ✅ Validación de email y contraseña
- ✅ Creación automática de perfil en la tabla `profiles`
- ✅ Envío de email de confirmación
- ✅ Almacenamiento seguro de sesión con `expo-secure-store`

**Flujo:**
```
Usuario completa formulario → signUp() → Supabase crea usuario → 
Perfil se crea automáticamente → Email de confirmación enviado
```

### 2. Inicio de Sesión (`signIn`)

- ✅ Autenticación con email y contraseña
- ✅ Verificación de credenciales
- ✅ Creación automática de perfil si no existe
- ✅ Persistencia de sesión
- ✅ Redirección automática a pantallas protegidas

**Flujo:**
```
Usuario ingresa credenciales → signIn() → Supabase valida → 
Sesión creada → Perfil verificado/creado → Redirección a (tabs)
```

### 3. Recuperación de Contraseña (`resetPassword`)

- ✅ Envío de email de recuperación
- ✅ Validación de email
- ✅ Manejo de errores (rate limiting, etc.)
- ✅ Confirmación visual al usuario

**Flujo:**
```
Usuario ingresa email → resetPassword() → Supabase envía email → 
Usuario recibe link → Actualiza contraseña
```

### 4. Gestión de Sesión

- ✅ Inicialización automática al abrir la app
- ✅ Verificación de sesión existente
- ✅ Refresh automático de tokens
- ✅ Suscripción a cambios de autenticación en tiempo real

### 5. Protección de Rutas

- ✅ Redirección automática según estado de autenticación
- ✅ Rutas protegidas (`(tabs)`) solo accesibles con sesión
- ✅ Rutas públicas (`(auth)`) solo accesibles sin sesión
- ✅ Loading states durante verificación

## 📁 Estructura de Archivos

```
src/
├── services/
│   └── supabase.js          # Cliente Supabase y authService
├── stores/
│   └── authStore.js          # Store de autenticación (Zustand)
app/
├── _layout.jsx              # Layout principal con protección de rutas
└── (auth)/
    ├── login.jsx            # Pantalla de login
    ├── register.jsx         # Pantalla de registro
    └── forgot-password.jsx # Pantalla de recuperación
```

## 🔑 Funciones del authService

### Funciones Principales

```javascript
// Registro
authService.signUp(email, password, fullName)

// Inicio de sesión
authService.signIn(email, password)

// Cerrar sesión
authService.signOut()

// Obtener usuario actual
authService.getCurrentUser()

// Obtener sesión actual
authService.getSession()

// Recuperar contraseña
authService.resetPassword(email)

// Actualizar contraseña
authService.updatePassword(newPassword)

// Reenviar confirmación
authService.resendConfirmation(email)

// Verificar confirmación de email
authService.checkEmailConfirmation()

// Actualizar metadata del usuario
authService.updateUserMetadata(metadata)

// Suscribirse a cambios de autenticación
authService.onAuthStateChange(callback)
```

## 🗄️ Gestión de Perfiles

El sistema crea automáticamente un perfil en la tabla `profiles` cuando:

1. **Registro**: Al registrarse un nuevo usuario
2. **Login**: Al iniciar sesión si el perfil no existe
3. **Inicialización**: Al abrir la app si hay sesión pero no perfil

La función `profileService.ensureProfile()` se encarga de:
- Verificar si el perfil existe
- Crearlo si no existe
- Usar datos del usuario (email, metadata) como valores por defecto

## 🔄 Flujo de Navegación

### Usuario No Autenticado

```
App inicia → _layout.jsx verifica sesión → No hay sesión → 
Redirige a /(auth)/login
```

### Usuario Autenticado

```
App inicia → _layout.jsx verifica sesión → Hay sesión → 
Redirige a /(tabs) (pantalla principal)
```

### Cambios de Autenticación en Tiempo Real

```
Usuario inicia sesión → Supabase emite evento SIGNED_IN → 
Suscripción en _layout.jsx detecta cambio → Actualiza estado → 
Redirige automáticamente
```

## 🔐 Seguridad

### Almacenamiento Seguro

- ✅ Uso de `expo-secure-store` para tokens y sesiones
- ✅ Tokens nunca expuestos en logs
- ✅ Refresh automático de tokens antes de expirar

### Validaciones

- ✅ Validación de formato de email
- ✅ Validación de longitud de contraseña (mínimo 6 caracteres)
- ✅ Manejo de errores específicos de Supabase
- ✅ Rate limiting en recuperación de contraseña

## 📱 Configuración Requerida

### 1. Variables de Entorno

Crea un archivo `.env` en la raíz del proyecto:

```env
EXPO_PUBLIC_SUPABASE_URL=https://tu-proyecto-id.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=tu-clave-anonima-aqui
```

### 2. Configuración en Supabase Dashboard

1. **Authentication > Settings**:
   - Configura URLs de redirección para tu app
   - Habilita email confirmation si lo deseas
   - Configura templates de email

2. **Database**:
   - Asegúrate de que la tabla `profiles` existe
   - Configura RLS (Row Level Security) apropiadamente

### 3. Políticas RLS Recomendadas

```sql
-- Permitir a usuarios ver todos los perfiles
CREATE POLICY "Users can view all profiles" 
ON profiles FOR SELECT USING (true);

-- Permitir a usuarios actualizar su propio perfil
CREATE POLICY "Users can update own profile" 
ON profiles FOR UPDATE USING (auth.uid() = id);

-- Permitir a usuarios insertar su propio perfil
CREATE POLICY "Users can insert own profile" 
ON profiles FOR INSERT WITH CHECK (auth.uid() = id);
```

## 🧪 Uso en Componentes

### Ejemplo: Usar autenticación en un componente

```javascript
import { useAuthStore } from '../src/stores/authStore';

function MyComponent() {
  const { user, session, isAuthenticated, logout } = useAuthStore();
  
  if (!isAuthenticated()) {
    return <Text>No autenticado</Text>;
  }
  
  return (
    <View>
      <Text>Bienvenido {user?.email}</Text>
      <Button onPress={logout}>Cerrar Sesión</Button>
    </View>
  );
}
```

### Ejemplo: Login programático

```javascript
import { useAuthStore } from '../src/stores/authStore';

function LoginButton() {
  const { login, loading } = useAuthStore();
  
  const handleLogin = async () => {
    const result = await login('usuario@email.com', 'password123');
    
    if (result.success) {
      console.log('Login exitoso!');
    } else {
      console.error('Error:', result.error);
    }
  };
  
  return (
    <Button onPress={handleLogin} loading={loading}>
      Iniciar Sesión
    </Button>
  );
}
```

## 🐛 Solución de Problemas

### Error: "Invalid login credentials"

- Verifica que el email y contraseña sean correctos
- Asegúrate de que el email esté confirmado (si email confirmation está habilitado)

### Error: "Email not confirmed"

- El usuario debe verificar su email antes de iniciar sesión
- Usa `resendConfirmation()` para reenviar el email

### Error: "Too many requests"

- Supabase tiene rate limiting
- Espera unos minutos antes de intentar de nuevo

### Sesión no persiste

- Verifica que `expo-secure-store` esté instalado
- Asegúrate de que las credenciales de Supabase estén correctas

### Perfil no se crea automáticamente

- Verifica que la tabla `profiles` existe
- Verifica las políticas RLS
- Revisa los logs de la consola para errores específicos

## 📚 Recursos Adicionales

- [Documentación de Supabase Auth](https://supabase.com/docs/guides/auth)
- [Expo Secure Store](https://docs.expo.dev/versions/latest/sdk/securestore/)
- [Zustand Documentation](https://github.com/pmndrs/zustand)

## ✅ Checklist de Implementación

- [x] Cliente de Supabase configurado
- [x] AuthService con todas las funciones necesarias
- [x] AuthStore con gestión de estado
- [x] Pantallas de login, registro y recuperación
- [x] Protección de rutas en _layout.jsx
- [x] Suscripción a cambios de autenticación
- [x] Creación automática de perfiles
- [x] Manejo de errores completo
- [x] Persistencia de sesión
- [x] Refresh automático de tokens

## 🎯 Próximos Pasos (Opcional)

- [ ] Autenticación con OAuth (Google, Apple, etc.)
- [ ] Autenticación con número de teléfono
- [ ] Verificación de dos factores (2FA)
- [ ] Cambio de email
- [ ] Eliminación de cuenta

---

**Última actualización**: Implementación completa del sistema de autenticación con Supabase.

