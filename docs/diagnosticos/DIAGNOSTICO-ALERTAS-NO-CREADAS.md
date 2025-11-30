# 🔍 Diagnóstico: Por Qué No Se Crearon Alertas

## ⚠️ Problema Detectado

No se crearon alertas cuando creaste el reporte. Vamos a diagnosticar por qué.

---

## 🔍 Diagnóstico Paso a Paso

### **Paso 1: Verificar quién creó el reporte**

```sql
-- Ver quién creó el reporte de "Dogo"
SELECT 
    r.id,
    r.type,
    r.pet_name,
    r.reporter_id,
    p.full_name as reporter_name,
    ST_Y(r.location::geometry) as latitude,
    ST_X(r.location::geometry) as longitude,
    r.status
FROM reports r
LEFT JOIN profiles p ON p.id = r.reporter_id
WHERE r.id = '5e2bf154-e75d-4823-aa2a-fb9b74f2a94c';
```

**Verifica:**
- ¿El `reporter_id` es diferente a tu `user_id`?
- Si es el mismo, el sistema NO crea alertas para ti mismo (es normal)

---

### **Paso 2: Ver tu user_id y ubicación**

```sql
-- Ver tu user_id
SELECT auth.uid() as mi_user_id;

-- Ver tu ubicación registrada
SELECT 
    user_id,
    latitude,
    longitude,
    updated_at
FROM user_locations
WHERE user_id = auth.uid();
```

---

### **Paso 3: Calcular distancia entre tu ubicación y el reporte**

```sql
-- Calcular distancia
SELECT 
    ST_Distance(
        (SELECT location FROM user_locations WHERE user_id = auth.uid()),
        (SELECT location FROM reports WHERE id = '5e2bf154-e75d-4823-aa2a-fb9b74f2a94c')
    ) as distancia_metros;
```

**Verifica:**
- ¿La distancia es menor a tu radio configurado? (ej: si configuraste 1km = 1000m)

---

### **Paso 4: Verificar tus preferencias de alertas**

```sql
-- Ver tus preferencias
SELECT 
    user_id,
    enabled,
    radius_meters,
    alert_types,
    species_filter
FROM user_alert_preferences
WHERE user_id = auth.uid();
```

**Verifica:**
- ¿`enabled` es `true`?
- ¿`radius_meters` es suficiente? (ej: si la distancia es 500m, el radio debe ser >= 500m)
- ¿`alert_types` incluye `'lost'`? (el reporte es tipo "lost")
- ¿`species_filter` permite perros? (o es NULL = todas)

---

### **Paso 5: Verificar que el trigger existe y está activo**

```sql
-- Verificar trigger
SELECT 
    tgname as trigger_name,
    tgenabled as enabled,
    tgrelid::regclass as table_name
FROM pg_trigger
WHERE tgname = 'trigger_geo_alerts_on_new_report';
```

**Deberías ver:**
- `trigger_name`: `trigger_geo_alerts_on_new_report`
- `enabled`: `O` (O = enabled, D = disabled)

---

### **Paso 6: Probar crear alertas manualmente**

```sql
-- Crear alertas manualmente para el reporte
SELECT enqueue_geo_alerts('5e2bf154-e75d-4823-aa2a-fb9b74f2a94c');
```

**Esto debería retornar:**
- Un número (cantidad de alertas creadas)
- Si retorna 0, significa que no hay usuarios cercanos que cumplan los criterios

---

### **Paso 7: Ver todos los usuarios con ubicación activa**

```sql
-- Ver usuarios con ubicación (últimas 24h)
SELECT 
    ul.user_id,
    p.full_name,
    ul.latitude,
    ul.longitude,
    ul.updated_at,
    uap.enabled as alertas_habilitadas,
    uap.radius_meters
FROM user_locations ul
LEFT JOIN profiles p ON p.id = ul.user_id
LEFT JOIN user_alert_preferences uap ON uap.user_id = ul.user_id
WHERE ul.updated_at > NOW() - INTERVAL '24 hours'
ORDER BY ul.updated_at DESC;
```

---

## 🎯 Causas Más Comunes

### **1. Creaste el reporte con tu propia cuenta**
- **Solución:** Crea el reporte desde otra cuenta (segundo celular/usuario)

### **2. Distancia mayor al radio configurado**
- **Solución:** Aumenta el radio o crea el reporte más cerca

### **3. Alertas deshabilitadas**
- **Solución:** Activa "Alertas activas" en la app

### **4. Filtro de tipo no coincide**
- **Solución:** Verifica que tienes "Mascotas perdidas" seleccionado

### **5. Filtro de especie**
- **Solución:** Verifica que tienes "Perros" seleccionado (o todas las especies)

### **6. Ubicación no está registrada**
- **Solución:** Activa "Rastreo de ubicación" en la app

---

## ✅ Query Completa de Diagnóstico

Ejecuta esta query completa para ver todo:

```sql
-- DIAGNÓSTICO COMPLETO
WITH reporte_info AS (
    SELECT 
        r.id as report_id,
        r.type as report_type,
        r.pet_name,
        r.reporter_id,
        r.location as report_location,
        ST_Y(r.location::geometry) as report_lat,
        ST_X(r.location::geometry) as report_lng
    FROM reports r
    WHERE r.id = '5e2bf154-e75d-4823-aa2a-fb9b74f2a94c'
),
mi_ubicacion AS (
    SELECT 
        user_id,
        location as my_location,
        latitude as my_lat,
        longitude as my_lng,
        updated_at
    FROM user_locations
    WHERE user_id = auth.uid()
),
mi_preferencias AS (
    SELECT 
        enabled,
        radius_meters,
        alert_types,
        species_filter
    FROM user_alert_preferences
    WHERE user_id = auth.uid()
)
SELECT 
    'Reporte' as tipo,
    r.report_type as valor,
    'Tipo de reporte creado' as descripcion
FROM reporte_info r
UNION ALL
SELECT 
    'Mi User ID'::text,
    auth.uid()::text,
    'Tu ID de usuario'::text
UNION ALL
SELECT 
    'Reporter ID'::text,
    r.reporter_id::text,
    'ID del que creó el reporte'::text
FROM reporte_info r
UNION ALL
SELECT 
    '¿Soy el reporter?'::text,
    CASE WHEN r.reporter_id = auth.uid() THEN 'SÍ (no se crean alertas para uno mismo)' ELSE 'NO' END,
    'Si eres tú, no se crean alertas'::text
FROM reporte_info r
UNION ALL
SELECT 
    'Distancia (metros)'::text,
    ROUND(ST_Distance(m.my_location, r.report_location))::text,
    'Distancia entre tu ubicación y el reporte'::text
FROM reporte_info r, mi_ubicacion m
UNION ALL
SELECT 
    'Radio configurado'::text,
    COALESCE(p.radius_meters, 1000)::text,
    'Radio máximo para alertas'::text
FROM mi_preferencias p
UNION ALL
SELECT 
    '¿Dentro del radio?'::text,
    CASE 
        WHEN ST_Distance(m.my_location, r.report_location) <= COALESCE(p.radius_meters, 1000) 
        THEN 'SÍ' 
        ELSE 'NO' 
    END,
    'Si la distancia es menor al radio'::text
FROM reporte_info r, mi_ubicacion m, mi_preferencias p
UNION ALL
SELECT 
    'Alertas habilitadas'::text,
    CASE WHEN p.enabled THEN 'SÍ' ELSE 'NO' END,
    'Si tienes alertas activas'::text
FROM mi_preferencias p
UNION ALL
SELECT 
    'Tipo permitido'::text,
    CASE 
        WHEN r.report_type = ANY(COALESCE(p.alert_types, ARRAY['lost']::text[])) 
        THEN 'SÍ' 
        ELSE 'NO' 
    END,
    'Si el tipo del reporte está en tus preferencias'::text
FROM reporte_info r, mi_preferencias p;
```

Esta query te mostrará exactamente por qué no se crearon alertas.

