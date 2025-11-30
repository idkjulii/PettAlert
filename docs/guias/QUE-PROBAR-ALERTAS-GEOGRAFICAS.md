# 🧪 Qué Probar: Sistema de Alertas Geográficas

## 🎯 Checklist de Pruebas

### **PASO 1: Verificar que la App Funciona**

#### **1.1 Abrir la App**
- [ ] La app se abre sin errores
- [ ] Puedes hacer login/registro
- [ ] Puedes navegar por las pantallas

#### **1.2 Verificar Navegación**
- [ ] Puedes ir a la tab de **Perfil**
- [ ] Ves tu información de usuario

---

### **PASO 2: Configurar Alertas Geográficas**

#### **2.1 Acceder a la Configuración**
- [ ] En Perfil, hay un botón **"Alertas Geográficas"**
  - Si no está, agrégalo siguiendo `INSTRUCCIONES-AGREGAR-BOTON-PERFIL.md`
- [ ] Al tocar el botón, se abre la pantalla de configuración

#### **2.2 Activar Rastreo de Ubicación**
- [ ] Toca el switch **"Activar rastreo"**
- [ ] Te pide permisos de ubicación
- [ ] Aceptas los permisos
- [ ] Aparece: **"📍 Última actualización: HH:MM:SS"**
- [ ] Puedes tocar **"Actualizar ahora"** y se actualiza

#### **2.3 Verificar en Base de Datos**
En Supabase Dashboard → SQL Editor, ejecuta:

```sql
-- Ver tu ubicación registrada
SELECT 
    user_id,
    latitude,
    longitude,
    accuracy,
    updated_at
FROM user_locations
WHERE user_id = auth.uid();
```

**Deberías ver:**
- ✅ Tu ubicación (latitud y longitud)
- ✅ Precisión (accuracy)
- ✅ Fecha de actualización reciente

#### **2.4 Verificar Preferencias**
```sql
-- Ver tus preferencias de alertas
SELECT * FROM user_alert_preferences WHERE user_id = auth.uid();
```

**Deberías ver:**
- ✅ `enabled: true`
- ✅ `radius_meters: 1000` (o el que configuraste)
- ✅ `alert_types: ['lost']` (o los que seleccionaste)

---

### **PASO 3: Configurar Preferencias de Alertas**

#### **3.1 Radio de Alertas**
- [ ] Puedes cambiar el radio (500m, 1km, 2km, 5km)
- [ ] El cambio se guarda correctamente

#### **3.2 Tipos de Alertas**
- [ ] Puedes seleccionar "Mascotas perdidas" y/o "Mascotas encontradas"
- [ ] Los cambios se guardan

#### **3.3 Filtro de Especies**
- [ ] Puedes seleccionar especies (Perros, Gatos, etc.)
- [ ] O dejar todas seleccionadas

---

### **PASO 4: Crear Reporte de Prueba**

#### **4.1 Crear Reporte Cercano**
En Supabase Dashboard → SQL Editor, ejecuta:

```sql
-- IMPORTANTE: Reemplaza las coordenadas con ubicaciones cercanas a ti
-- (a menos de 1km de distancia)

INSERT INTO reports (
    type,
    reporter_id,
    pet_name,
    species,
    breed,
    color,
    size,
    description,
    location,
    address,
    status,
    incident_date
) VALUES (
    'lost',
    auth.uid(),  -- O el ID de otro usuario
    'Max',
    'dog',
    'Golden Retriever',
    'Dorado',
    'large',
    'Perro muy amigable, responde a Max',
    ST_SetSRID(ST_MakePoint(-58.382000, -34.604000), 4326)::geography,
    -- ⚠️ Reemplaza con coordenadas cercanas a tu ubicación
    'Av. de Prueba 123',
    'active',
    NOW()
) RETURNING id;
```

**Nota:** Ajusta las coordenadas para que estén cerca de tu ubicación actual.

#### **4.2 Verificar que se Crearon Alertas**
```sql
-- Ver alertas creadas para ti
SELECT 
    id,
    recipient_id,
    report_id,
    distance_meters,
    notification_data->>'pet_name' as mascota,
    processed_at,
    created_at
FROM geo_alert_notifications_queue
WHERE recipient_id = auth.uid()
ORDER BY created_at DESC
LIMIT 5;
```

**Deberías ver:**
- ✅ Al menos 1 alerta creada
- ✅ `distance_meters` menor a tu radio configurado (ej: < 1000m)
- ✅ `notification_data` con información de la mascota

---

### **PASO 5: Verificar Notificación Push**

#### **5.1 Recibir Notificación**
- [ ] **Deberías recibir una notificación push** en tu teléfono
- [ ] Título: **"🐾 Mascota perdida cerca de ti"**
- [ ] Cuerpo: **"Max · Perro · Golden Retriever a 0.5km. Av. de Prueba 123"**

#### **5.2 Verificar que se Procesó**
```sql
-- Ver alertas procesadas
SELECT 
    id,
    processed_at,
    created_at,
    notification_data->>'pet_name' as mascota
FROM geo_alert_notifications_queue
WHERE recipient_id = auth.uid()
  AND processed_at IS NOT NULL
ORDER BY processed_at DESC
LIMIT 5;
```

**Deberías ver:**
- ✅ `processed_at` con un timestamp reciente
- ✅ La alerta fue procesada y enviada

#### **5.3 Ver Logs de Edge Function**
En PowerShell:

```powershell
npx supabase functions logs send-geo-alerts --project-ref eamsbroadstwkrkjcuvo --follow
```

**Deberías ver:**
- ✅ Logs de procesamiento
- ✅ Mensajes como "✅ Alerta X procesada exitosamente"
- ✅ Sin errores

---

### **PASO 6: Probar Filtros**

#### **6.1 Filtro por Radio**
1. Configura radio a **500m**
2. Crea reporte a **1km** de distancia
3. **No deberías recibir notificación** (está fuera del radio)
4. Crea reporte a **300m** de distancia
5. **SÍ deberías recibir notificación** (está dentro del radio)

#### **6.2 Filtro por Tipo**
1. Configura solo **"Mascotas perdidas"**
2. Crea reporte tipo **"found"**
3. **No deberías recibir notificación**
4. Crea reporte tipo **"lost"**
5. **SÍ deberías recibir notificación**

#### **6.3 Filtro por Especie**
1. Configura solo **"Perros"**
2. Crea reporte de **gato**
3. **No deberías recibir notificación**
4. Crea reporte de **perro**
5. **SÍ deberías recibir notificación**

---

### **PASO 7: Verificar Estadísticas**

En Supabase Dashboard → SQL Editor:

```sql
SELECT * FROM get_geo_alerts_stats();
```

**Después de probar, deberías ver:**
- ✅ **Usuarios con ubicación:** 1 (o más si probaste con otros usuarios)
- ✅ **Usuarios con alertas activas:** 1 (o más)
- ✅ **Alertas enviadas hoy:** 1 o más (depende de cuántas pruebas hiciste)
- ✅ **Radio promedio:** 1000 metros (o el que configuraste)

---

## 🐛 Qué Hacer Si Algo No Funciona

### **No recibo notificaciones:**
1. Verifica que tienes tokens push:
   ```sql
   SELECT * FROM push_tokens WHERE user_id = auth.uid();
   ```
2. Verifica que tu ubicación está registrada:
   ```sql
   SELECT * FROM user_locations WHERE user_id = auth.uid();
   ```
3. Verifica que las alertas están habilitadas:
   ```sql
   SELECT enabled FROM user_alert_preferences WHERE user_id = auth.uid();
   ```
4. Verifica logs de Edge Function:
   ```powershell
   npx supabase functions logs send-geo-alerts --project-ref eamsbroadstwkrkjcuvo
   ```

### **No se crean alertas:**
1. Verifica que el reporte tiene ubicación:
   ```sql
   SELECT id, type, location FROM reports WHERE id = 'REPORT_ID';
   ```
2. Verifica que el trigger existe:
   ```sql
   SELECT * FROM pg_trigger WHERE tgname = 'trigger_geo_alerts_on_new_report';
   ```
3. Crea alertas manualmente:
   ```sql
   SELECT enqueue_geo_alerts('REPORT_ID');
   ```

### **Ubicación no se actualiza:**
1. Verifica permisos en el dispositivo (Settings → Apps → PetAlert → Permissions)
2. Verifica que el rastreo está activado en la app
3. Prueba "Actualizar ahora" manualmente

---

## ✅ Resumen: Qué Deberías Ver

### **En la App:**
- ✅ Pantalla de configuración de alertas
- ✅ Switch para activar rastreo
- ✅ Información de última actualización de ubicación
- ✅ Opciones para configurar radio, tipos, especies

### **En la Base de Datos:**
- ✅ Tu ubicación en `user_locations`
- ✅ Tus preferencias en `user_alert_preferences`
- ✅ Alertas creadas en `geo_alert_notifications_queue`
- ✅ Alertas procesadas (con `processed_at`)

### **En tu Teléfono:**
- ✅ Notificación push cuando se crea un reporte cercano
- ✅ Título y mensaje con información de la mascota
- ✅ Distancia al reporte

### **En los Logs:**
- ✅ Logs de Edge Function procesando alertas
- ✅ Mensajes de éxito
- ✅ Sin errores

---

## 🎯 Orden de Pruebas Recomendado

1. **Primero:** Verificar que la app funciona y puedes acceder a configuración
2. **Segundo:** Activar rastreo de ubicación y verificar en BD
3. **Tercero:** Crear reporte de prueba cercano
4. **Cuarto:** Verificar que recibes notificación push
5. **Quinto:** Probar filtros (radio, tipo, especie)

---

**✨ Sigue este checklist y sabrás exactamente qué está funcionando y qué no.**

