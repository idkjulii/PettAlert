# 🎯 Guía Paso a Paso: Solucionar Todo

## 📋 Resumen de lo que vamos a hacer

1. ✅ Obtener tu User ID
2. ✅ Crear preferencias de alertas
3. ✅ Verificar/crear ubicación
4. ✅ Probar que se crean alertas
5. ✅ Hacer build con EAS (opcional, para notificaciones)

---

## 📍 PASO 1: Obtener tu User ID

### **En Supabase Dashboard → SQL Editor, ejecuta:**

```sql
-- Buscar tu user_id por email
SELECT 
    id as user_id,
    email,
    created_at
FROM auth.users 
WHERE email IN (
    'julianasellesdelpiano@gmail.com',
    'nydiasdp@gmail.com'
)
ORDER BY created_at DESC;
```

**Copia el `user_id` que aparece** (es un UUID como `ff29f934-25b9-4fcd-ac66-bbfcc51d7c68`)

---

## 📍 PASO 2: Crear Preferencias de Alertas

### **En SQL Editor, ejecuta (reemplaza TU_USER_ID con el que copiaste):**

```sql
-- Crear preferencias de alertas
INSERT INTO user_alert_preferences (
    user_id,
    enabled,
    radius_meters,
    alert_types,
    species_filter
) VALUES (
    'TU_USER_ID'::uuid,  -- ⚠️ Pega aquí tu user_id
    true,
    1000,
    ARRAY['lost']::text[],
    NULL
)
ON CONFLICT (user_id) DO UPDATE SET
    enabled = true,
    radius_meters = COALESCE(EXCLUDED.radius_meters, user_alert_preferences.radius_meters),
    alert_types = COALESCE(EXCLUDED.alert_types, user_alert_preferences.alert_types);
```

**Deberías ver:** "Success. No rows returned" o "1 row inserted"

### **Verificar que se crearon:**

```sql
-- Verificar preferencias
SELECT 
    user_id,
    enabled,
    radius_meters,
    alert_types,
    species_filter
FROM user_alert_preferences
WHERE user_id = 'TU_USER_ID'::uuid;  -- Tu user_id
```

**Deberías ver:** 1 fila con tus preferencias

---

## 📍 PASO 3: Verificar/Crear Ubicación

### **3.1 Verificar si tienes ubicación:**

```sql
-- Ver tu ubicación
SELECT 
    user_id,
    latitude,
    longitude,
    updated_at
FROM user_locations
WHERE user_id = 'TU_USER_ID'::uuid;  -- Tu user_id
```

### **3.2 Si NO tienes ubicación, créala:**

**Opción A: Desde la app (Recomendado)**
1. Abre la app
2. Ve a **Perfil → Alertas Geográficas**
3. Activa **"Rastreo de ubicación"**
4. Acepta permisos
5. Espera 10 segundos
6. Verifica en SQL de nuevo

**Opción B: Manualmente en SQL**

```sql
-- Registrar ubicación manualmente
-- ⚠️ IMPORTANTE: Ajusta las coordenadas según tu ubicación actual
SELECT * FROM upsert_user_location(
    'TU_USER_ID'::uuid,  -- Tu user_id
    -27.475333,  -- Tu latitud (ajusta según tu ubicación)
    -58.851961,  -- Tu longitud (ajusta según tu ubicación)
    20.0         -- Precisión en metros
);
```

**Para obtener tus coordenadas actuales:**
- En los logs de la app, busca: `📍 Ubicación obtenida: -27.475333, -58.851961`
- O usa Google Maps para obtener tus coordenadas

### **3.3 Verificar que se guardó:**

```sql
-- Verificar ubicación
SELECT 
    user_id,
    latitude,
    longitude,
    updated_at
FROM user_locations
WHERE user_id = 'TU_USER_ID'::uuid;
```

**Deberías ver:** Tu ubicación con timestamp reciente

---

## 📍 PASO 4: Probar Crear Alertas

### **4.1 Calcular distancia al reporte:**

```sql
-- Calcular distancia entre tu ubicación y el reporte de "Dogo"
SELECT 
    ROUND(ST_Distance(
        (SELECT location FROM user_locations WHERE user_id = 'TU_USER_ID'::uuid),
        (SELECT location FROM reports WHERE id = '5e2bf154-e75d-4823-aa2a-fb9b74f2a94c')
    )) as distancia_metros;
```

**Verifica:**
- Si la distancia es menor a 1000m (1km), debería crearse la alerta
- Si es mayor, aumenta el radio en las preferencias o crea un reporte más cerca

### **4.2 Crear alertas manualmente:**

```sql
-- Crear alertas para el reporte de "Dogo"
SELECT enqueue_geo_alerts('5e2bf154-e75d-4823-aa2a-fb9b74f2a94c');
```

**Deberías ver:** Un número (ej: `1` = una alerta creada)

### **4.3 Verificar que se creó la alerta:**

```sql
-- Ver alertas creadas para ti
SELECT 
    id,
    recipient_id,
    report_id,
    distance_meters,
    notification_data->>'pet_name' as mascota,
    notification_data->>'type' as tipo,
    processed_at,
    created_at
FROM geo_alert_notifications_queue
WHERE recipient_id = 'TU_USER_ID'::uuid
ORDER BY created_at DESC
LIMIT 5;
```

**Deberías ver:** Al menos 1 alerta con el reporte de "Dogo"

---

## 📍 PASO 5: Verificar que se Procesó

### **Ver alertas procesadas:**

```sql
-- Ver alertas procesadas
SELECT 
    id,
    distance_meters,
    notification_data->>'pet_name' as mascota,
    processed_at,
    created_at
FROM geo_alert_notifications_queue
WHERE recipient_id = 'TU_USER_ID'::uuid
  AND processed_at IS NOT NULL
ORDER BY created_at DESC
LIMIT 5;
```

**Si `processed_at` tiene un valor:** La alerta se procesó y se intentó enviar ✅

**Si `processed_at` es NULL:** La alerta está pendiente (el webhook puede no estar funcionando)

---

## 📍 PASO 6: Verificar Webhook (Si processed_at es NULL)

### **Ver logs de Edge Function:**

En PowerShell:

```powershell
npx supabase functions logs send-geo-alerts --project-ref eamsbroadstwkrkjcuvo --follow
```

**Deberías ver:** Logs de procesamiento cuando se crean alertas

---

## 📍 PASO 7: Hacer Build con EAS (Para Notificaciones Reales)

### **7.1 Instalar EAS CLI:**

```powershell
npm install -g eas-cli
```

### **7.2 Login en Expo:**

```powershell
eas login
```

(Si no tienes cuenta, créala gratis)

### **7.3 Configurar proyecto:**

```powershell
eas build:configure
```

### **7.4 Generar APK:**

```powershell
eas build --platform android --profile preview
```

**Esto:**
- Compilará la app en la nube
- Tardará 10-15 minutos
- Te dará un link para descargar el APK

### **7.5 Instalar APK:**

1. Descarga el APK desde el link
2. Instálalo en tu teléfono
3. Abre la app
4. Activa alertas geográficas
5. Crea un reporte de prueba
6. **Deberías recibir notificación push** 🎉

---

## ✅ Checklist Final

Antes de considerar que todo funciona:

- [ ] Preferencias creadas en `user_alert_preferences`
- [ ] Ubicación registrada en `user_locations`
- [ ] Alertas se crean cuando ejecutas `enqueue_geo_alerts()`
- [ ] Alertas se procesan (`processed_at` tiene valor)
- [ ] Build con EAS generado (opcional, para notificaciones)

---

## 🐛 Si Algo No Funciona

### **Preferencias no se crean:**
- Verifica que el user_id es correcto
- Verifica que no hay error de sintaxis en la query

### **Ubicación no se registra:**
- Activa el rastreo en la app
- Espera 10 segundos
- Verifica permisos de ubicación en el dispositivo

### **Alertas no se crean:**
- Verifica distancia (debe ser menor al radio)
- Verifica que el tipo del reporte está en `alert_types`
- Verifica que `enabled = true`

### **Alertas no se procesan:**
- Verifica que el webhook está activo en Dashboard
- Verifica logs de Edge Function
- Invoca manualmente: `SELECT invoke_geo_alerts_edge_function();`

---

## 📝 Resumen de Queries (Copia y Pega)

```sql
-- 1. Obtener user_id
SELECT id, email FROM auth.users WHERE email = 'TU_EMAIL';

-- 2. Crear preferencias (reemplaza TU_USER_ID)
INSERT INTO user_alert_preferences (user_id, enabled, radius_meters, alert_types)
VALUES ('TU_USER_ID'::uuid, true, 1000, ARRAY['lost']::text[])
ON CONFLICT (user_id) DO UPDATE SET enabled = true;

-- 3. Verificar preferencias
SELECT * FROM user_alert_preferences WHERE user_id = 'TU_USER_ID'::uuid;

-- 4. Registrar ubicación (ajusta coordenadas)
SELECT * FROM upsert_user_location('TU_USER_ID'::uuid, -27.475333, -58.851961, 20.0);

-- 5. Verificar ubicación
SELECT * FROM user_locations WHERE user_id = 'TU_USER_ID'::uuid;

-- 6. Calcular distancia
SELECT ROUND(ST_Distance(
    (SELECT location FROM user_locations WHERE user_id = 'TU_USER_ID'::uuid),
    (SELECT location FROM reports WHERE id = '5e2bf154-e75d-4823-aa2a-fb9b74f2a94c')
)) as distancia_metros;

-- 7. Crear alertas manualmente
SELECT enqueue_geo_alerts('5e2bf154-e75d-4823-aa2a-fb9b74f2a94c');

-- 8. Ver alertas creadas
SELECT * FROM geo_alert_notifications_queue 
WHERE recipient_id = 'TU_USER_ID'::uuid 
ORDER BY created_at DESC LIMIT 5;
```

---

**✨ Sigue estos pasos en orden y todo debería funcionar!**

