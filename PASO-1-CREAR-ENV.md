# 📝 PASO 1: Crear archivo .env

## ¿Qué necesitas?

Antes de continuar, necesitas tener:
1. **SUPABASE_URL**: La URL de tu proyecto Supabase (ejemplo: `https://xxxxx.supabase.co`)
2. **SUPABASE_SERVICE_KEY**: La clave de servicio (service_role key) de Supabase

## Instrucciones

### Opción A: Crear manualmente

1. Ve a la carpeta `backend`
2. Copia el archivo `env.example` y renómbralo a `.env`
3. Edita el archivo `.env` con tus credenciales reales

### Opción B: Usar PowerShell (Windows)

```powershell
cd backend
copy env.example .env
notepad .env
```

Luego edita el archivo con tus credenciales.

## Contenido del archivo .env

```env
SUPABASE_URL=https://TU-PROYECTO-ID.supabase.co
SUPABASE_SERVICE_KEY=tu-clave-service-role-aqui
ALLOWED_ORIGINS=*
GENERATE_EMBEDDINGS_LOCALLY=true
```

## ⚠️ IMPORTANTE

- NO subas el archivo `.env` a Git (debe estar en `.gitignore`)
- Guarda tus credenciales de forma segura
- La `SUPABASE_SERVICE_KEY` debe ser la clave de **service_role**, no la anon key

## ✅ Verificación

Una vez creado, verifica que el archivo existe:
```powershell
Test-Path backend\.env
```

Debería devolver `True`.

---

**¿Ya tienes el archivo .env creado?** 
- Si SÍ → Continúa al PASO 2
- Si NO → Crea el archivo primero y luego continúa


