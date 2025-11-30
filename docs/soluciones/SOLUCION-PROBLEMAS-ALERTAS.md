# 🔧 Solución: Problemas Detectados

## ⚠️ Problemas Encontrados

1. **Distancia = NULL** → No tienes ubicación registrada en la BD
2. **No hay preferencias** → No tienes configuración de alertas creada

---

## ✅ SOLUCIÓN 1: Verificar y Crear Ubicación

### **Paso 1: Verificar si tienes ubicación**

```sql
-- Ver tu ubicación
SELECT 
    user_id,
    latitude,
    longitude,
    updated_at
FROM user_locations
WHERE user_id = auth.uid();
```

Si no retorna nada, necesitas registrar tu ubicación.

### **Paso 2: Registrar ubicación manualmente (temporal)**

```sql
-- Registrar tu ubicación (usa las coordenadas de tu ubicación actual)
SELECT * FROM upsert_user_location(
    auth.uid(),
    -27.475333,  -- Tu latitud (ajusta según tu ubicación)
    -58.851961,  -- Tu longitud (ajusta según tu ubicación)
    20.0         -- Precisión en metros
);
```

**O mejor:** Activa el rastreo en la app y espera a que se actualice automáticamente.

---

## ✅ SOLUCIÓN 2: Crear Preferencias de Alertas

### **Paso 1: Crear preferencias manualmente**

```sql
-- Crear preferencias por defecto
INSERT INTO user_alert_preferences (
    user_id,
    enabled,
    radius_meters,
    alert_types,
    species_filter
) VALUES (
    auth.uid(),
    true,
    1000,
    ARRAY['lost']::text[],
    NULL  -- NULL = todas las especies
)
ON CONFLICT (user_id) DO UPDATE SET
    enabled = true,
    radius_meters = COALESCE(user_alert_preferences.radius_meters, 1000),
    alert_types = COALESCE(user_alert_preferences.alert_types, ARRAY['lost']::text[]);
```

### **Paso 2: Verificar que se crearon**

```sql
SELECT * FROM user_alert_preferences WHERE user_id = auth.uid();
```

---

## ✅ SOLUCIÓN 3: Activar desde la App

**En la app:**
1. Ve a **Perfil → Alertas Geográficas**
2. Activa **"Rastreo de ubicación"** (esto registra tu ubicación)
3. Asegúrate de que **"Alertas activas"** esté ON
4. Configura el radio (ej: 1km)
5. Espera unos segundos para que se actualice

---

## ✅ SOLUCIÓN 4: Probar Crear Alertas Manualmente

Una vez que tengas ubicación y preferencias:

```sql
-- Intentar crear alertas para el reporte de "Dogo"
SELECT enqueue_geo_alerts('5e2bf154-e75d-4823-aa2a-fb9b74f2a94c');
```

Esto debería retornar `1` (una alerta creada para ti).

---

## 🔍 Verificación Completa

Ejecuta esta query después de hacer los pasos anteriores:

```sql
-- Verificar todo
SELECT 
    'Ubicación registrada' as item,
    CASE WHEN EXISTS (SELECT 1 FROM user_locations WHERE user_id = auth.uid()) 
         THEN 'SÍ ✅' ELSE 'NO ❌' END as estado
UNION ALL
SELECT 
    'Preferencias creadas',
    CASE WHEN EXISTS (SELECT 1 FROM user_alert_preferences WHERE user_id = auth.uid()) 
         THEN 'SÍ ✅' ELSE 'NO ❌' END
UNION ALL
SELECT 
    'Alertas habilitadas',
    CASE WHEN COALESCE((SELECT enabled FROM user_alert_preferences WHERE user_id = auth.uid()), true)
         THEN 'SÍ ✅' ELSE 'NO ❌' END
UNION ALL
SELECT 
    'Distancia al reporte',
    COALESCE(
        ROUND(ST_Distance(
            (SELECT location FROM user_locations WHERE user_id = auth.uid()),
            (SELECT location FROM reports WHERE id = '5e2bf154-e75d-4823-aa2a-fb9b74f2a94c')
        ))::text,
        'Sin ubicación'
    ) || ' metros';
```

---

## 🎯 Orden de Acción Recomendado

1. **En la app:** Activa "Rastreo de ubicación" y "Alertas activas"
2. **Espera 10 segundos** para que se actualice
3. **En SQL:** Ejecuta la query de verificación completa
4. **Si aún no funciona:** Crea preferencias manualmente con la query de arriba
5. **Prueba crear alertas:** `SELECT enqueue_geo_alerts('5e2bf154-e75d-4823-aa2a-fb9b74f2a94c');`

---

## 📝 Nota Importante

El hook `useGeoAlerts` debería crear las preferencias automáticamente cuando abres la pantalla de configuración. Si no se crearon, puede ser que:
- No hayas abierto la pantalla de configuración aún
- O hubo un error al guardar

La solución más rápida es crear las preferencias manualmente con la query de arriba.

