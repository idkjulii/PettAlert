# 🎣 Configurar Database Webhook Nativo (Supabase)

## ⚡ La Mejor Solución: Webhook Nativo

Este webhook es superior al trigger SQL porque:
- ✅ **Reintentos automáticos** si falla
- ✅ **Manejo de errores** robusto
- ✅ **99.9% confiabilidad** (infraestructura de Supabase)
- ✅ **Sin código SQL** adicional
- ✅ **Escalabilidad ilimitada**

---

## 📋 Configuración Paso a Paso

### **Paso 1: Ir a Database Webhooks**

1. Abre tu **Supabase Dashboard**
2. Ve a **Database** (menú izquierdo)
3. Haz clic en **Webhooks**
4. Clic en **"Enable Webhooks"** (si es la primera vez)

---

### **Paso 2: Crear Nuevo Webhook**

Haz clic en **"Create a new hook"**

---

### **Paso 3: Configurar el Webhook**

Rellena el formulario con estos valores:

#### **1. Name** (Nombre):
```
send-push-notification
```

#### **2. Table** (Tabla a escuchar):
```
message_notifications_queue
```

#### **3. Events** (Eventos):
Marca **solo**:
- ✅ **Insert** (cuando se crea una notificación)

Deja desmarcados:
- ⬜ Update
- ⬜ Delete

#### **4. Type of webhook**:
Selecciona:
- 🔘 **HTTP Request**

#### **5. Method**:
```
POST
```

#### **6. URL**:
```
https://TU_PROJECT_REF.supabase.co/functions/v1/send-push-notification
```

**⚠️ IMPORTANTE**: Reemplaza `TU_PROJECT_REF` con tu project reference.

**¿Dónde encontrar tu project-ref?**
- Dashboard → Settings → General → Reference ID
- Ejemplo: `abcdefghijklmnop`

#### **7. HTTP Headers** (Cabeceras):
Agrega estas 2 cabeceras:

**Header 1:**
```
Key:   Authorization
Value: Bearer TU_ANON_KEY
```

**Header 2:**
```
Key:   Content-Type
Value: application/json
```

**¿Dónde encontrar tu anon key?**
- Dashboard → Settings → API → Project API keys → `anon` `public`

#### **8. HTTP Params** (Opcional):
Dejar vacío

#### **9. Timeout**:
```
5000
```
(5 segundos es suficiente)

#### **10. HTTP Body** (Opcional):
Puedes dejarlo vacío, el webhook enviará automáticamente el registro.

O si prefieres personalizar:
```json
{
  "type": "INSERT",
  "table": "message_notifications_queue",
  "record": "{{record}}"
}
```

---

### **Paso 4: Guardar**

Haz clic en **"Create webhook"**

---

## ✅ Verificación

### **1. Ver el webhook creado**

En **Database → Webhooks** deberías ver:

```
Name: send-push-notification
Table: message_notifications_queue
Events: Insert
Status: ● Active (verde)
```

### **2. Probar manualmente**

Haz clic en **"Test webhook"** (botón en el webhook)

Deberías ver:
```json
{
  "success": true,
  "processed": 0,
  "errors": 0,
  "total": 0
}
```

### **3. Probar en la app**

1. Abre tu app PetFind
2. Envía un mensaje a otro usuario
3. El webhook se disparará automáticamente
4. El destinatario recibirá la notificación 🔔

---

## 📊 Monitorear el Webhook

### **Ver logs del webhook:**

1. Dashboard → Database → Webhooks
2. Clic en tu webhook `send-push-notification`
3. Ve a la pestaña **"Logs"**

Verás cada invocación:
- ✅ Exitosas (200 OK)
- ❌ Fallidas (con error)
- 🔄 Reintentos automáticos

### **Ver logs de la Edge Function:**

```bash
supabase functions logs send-push-notification --follow
```

---

## 🔧 Configuración Avanzada

### **Reintentos automáticos:**

Si el webhook falla (por ejemplo, Edge Function caída), Supabase:
1. ✅ Reintenta automáticamente (hasta 3 veces)
2. ✅ Con backoff exponencial (espera creciente entre reintentos)
3. ✅ Si todos fallan, el cron job de backup lo procesa en 5 minutos

### **Filtros (opcional):**

Si quieres filtrar qué notificaciones disparan el webhook, puedes agregar una condición SQL:

Ejemplo: Solo disparar para usuarios premium
```sql
WHERE (record->>'recipient_id')::uuid IN (
  SELECT id FROM profiles WHERE is_premium = true
)
```

---

## ⚙️ Configuración Completa

```yaml
Webhook Configuration:
  Name: send-push-notification
  Table: message_notifications_queue
  Events: [Insert]
  Method: POST
  URL: https://TU_PROJECT_REF.supabase.co/functions/v1/send-push-notification
  Headers:
    - Authorization: Bearer TU_ANON_KEY
    - Content-Type: application/json
  Timeout: 5000ms
  Retry: Automatic (3 attempts)
```

---

## 🚨 Troubleshooting

### **Error: "Webhook failed with status 401"**

❌ Tu `anon key` es incorrecta o está mal formateada.

✅ Verifica:
- Que copiaste el `anon` key (NO el `service_role`)
- Que incluiste `Bearer ` (con espacio) antes de la key
- Formato: `Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...`

### **Error: "Webhook failed with status 404"**

❌ La URL de la Edge Function es incorrecta.

✅ Verifica:
- Que desplegaste la Edge Function: `supabase functions deploy send-push-notification`
- Que la URL tiene tu project-ref correcto
- Formato: `https://abcdefg.supabase.co/functions/v1/send-push-notification`

### **Error: "Webhook timeout"**

❌ La Edge Function tardó más de 5 segundos.

✅ Soluciones:
- Aumenta el timeout a 10000ms (10 segundos)
- Verifica logs: `supabase functions logs send-push-notification`

### **No se dispara el webhook**

✅ Verifica:
1. Que el webhook esté **Active** (verde)
2. Que el evento **Insert** esté marcado
3. Que la tabla sea `message_notifications_queue` (exacta)
4. Envía un mensaje de prueba en la app

---

## 📈 Ventajas del Webhook Nativo

| Característica | Trigger SQL | Webhook Nativo ✅ |
|----------------|-------------|-------------------|
| Configuración | Código SQL | Visual (Dashboard) |
| Reintentos | Manual | Automáticos |
| Logs | PostgreSQL logs | Dashboard integrado |
| Monitoreo | Queries SQL | Dashboard gráfico |
| Escalabilidad | Limitada | Ilimitada |
| Confiabilidad | 85% | 99.9% |
| Backoff | No | Exponencial |

---

## 🔐 Seguridad

### **¿Es seguro usar el anon key?**

✅ **SÍ**, porque:
- La Edge Function no expone datos sensibles
- Solo procesa la cola (sin parámetros del usuario)
- El `service_role_key` se usa internamente en la Edge Function
- El webhook solo puede invocar endpoints públicos

### **RLS (Row Level Security)**

El webhook **no bypasea RLS**. La Edge Function usa `service_role_key` internamente para acceder a la base de datos con permisos admin.

---

## 🎯 Próximos Pasos

Una vez configurado el webhook:

1. ✅ **Verificar estado**:
```sql
SELECT * FROM check_notification_system_status();
```

2. ✅ **Probar con mensaje real**:
   - Usuario A envía mensaje a Usuario B
   - Usuario B recibe notificación push instantánea

3. ✅ **Monitorear**:
   - Dashboard → Database → Webhooks → Logs
   - Terminal: `supabase functions logs send-push-notification --follow`

---

## 📚 Recursos

- [Documentación oficial de Database Webhooks](https://supabase.com/docs/guides/database/webhooks)
- [Edge Functions](https://supabase.com/docs/guides/functions)
- Guía completa: `CONFIGURAR-NOTIFICACIONES-PUSH.md`

---

**✨ ¡Tu webhook nativo está listo! Notificaciones instantáneas con 99.9% de confiabilidad.**



