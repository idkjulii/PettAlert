# 🚀 Invocar Edge Function Manualmente

## Opción 1: Usando curl (Más simple)

### Paso 1: Obtener Service Role Key
1. Ve a **Supabase Dashboard → Settings → API**
2. Copia el **Service Role Key** (el que dice "secret", no el anon key)

### Paso 2: Ejecutar en PowerShell

```powershell
# Reemplaza TU_SERVICE_ROLE_KEY con el key que copiaste
$headers = @{
    "Authorization" = "Bearer TU_SERVICE_ROLE_KEY"
    "Content-Type" = "application/json"
}

Invoke-RestMethod -Uri "https://eamsbroadstwkrkjcuvo.supabase.co/functions/v1/send-geo-alerts" -Method POST -Headers $headers -Body "{}"
```

---

## Opción 2: Desde Supabase Dashboard

1. Ve a **Supabase Dashboard → Edge Functions**
2. Busca `send-geo-alerts`
3. Click en **"Invoke"** o **"Test"**
4. Click en **"Run"**

---

## Opción 3: Verificar Webhook (Recomendado)

El webhook debería invocar automáticamente la función cuando se crea una alerta. Verifica:

1. Ve a **Supabase Dashboard → Database → Webhooks**
2. Busca el webhook `process-geo-alerts-immediately`
3. Verifica que esté **activo** (toggle verde)
4. Click en el webhook para ver logs

---

## Después de invocar: Verificar que se procesaron

```sql
-- Ver estado de alertas
SELECT 
    ganq.id,
    u.email,
    ganq.distance_meters,
    ganq.notification_data->>'pet_name' as mascota,
    ganq.processed_at,
    CASE 
        WHEN ganq.processed_at IS NULL THEN '⏳ PENDIENTE'
        ELSE '✅ PROCESADA'
    END as estado
FROM geo_alert_notifications_queue ganq
LEFT JOIN auth.users u ON u.id = ganq.recipient_id
WHERE ganq.recipient_id IN (
    '5973ee88-8409-4be6-8884-36a4ad29ad7c',
    'b3b9d127-50e0-4217-8c6b-cc2936b326bb'
)
ORDER BY ganq.created_at DESC;
```

Si `processed_at` tiene un valor, ¡la alerta se procesó correctamente! ✅

