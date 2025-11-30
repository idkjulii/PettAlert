# 🔧 Configuración del Webhook para Alertas Geográficas

## ✅ Configuración Correcta

### **Paso 1: General**
- **Name:** `process-geo-alerts-immediately`
  - ⚠️ No uses espacios ni caracteres especiales
  - ✅ Usa guiones o guiones bajos

### **Paso 2: Conditions to fire webhook**

**Table:**
- Selecciona: `geo_alert_notifications_queue`

**Events:**
- ✅ **Insert** (marcado)
- ❌ Update (sin marcar)
- ❌ Delete (sin marcar)

### **Paso 3: Webhook configuration**

**Type of webhook:**
- Selecciona: **HTTP Request**

**HTTP Request Configuration:**

#### **Method:**
- Selecciona: `POST`

#### **URL:**
```
https://TU_PROJECT_REF.supabase.co/functions/v1/send-geo-alerts
```

⚠️ **IMPORTANTE:** 
- Reemplaza `TU_PROJECT_REF` con tu Project Ref real
- La URL debe terminar en `/send-geo-alerts` (no cortada)
- Ejemplo completo: `https://eamsbroadstwkrkjcuvo.supabase.co/functions/v1/send-geo-alerts`

#### **Timeout:**
- Cambia de `5000 ms` a `25000 ms` (25 segundos)
- ⚠️ **CRÍTICO:** La Edge Function puede procesar hasta 50 notificaciones y necesita más tiempo

#### **HTTP Headers:**

Agrega estos dos headers:

1. **Content-Type:**
   - Key: `Content-Type`
   - Value: `application/json`

2. **Authorization:**
   - Key: `Authorization`
   - Value: `Bearer TU_SERVICE_ROLE_KEY`
   - ⚠️ Reemplaza `TU_SERVICE_ROLE_KEY` con tu Service Role Key real
   - Puedes encontrarla en: **Dashboard → Settings → API → service_role key**

#### **HTTP Parameters:**
- Deja vacío (no necesitas parámetros)

---

## 📋 Checklist de Configuración

Antes de hacer click en "Create webhook", verifica:

- [ ] **Name:** Sin espacios, solo letras, números y guiones
- [ ] **Table:** `geo_alert_notifications_queue`
- [ ] **Events:** Solo `Insert` marcado
- [ ] **Type:** HTTP Request
- [ ] **Method:** POST
- [ ] **URL:** Completa y correcta (termina en `/send-geo-alerts`)
- [ ] **Timeout:** 25000 ms (25 segundos)
- [ ] **Header 1:** `Content-Type: application/json`
- [ ] **Header 2:** `Authorization: Bearer [TU_SERVICE_ROLE_KEY]`

---

## 🔍 Cómo Obtener tu Service Role Key

1. Ve a **Supabase Dashboard**
2. Click en **Settings** (⚙️) en el menú lateral
3. Click en **API**
4. Busca la sección **Project API keys**
5. Copia el valor de **service_role** (⚠️ NO uses la `anon` key)
6. Pégala en el header Authorization: `Bearer [pega_aquí]`

---

## ✅ Verificar que Funciona

Después de crear el webhook:

### **1. Verificar en Dashboard:**
- Ve a **Database → Webhooks**
- Deberías ver tu webhook listado
- Estado: **Active** (verde)

### **2. Probar con SQL:**

```sql
-- Crear una alerta de prueba
INSERT INTO geo_alert_notifications_queue (
    recipient_id,
    report_id,
    distance_meters,
    notification_data
) VALUES (
    auth.uid(),  -- Tu user ID
    gen_random_uuid(),  -- Un UUID de prueba
    500,
    '{"pet_name": "Test", "type": "lost"}'::jsonb
);

-- Verificar que se procesó (debería tener processed_at)
SELECT 
    id,
    processed_at,
    created_at
FROM geo_alert_notifications_queue
ORDER BY created_at DESC
LIMIT 1;
```

### **3. Ver Logs de la Edge Function:**

```bash
supabase functions logs send-geo-alerts --follow
```

Deberías ver logs cuando se crea una nueva alerta.

---

## 🐛 Troubleshooting

### **Problema: Webhook no se invoca**

**Verifica:**
1. ✅ El webhook está **Active** en Dashboard
2. ✅ La URL es correcta y completa
3. ✅ El Authorization header tiene el `service_role` key (no `anon`)
4. ✅ El timeout es suficiente (25000ms)

**Prueba manualmente:**
```sql
-- Invocar la función directamente
SELECT invoke_geo_alerts_edge_function();
```

### **Problema: Error 401 (Unauthorized)**

- Verifica que el Authorization header tiene el formato correcto: `Bearer [key]`
- Asegúrate de usar el `service_role` key, no el `anon` key

### **Problema: Error 500 (Timeout)**

- Aumenta el timeout a 30000ms (30 segundos)
- Verifica que la Edge Function está desplegada correctamente

### **Problema: Error 404 (Not Found)**

- Verifica que la URL es correcta
- Asegúrate de que la Edge Function está desplegada:
  ```bash
  supabase functions list
  ```
- Deberías ver `send-geo-alerts` en la lista

---

## 📊 Monitoreo del Webhook

### **Ver historial de invocaciones:**

En **Dashboard → Database → Webhooks → [Tu webhook]**, puedes ver:
- Últimas invocaciones
- Estado (success/error)
- Tiempo de respuesta
- Errores (si los hay)

### **Ver logs detallados:**

```bash
# Ver logs en tiempo real
supabase functions logs send-geo-alerts --follow

# Ver últimos 50 logs
supabase functions logs send-geo-alerts --limit 50
```

---

## ✅ Configuración Final Correcta

```
Name: process-geo-alerts-immediately
Table: geo_alert_notifications_queue
Events: Insert ✓
Type: HTTP Request
Method: POST
URL: https://[TU_PROJECT].supabase.co/functions/v1/send-geo-alerts
Timeout: 25000 ms
Headers:
  Content-Type: application/json
  Authorization: Bearer [TU_SERVICE_ROLE_KEY]
```

---

**✨ Una vez configurado correctamente, el sistema enviará notificaciones automáticamente cuando se creen nuevos reportes de mascotas perdidas cerca de usuarios.**

