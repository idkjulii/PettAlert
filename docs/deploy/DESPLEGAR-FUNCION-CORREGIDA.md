# 🚀 Desplegar Edge Function Corregida

## Problema encontrado y solucionado

✅ **Error:** `column push_tokens.token does not exist`  
✅ **Solución:** Cambiado `token` por `expo_token` en la Edge Function

---

## Desplegar la función corregida

Ejecuta en PowerShell:

```powershell
npx supabase functions deploy send-geo-alerts --project-ref eamsbroadstwkrkjcuvo
```

---

## Verificar que funcionó

### 1. Crear una nueva alerta

```sql
SELECT enqueue_geo_alerts('5e2bf154-e75d-4823-aa2a-fb9b74f2a94c');
```

### 2. Esperar 10-15 segundos

El webhook debería invocar automáticamente la función.

### 3. Verificar que se procesó

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
LIMIT 1;
```

Si `processed_at` tiene un valor, ¡funcionó! ✅

### 4. Ver logs (opcional)

En Supabase Dashboard → Edge Functions → send-geo-alerts → Logs

Deberías ver:
- ✅ `Procesando alertas...`
- ✅ `Exitosas: 1` (o más)
- ❌ Sin errores de "column does not exist"

---

## Resumen

1. ✅ Problema identificado: columna incorrecta (`token` vs `expo_token`)
2. ✅ Código corregido
3. ⏳ Desplegar función
4. ⏳ Probar creando nueva alerta
5. ⏳ Verificar que se procesa automáticamente

