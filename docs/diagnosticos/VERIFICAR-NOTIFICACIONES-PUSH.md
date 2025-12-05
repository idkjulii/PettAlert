# 🔍 Verificación del Sistema de Notificaciones Push

## ✅ Cambios Aplicados

### 1. Filtro en el Frontend
Se ha actualizado `src/hooks/usePushNotifications.js` para:
- **NO mostrar notificaciones** cuando el usuario actual es el emisor del mensaje
- Filtrar notificaciones en dos niveles:
  1. `setNotificationHandler`: Decide si mostrar la notificación antes de que aparezca
  2. `addNotificationReceivedListener`: Log adicional para debugging

### 2. Código del Filtro
```javascript
Notifications.setNotificationHandler({
  handleNotification: async (notification) => {
    const senderId = notification?.request?.content?.data?.sender_id;
    const currentUserId = useAuthStore.getState()?.user?.id;
    
    // Solo mostrar si NO soy el emisor
    const shouldShow = senderId && currentUserId && senderId !== currentUserId;
    
    return {
      shouldShowAlert: shouldShow,
      shouldShowBanner: shouldShow,
      shouldShowList: shouldShow,
      shouldPlaySound: shouldShow,
      shouldSetBadge: shouldShow,
    };
  },
});
```

## 🧪 Cómo Probar

### Paso 1: Recargar la Aplicación
1. En la terminal de Expo, presiona `r` para recargar
2. O cierra completamente la app y vuelve a abrirla

### Paso 2: Probar con Dos Dispositivos
1. **Dispositivo A**: Usuario A envía un mensaje a Usuario B
2. **Dispositivo A**: NO debe mostrar notificación (es el emisor)
3. **Dispositivo B**: SÍ debe mostrar notificación (es el receptor)

### Paso 3: Verificar Logs
En la terminal de Expo, busca:
```
✅ Notificación de otro usuario recibida  <- Solo en dispositivo receptor
🚫 Notificación del mismo usuario, ignorando  <- Si aparece, el filtro funciona
```

## 🔧 Verificar Base de Datos

Para confirmar que las notificaciones se están encolando correctamente:

```sql
-- Ver notificaciones en cola
SELECT 
  mnq.id,
  mnq.message_id,
  mnq.recipient_id,
  mnq.payload->>'sender_id' as sender_id,
  mnq.payload->>'content' as content,
  mnq.processed_at,
  mnq.created_at,
  p.email as recipient_email
FROM message_notifications_queue mnq
LEFT JOIN profiles p ON p.id = mnq.recipient_id
ORDER BY mnq.created_at DESC
LIMIT 20;
```

**Verificar que:**
- `recipient_id` ≠ `sender_id` (el receptor NO es el emisor)
- Las notificaciones se procesan (`processed_at` tiene valor)

## 🐛 Si Sigue Sin Funcionar

### Problema 1: El otro dispositivo NO recibe notificaciones

Verificar que el token push esté registrado:
```sql
-- Ver tokens registrados
SELECT 
  pt.user_id,
  pt.expo_token,
  pt.platform,
  pt.created_at,
  p.email
FROM push_tokens pt
LEFT JOIN profiles p ON p.id = pt.user_id
ORDER BY pt.created_at DESC;
```

### Problema 2: Las notificaciones NO se procesan

Verificar que la Edge Function esté funcionando:
```sql
-- Buscar notificaciones pendientes antiguas
SELECT 
  COUNT(*) as pendientes,
  MIN(created_at) as mas_antigua
FROM message_notifications_queue
WHERE processed_at IS NULL;
```

Si hay notificaciones pendientes de hace más de 1 minuto, la Edge Function no se está invocando.

### Problema 3: Errores en la Edge Function

Ver logs en Supabase Dashboard:
1. Dashboard > Edge Functions > `send-push-notification`
2. Ver logs de ejecución
3. Buscar errores

## 📱 URL Actualizada

**IMPORTANTE**: Asegúrate de que la app esté usando la nueva URL:
```
https://received-investments-riders-cope.trycloudflare.com
```

Para verificar en los logs de Expo, busca:
```
BACKEND_URL final: https://received-investments-riders-cope.trycloudflare.com
```

Si ves la URL antigua, recarga la app con `r` en la terminal de Expo.

## ✅ Checklist

- [ ] App recargada completamente
- [ ] URL del backend correcta en los logs
- [ ] Tokens push registrados para ambos usuarios
- [ ] Notificaciones solo aparecen en el receptor
- [ ] El emisor NO ve notificaciones de sus propios mensajes

