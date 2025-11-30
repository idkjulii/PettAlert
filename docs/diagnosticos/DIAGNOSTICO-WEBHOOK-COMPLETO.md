# 🔍 Diagnóstico Completo del Webhook

## Problema: Webhook configurado pero no procesa alertas

### Posibles causas:

1. **Webhook no está activo** (toggle desactivado)
2. **Edge Function está fallando** (errores en la función)
3. **Permisos insuficientes** (RLS bloqueando)
4. **Webhook no se está invocando** (problema de configuración)

---

## Pasos de Diagnóstico

### 1. Verificar que el webhook esté activo

En la página del webhook, busca un toggle o switch que diga "Active" o "Enabled". Debe estar en verde.

### 2. Ver logs del webhook

En la página del webhook, busca:
- "Logs"
- "History" 
- "Recent invocations"
- "Activity"

Si no hay logs, el webhook no se está invocando.

### 3. Invocar Edge Function manualmente

Para verificar si la función funciona:

**Obtén tu Service Role Key:**
1. Dashboard → Settings → API
2. Copia el `service_role` key

**Invoca la función en PowerShell:**

```powershell
$headers = @{
    "Authorization" = "Bearer TU_SERVICE_ROLE_KEY"
    "Content-Type" = "application/json"
}

Invoke-RestMethod -Uri "https://eamsbroadstwkrkjcuvo.supabase.co/functions/v1/send-geo-alerts" -Method POST -Headers $headers -Body "{}"
```

### 4. Ver logs de la Edge Function

```powershell
npx supabase functions logs send-geo-alerts --project-ref eamsbroadstwkrkjcuvo
```

### 5. Verificar alertas pendientes

```sql
-- Ver alertas pendientes
SELECT 
    COUNT(*) as total_pendientes,
    MIN(created_at) as mas_antigua,
    MAX(created_at) as mas_reciente
FROM geo_alert_notifications_queue
WHERE processed_at IS NULL;
```

---

## Solución Temporal: Procesar Manualmente

Mientras diagnosticamos, puedes procesar las alertas manualmente:

```sql
-- Invocar función manualmente (si está configurada)
SELECT invoke_geo_alerts_edge_function();
```

O desde PowerShell:

```powershell
# Con tu Service Role Key
$headers = @{
    "Authorization" = "Bearer TU_SERVICE_ROLE_KEY"
    "Content-Type" = "application/json"
}

Invoke-RestMethod -Uri "https://eamsbroadstwkrkjcuvo.supabase.co/functions/v1/send-geo-alerts" -Method POST -Headers $headers -Body "{}"
```

---

## Verificar Resultado

Después de invocar manualmente:

```sql
SELECT 
    ganq.id,
    ganq.processed_at,
    ganq.created_at,
    CASE 
        WHEN ganq.processed_at IS NULL THEN '⏳ PENDIENTE'
        ELSE '✅ PROCESADA'
    END as estado
FROM geo_alert_notifications_queue ganq
WHERE ganq.recipient_id = 'b3b9d127-50e0-4217-8c6b-cc2936b326bb'
ORDER BY ganq.created_at DESC
LIMIT 5;
```

Si `processed_at` tiene valor, la función funciona y el problema es el webhook.

