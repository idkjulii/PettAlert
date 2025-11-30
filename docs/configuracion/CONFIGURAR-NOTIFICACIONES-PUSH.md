# 🔔 Configuración del Sistema de Notificaciones Push

Sistema completo de notificaciones push en tiempo real para PetFind usando Expo + Supabase Edge Functions.

## 📋 Arquitectura del Sistema

```
Usuario envía mensaje
        ↓
Trigger DB encola notificación
        ↓
┌───────────────────────────────────────┐
│  DUAL INVOCATION SYSTEM               │
├───────────────────────────────────────┤
│  1. Database Webhook (Tiempo Real)   │ ← 99.9% confiable
│     └─► Invoca Edge Function         │   Reintentos automáticos
│                                       │
│  2. pg_cron Backup (Cada 5 min)      │
│     └─► Procesa notificaciones       │
│         pendientes o fallidas         │
└───────────────────────────────────────┘
        ↓
Edge Function procesa cola
        ↓
Envía a Expo Push API
        ↓
Usuario recibe notificación 📱
```

## 🚀 Pasos de Instalación

### **Paso 1: Instalar Supabase CLI**

```bash
# Instalar CLI globalmente
npm install -g supabase

# Verificar instalación
supabase --version
```

### **Paso 2: Autenticarse en Supabase**

```bash
# Login con tu cuenta de Supabase
supabase login

# Te pedirá generar un access token desde:
# https://app.supabase.com/account/tokens
```

### **Paso 3: Vincular tu Proyecto**

```bash
# Desde la raíz del proyecto
cd C:\Users\maria\OneDrive\Escritorio\lpm\petFindnoborres

# Vincular con tu proyecto de Supabase
supabase link --project-ref TU_PROJECT_REF

# Puedes encontrar tu project-ref en:
# Supabase Dashboard > Settings > General > Reference ID
```

### **Paso 4: Configurar Variables de Entorno en Supabase**

Ve a tu **Supabase Dashboard**:

1. **Dashboard** → **Settings** → **Database** → **Custom PostgreSQL Configuration**

2. Agrega estas configuraciones:

```sql
-- Variable 1: URL de tu proyecto
app.supabase_url = 'https://TU_PROJECT_REF.supabase.co'

-- Variable 2: Service Role Key (Dashboard > Settings > API > service_role key)
app.supabase_service_role_key = 'tu_service_role_key_aqui'
```

⚠️ **IMPORTANTE**: Usa el **service_role key**, NO el anon key.

### **Paso 5: Habilitar extensión pg_net**

En **SQL Editor** de Supabase Dashboard:

```sql
-- Habilitar extensión para llamadas HTTP
CREATE EXTENSION IF NOT EXISTS pg_net;
```

### **Paso 6: Ejecutar Migración SQL**

Opción A - Desde Supabase Dashboard:

```sql
-- Copiar y pegar el contenido de:
-- backend/migrations/009_notification_system.sql
-- en el SQL Editor de Supabase y ejecutar
```

Opción B - Usando CLI:

```bash
supabase db push
```

### **Paso 7: Desplegar Edge Function**

```bash
# Desplegar la función
supabase functions deploy send-push-notification

# Verificar que se desplegó correctamente
supabase functions list
```

### **Paso 8: Configurar Database Webhook** ⭐

Este es el **componente clave** para notificaciones en tiempo real.

**Dashboard → Database → Webhooks → Create a new hook**

Configuración:
```yaml
Name: send-push-notification
Table: message_notifications_queue
Events: [Insert]
Method: POST
URL: https://TU_PROJECT_REF.supabase.co/functions/v1/send-push-notification
Headers:
  - Authorization: Bearer TU_ANON_KEY
  - Content-Type: application/json
Timeout: 5000ms
```

📖 **Guía detallada paso a paso**: Ver `CONFIGURAR-WEBHOOK.md`

**¿Por qué webhook nativo?**
- ✅ Reintentos automáticos (3 intentos)
- ✅ 99.9% de confiabilidad
- ✅ Logs integrados en Dashboard
- ✅ Backoff exponencial
- ✅ Escalabilidad ilimitada

## ✅ Verificación del Sistema

### **1. Verificar en SQL Editor**

```sql
-- Ver estado del sistema
SELECT * FROM check_notification_system_status();

-- Ver cron jobs activos
SELECT * FROM cron.job;

-- Ver notificaciones pendientes
SELECT COUNT(*) as pendientes 
FROM message_notifications_queue 
WHERE processed_at IS NULL;
```

### **2. Probar Edge Function manualmente**

```bash
# Desde terminal
curl -X POST \
  https://TU_PROJECT_REF.supabase.co/functions/v1/send-push-notification \
  -H "Authorization: Bearer TU_ANON_KEY" \
  -H "Content-Type: application/json"
```

### **3. Ver Logs en Tiempo Real**

```bash
# Ver logs de la Edge Function
supabase functions logs send-push-notification --follow
```

### **4. Probar con un mensaje real**

1. Abre tu app PetFind
2. Envía un mensaje a otro usuario
3. Verifica que el destinatario reciba la notificación push

## 🔍 Troubleshooting

### **Problema: No se envían notificaciones**

```sql
-- 1. Verificar que hay notificaciones en cola
SELECT * FROM message_notifications_queue 
WHERE processed_at IS NULL 
LIMIT 5;

-- 2. Verificar que hay tokens registrados
SELECT COUNT(*) FROM push_tokens;

-- 3. Ver logs de errores
SELECT * FROM message_notifications_queue 
ORDER BY created_at DESC 
LIMIT 10;
```

### **Problema: Edge Function falla**

```bash
# Ver logs detallados
supabase functions logs send-push-notification --follow

# Redesplegar función
supabase functions deploy send-push-notification --no-verify-jwt
```

### **Problema: Cron jobs no funcionan**

```sql
-- Verificar que pg_cron está habilitado
SELECT * FROM pg_extension WHERE extname = 'pg_cron';

-- Ver cron jobs
SELECT * FROM cron.job;

-- Eliminar y recrear cron job
SELECT cron.unschedule('process-push-notifications-backup');

SELECT cron.schedule(
  'process-push-notifications-backup',
  '*/5 * * * *',
  'SELECT invoke_push_notification_edge_function();'
);
```

### **Problema: Variables de configuración no existen**

```sql
-- Verificar variables
SHOW app.supabase_url;
SHOW app.supabase_service_role_key;

-- Si no existen, configurarlas:
-- Dashboard > Settings > Database > Custom PostgreSQL Configuration
```

## 🔧 Funciones Útiles

### **Reprocesar notificaciones fallidas**

```sql
-- Reintentar notificaciones con más de 10 minutos sin procesar
SELECT retry_failed_notifications(10);
```

### **Limpiar notificaciones antiguas**

```sql
-- Eliminar notificaciones procesadas de hace más de 7 días
DELETE FROM message_notifications_queue
WHERE processed_at IS NOT NULL
  AND processed_at < NOW() - INTERVAL '7 days';
```

### **Desactivar sistema temporalmente**

```sql
-- Desactivar trigger (para mantenimiento)
ALTER TABLE message_notifications_queue 
DISABLE TRIGGER trigger_process_notification_immediately;

-- Reactivar
ALTER TABLE message_notifications_queue 
ENABLE TRIGGER trigger_process_notification_immediately;
```

## 📊 Monitoreo

### **Dashboard personalizado en Supabase**

```sql
-- Consulta para dashboard
SELECT 
  COUNT(*) FILTER (WHERE processed_at IS NULL) as pendientes,
  COUNT(*) FILTER (WHERE processed_at IS NOT NULL AND processed_at > NOW() - INTERVAL '1 hour') as ultima_hora,
  COUNT(*) FILTER (WHERE processed_at IS NOT NULL AND processed_at > NOW() - INTERVAL '24 hours') as ultimo_dia,
  COUNT(*) as total
FROM message_notifications_queue;
```

### **Métricas de usuarios activos**

```sql
-- Usuarios con notificaciones habilitadas
SELECT 
  COUNT(DISTINCT user_id) as usuarios_con_tokens,
  COUNT(*) as total_tokens,
  COUNT(*) FILTER (WHERE platform = 'android') as android,
  COUNT(*) FILTER (WHERE platform = 'ios') as ios
FROM push_tokens;
```

## 🎯 Siguiente Paso

Una vez configurado, las notificaciones funcionarán automáticamente:

1. ✅ Cuando alguien envía un mensaje → notificación instantánea
2. ✅ Cron job cada 5 minutos → procesa notificaciones fallidas
3. ✅ Limpieza automática → elimina notificaciones antiguas

## 📱 Probar en la App

1. Usuario A envía mensaje a Usuario B
2. Usuario B debería recibir notificación push inmediatamente
3. Si la app está cerrada, la notificación aparece en la bandeja del sistema
4. Al tocar la notificación, abre la conversación directamente

## 🔐 Seguridad

- ✅ RLS habilitado en todas las tablas
- ✅ Service role key solo en backend/Edge Functions
- ✅ Los usuarios solo pueden ver sus propios tokens
- ✅ La cola de notificaciones no es accesible directamente

## 💰 Costos

### Supabase Edge Functions:
- **Gratis**: Hasta 500K invocaciones/mes
- Tu app probablemente usará: ~10-100K/mes
- ✅ **Completamente gratis para tu caso de uso**

### Expo Push Notifications:
- ✅ **Completamente gratis** (sin límites)

---

## 📞 Soporte

Si tienes problemas:
1. Revisa los logs: `supabase functions logs send-push-notification --follow`
2. Verifica el estado: `SELECT * FROM check_notification_system_status();`
3. Revisa la documentación: `supabase/functions/send-push-notification/README.md`

¡Tu sistema de notificaciones está listo! 🎉

