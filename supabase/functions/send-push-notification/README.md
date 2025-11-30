# Edge Function: Send Push Notification

Edge Function de Supabase para procesar la cola de notificaciones push y enviarlas a través de Expo.

## 🚀 Funcionamiento

Esta función:
1. Lee notificaciones pendientes de `message_notifications_queue`
2. Obtiene los tokens push del destinatario
3. Envía notificaciones a través de Expo Push API
4. Marca las notificaciones como procesadas
5. Limpia notificaciones antiguas (>7 días)

## 📦 Despliegue

### Requisitos previos:
- Supabase CLI instalado: `npm install -g supabase`
- Autenticado en Supabase: `supabase login`

### Comandos:

```bash
# Vincular proyecto
supabase link --project-ref TU_PROJECT_REF

# Desplegar la función
supabase functions deploy send-push-notification

# Ver logs en tiempo real
supabase functions logs send-push-notification --follow
```

## 🔧 Variables de Entorno

La función usa automáticamente:
- `SUPABASE_URL` - URL de tu proyecto Supabase
- `SUPABASE_SERVICE_ROLE_KEY` - Service role key (con permisos admin)

## 🔗 URL de la función

Una vez desplegada:
```
https://TU_PROJECT_REF.supabase.co/functions/v1/send-push-notification
```

## 🧪 Probar manualmente

```bash
curl -X POST \
  https://TU_PROJECT_REF.supabase.co/functions/v1/send-push-notification \
  -H "Authorization: Bearer TU_ANON_KEY"
```

## 📊 Respuesta exitosa

```json
{
  "success": true,
  "processed": 5,
  "errors": 0,
  "total": 5
}
```

## ⚙️ Invocación automática

Esta función se invoca automáticamente mediante:
1. **Database Webhook** - Cuando se inserta una nueva notificación
2. **pg_cron** - Cada 5 minutos como backup

Ver `backend/migrations/009_notification_system.sql` para la configuración.




