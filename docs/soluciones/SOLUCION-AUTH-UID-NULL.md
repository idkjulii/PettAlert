# 🔧 Solución: auth.uid() retorna NULL

## ⚠️ Problema

`auth.uid()` retorna `NULL` porque no estás autenticado en el SQL Editor o estás usando un rol sin acceso.

---

## ✅ SOLUCIÓN 1: Obtener tu User ID primero

### **Paso 1: Obtener tu User ID desde la app**

En los logs de la app, busca tu user_id. O ejecuta esta query:

```sql
-- Ver tu user_id (si estás autenticado)
SELECT auth.uid() as mi_user_id;
```

Si retorna NULL, necesitas autenticarte primero.

### **Paso 2: Obtener User ID desde la tabla de usuarios**

```sql
-- Ver usuarios recientes (busca el tuyo por email)
SELECT 
    id,
    email,
    created_at
FROM auth.users
WHERE email = 'julianasellesdelpiano@gmail.com'  -- Tu email
   OR email = 'nydiasdp@gmail.com';  -- O el otro email que usaste
```

Copia el `id` que aparece.

---

## ✅ SOLUCIÓN 2: Crear Preferencias con User ID específico

Una vez que tengas tu user_id, reemplázalo en esta query:

```sql
-- Crear preferencias (reemplaza TU_USER_ID con tu ID real)
INSERT INTO user_alert_preferences (
    user_id,
    enabled,
    radius_meters,
    alert_types,
    species_filter
) VALUES (
    'TU_USER_ID_AQUI'::uuid,  -- ⚠️ Reemplaza con tu user_id
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

---

## ✅ SOLUCIÓN 3: Usar la App (Más Fácil)

**La forma más fácil es usar la app directamente:**

1. **Abre la app** en Expo Go
2. **Ve a Perfil → Alertas Geográficas**
3. **Activa "Rastreo de ubicación"** (esto crea las preferencias automáticamente)
4. **Asegúrate de que "Alertas activas" esté ON**
5. **Configura el radio** (ej: 1km)

El hook `useGeoAlerts` debería crear las preferencias automáticamente cuando abres la pantalla.

---

## ✅ SOLUCIÓN 4: Verificar desde la App

En la app, cuando activas el rastreo, deberías ver en los logs:

```
✅ Ubicación actualizada en servidor
```

Y cuando abres la configuración de alertas, debería crear las preferencias automáticamente.

---

## 🔍 Verificar si se crearon desde la App

Después de activar el rastreo en la app, ejecuta:

```sql
-- Ver todas las preferencias (sin usar auth.uid())
SELECT 
    uap.user_id,
    u.email,
    uap.enabled,
    uap.radius_meters,
    uap.alert_types
FROM user_alert_preferences uap
LEFT JOIN auth.users u ON u.id = uap.user_id
ORDER BY uap.created_at DESC
LIMIT 5;
```

Busca tu email en los resultados.

---

## 🎯 Recomendación

**Usa la app directamente:**
1. Abre la app
2. Ve a Perfil → Alertas Geográficas
3. Activa todo
4. Espera 10 segundos
5. Luego verifica en SQL si se crearon las preferencias

Es más fácil que hacerlo manualmente en SQL.

