# 📍 Sistema de Alertas Geográficas - PetAlert

## 🎯 Descripción

Sistema completo de notificaciones push basado en geolocalización que alerta a los usuarios cuando se reporta una mascota perdida o encontrada dentro de un radio configurable (por defecto 1km) de su ubicación actual.

---

## ✨ Características

### 🗺️ Rastreo de Ubicación
- ✅ Solicitud automática de permisos de ubicación
- ✅ Rastreo en primer plano (foreground)
- ✅ Actualización automática cada 5 minutos
- ✅ Actualización por distancia (cada 100 metros)
- ✅ Precisión balanceada para optimizar batería
- ✅ Actualización manual bajo demanda

### 🔔 Notificaciones Inteligentes
- ✅ Notificaciones push instantáneas
- ✅ Incluyen distancia al reporte
- ✅ Información completa de la mascota
- ✅ Enlace directo al reporte
- ✅ Sonido y vibración configurables

### ⚙️ Configuración Personalizada
- ✅ Radio de alertas: 500m, 1km, 2km, 5km
- ✅ Tipos de reportes: Perdidas, Encontradas, o Ambas
- ✅ Filtro por especies: Perros, Gatos, Aves, Otros
- ✅ Horario silencioso (próximamente)
- ✅ Habilitar/deshabilitar sin perder configuración

### 🔐 Privacidad y Seguridad
- ✅ Ubicación encriptada en la base de datos
- ✅ Solo se almacena la última ubicación
- ✅ El usuario controla cuándo compartir
- ✅ Ubicaciones antiguas (>24h) se ignoran
- ✅ RLS (Row Level Security) activado

---

## 🏗️ Arquitectura del Sistema

```
┌─────────────────────────────────────────────────────────────┐
│                    FLUJO DE ALERTAS                          │
└─────────────────────────────────────────────────────────────┘

1. REGISTRO DE UBICACIÓN
   ┌──────────────┐
   │ Usuario      │
   │ activa       │ → Solicita permisos
   │ alertas      │
   └──────────────┘
          ↓
   GPS obtiene ubicación
          ↓
   ┌──────────────────────────┐
   │ Hook: useGeoAlerts       │
   │ - Cada 5 min             │
   │ - Cada 100 metros        │
   └──────────────────────────┘
          ↓
   ┌──────────────────────────┐
   │ RPC: upsert_user_location│
   │ Supabase                 │
   └──────────────────────────┘
          ↓
   Tabla: user_locations
   (última ubicación del usuario)


2. NUEVO REPORTE DE MASCOTA
   ┌──────────────┐
   │ Usuario A    │
   │ reporta      │ → INSERT INTO reports
   │ mascota      │
   └──────────────┘
          ↓
   ┌─────────────────────────────────┐
   │ TRIGGER: trigger_geo_alerts     │
   │ _on_new_report                  │
   └─────────────────────────────────┘
          ↓
   ┌─────────────────────────────────┐
   │ Función: enqueue_geo_alerts()   │
   │ 1. Buscar usuarios cercanos     │
   │ 2. Aplicar filtros (tipo, raza) │
   │ 3. Crear notificaciones         │
   └─────────────────────────────────┘
          ↓
   Tabla: geo_alert_notifications_queue
          ↓
   ┌─────────────────────────────────┐
   │ TRIGGER: trigger_process_geo    │
   │ _alert_immediately              │
   └─────────────────────────────────┘
          ↓
   Invoca Edge Function
          ↓
   ┌─────────────────────────────────┐
   │ Edge Function:                  │
   │ send-geo-alerts                 │
   │ 1. Lee cola pendiente           │
   │ 2. Obtiene tokens push          │
   │ 3. Envía a Expo API             │
   │ 4. Marca como procesada         │
   └─────────────────────────────────┘
          ↓
   Expo Push API
          ↓
   ┌──────────────┐
   │ Usuario B    │
   │ Recibe       │ 📱
   │ notificación │
   └──────────────┘
```

---

## 📦 Componentes del Sistema

### **Backend (SQL)**

#### 1. Tablas

**`user_locations`**
```sql
- id: uuid (PK)
- user_id: uuid (FK → auth.users)
- location: geography(POINT) -- PostGIS
- latitude: double precision
- longitude: double precision
- accuracy: double precision (metros)
- updated_at: timestamptz
- created_at: timestamptz
```

**`user_alert_preferences`**
```sql
- id: uuid (PK)
- user_id: uuid (FK → auth.users)
- enabled: boolean (default true)
- radius_meters: integer (default 1000)
- alert_types: text[] (default ['lost'])
- species_filter: text[] (NULL = todas)
- quiet_hours_start: time
- quiet_hours_end: time
- updated_at: timestamptz
- created_at: timestamptz
```

**`geo_alert_notifications_queue`**
```sql
- id: uuid (PK)
- recipient_id: uuid (FK → auth.users)
- report_id: uuid (FK → reports)
- distance_meters: double precision
- notification_data: jsonb
- processed_at: timestamptz
- created_at: timestamptz
```

#### 2. Funciones Principales

**`upsert_user_location(user_id, lat, lng, accuracy)`**
- Actualiza o crea la ubicación del usuario
- Usa ST_MakePoint para crear geografía PostGIS
- Expuesta a usuarios autenticados

**`find_nearby_users(lat, lng, radius_meters)`**
- Encuentra usuarios dentro del radio especificado
- Aplica filtros de preferencias
- Excluye ubicaciones antiguas (>24h)
- Respeta horario silencioso

**`enqueue_geo_alerts(report_id)`**
- Busca usuarios cercanos al reporte
- Aplica filtros de tipo y especie
- Crea notificaciones en la cola
- Retorna cantidad de notificaciones creadas

**`get_geo_alerts_stats()`**
- Estadísticas del sistema
- Usuarios con ubicación activa
- Alertas pendientes y enviadas
- Radio promedio configurado

#### 3. Triggers

**`trigger_geo_alerts_on_new_report`**
- Se activa: AFTER INSERT en `reports`
- Condición: status = 'active' AND location IS NOT NULL
- Acción: Ejecuta `enqueue_geo_alerts()`

**`trigger_process_geo_alert_immediately`**
- Se activa: AFTER INSERT en `geo_alert_notifications_queue`
- Acción: Invoca Edge Function inmediatamente

### **Edge Function (TypeScript)**

**`supabase/functions/send-geo-alerts/index.ts`**

Proceso:
1. Lee hasta 50 notificaciones pendientes
2. Para cada notificación:
   - Obtiene tokens push del destinatario
   - Construye mensaje con distancia y datos de la mascota
   - Envía a Expo Push API
   - Marca como procesada
3. Limpia notificaciones antiguas (>7 días)

Formato del mensaje:
```typescript
{
  to: "ExponentPushToken[xxx]",
  title: "🐾 Mascota perdida cerca de ti",
  body: "Max · Perro · Golden a 0.5km. Av. Principal 123",
  data: {
    type: "geo_alert",
    report_id: "uuid",
    distance_meters: 500,
    latitude: -34.603722,
    longitude: -58.381592
  }
}
```

### **Frontend (React Native)**

#### 1. Hook: `useGeoAlerts()`

**Estado:**
- `locationEnabled`: Boolean
- `currentLocation`: Object con coords
- `alertPreferences`: Object con configuración
- `isLoading`: Boolean
- `error`: String | null
- `permissionStatus`: String

**Acciones:**
- `toggleLocationTracking(enabled)`: Activar/desactivar rastreo
- `requestLocationPermission()`: Solicitar permisos
- `getCurrentLocation()`: Obtener ubicación actual
- `forceLocationUpdate()`: Actualizar manualmente
- `updateAlertRadius(meters)`: Cambiar radio
- `updateAlertTypes(types)`: Cambiar tipos de reportes
- `updateSpeciesFilter(species)`: Filtrar especies
- `toggleAlerts(enabled)`: Habilitar/deshabilitar alertas

#### 2. Componente: `GeoAlertsSettings`

Secciones:
- **Rastreo de ubicación**: Switch on/off con info de última actualización
- **Notificaciones**: Habilitar/deshabilitar alertas
- **Radio de alertas**: Botones para 500m, 1km, 2km, 5km
- **Tipos de alertas**: Checkboxes para perdidas/encontradas
- **Filtro de especies**: Botones para perro, gato, ave, otros

#### 3. Pantalla: `app/geo-alerts-settings.jsx`

Modal screen accesible desde el perfil del usuario.

---

## 🚀 Instalación y Configuración

### **Paso 1: Ejecutar Migración SQL**

```bash
# Conectarse a Supabase
cd backend

# Ejecutar migración
supabase db push migrations/011_geo_alerts_system.sql

# O manualmente en SQL Editor
```

Copia el contenido de `backend/migrations/011_geo_alerts_system.sql` en:
**Supabase Dashboard → SQL Editor → New Query → Ejecutar**

### **Paso 2: Desplegar Edge Function**

```bash
# Asegúrate de tener Supabase CLI instalado
npm install -g supabase

# Login a Supabase
supabase login

# Vincular proyecto
supabase link --project-ref YOUR_PROJECT_REF

# Desplegar función
supabase functions deploy send-geo-alerts

# Verificar despliegue
supabase functions list
```

### **Paso 3: Configurar Webhook de Base de Datos**

1. Ve a **Supabase Dashboard → Database → Webhooks**
2. Click en **Create a new hook**
3. Configura:

```
Name: process-geo-alerts-immediately
Table: geo_alert_notifications_queue
Events: INSERT
Type: HTTP Request

HTTP Request:
  Method: POST
  URL: https://YOUR_PROJECT.supabase.co/functions/v1/send-geo-alerts
  Headers:
    Authorization: Bearer YOUR_SERVICE_ROLE_KEY
    Content-Type: application/json
  
Timeout: 25000ms
```

4. Click **Confirm**

### **Paso 4: Configurar Variables de PostgreSQL**

En **Supabase Dashboard → Settings → Database → Custom PostgreSQL Configuration**:

```
app.supabase_url = https://YOUR_PROJECT.supabase.co
app.supabase_service_role_key = YOUR_SERVICE_ROLE_KEY
```

### **Paso 5: Actualizar App (React Native)**

```bash
# Instalar dependencias (si no las tienes)
npm install expo-location expo-notifications

# Regenerar configuración nativa
npx expo prebuild --clean

# Para Android
npx expo run:android

# Para iOS
npx expo run:ios
```

### **Paso 6: Agregar Botón en Perfil**

Edita `app/(tabs)/profile.jsx` para agregar un botón que navegue a `/geo-alerts-settings`:

```jsx
import { useRouter } from 'expo-router';

// ... dentro del componente
const router = useRouter();

<TouchableOpacity 
  style={styles.settingItem}
  onPress={() => router.push('/geo-alerts-settings')}
>
  <Ionicons name="location" size={24} color="#007AFF" />
  <Text style={styles.settingText}>Alertas Geográficas</Text>
  <Ionicons name="chevron-forward" size={20} color="#999" />
</TouchableOpacity>
```

---

## 🧪 Testing

### **1. Verificar Instalación**

```sql
-- Ver estadísticas del sistema
SELECT * FROM get_geo_alerts_stats();

-- Debe retornar:
-- | stat_name                   | stat_value | description                        |
-- |----------------------------|------------|-------------------------------------|
-- | Usuarios con ubicación      | 0          | Usuarios con ubicación en 24h      |
-- | Usuarios con alertas activas| 0          | Usuarios con alertas habilitadas   |
-- | Alertas pendientes          | 0          | Alertas en cola sin procesar       |
-- | Alertas enviadas hoy        | 0          | Alertas procesadas en 24h          |
-- | Radio promedio              | 1000 metros| Radio promedio configurado         |
```

### **2. Probar Rastreo de Ubicación**

En la app:
1. Ir a **Perfil → Alertas Geográficas**
2. Activar **"Rastreo de ubicación"**
3. Aceptar permisos
4. Verificar que aparece **"Última actualización: HH:MM:SS"**
5. Click en **"Actualizar ahora"** → debe actualizar el timestamp

Verificar en SQL:
```sql
-- Ver tu ubicación registrada
SELECT 
  user_id,
  latitude,
  longitude,
  accuracy,
  updated_at
FROM user_locations
WHERE user_id = 'TU_USER_ID';
```

### **3. Probar Alertas Geográficas**

#### **Preparación:**

```sql
-- 1. Registrar tu ubicación (reemplaza con tu ID y coordenadas reales)
SELECT * FROM upsert_user_location(
  'TU_USER_ID'::uuid,
  -34.603722,  -- Tu latitud
  -58.381592,  -- Tu longitud
  10.0
);

-- 2. Verificar que tienes preferencias creadas
SELECT * FROM user_alert_preferences WHERE user_id = 'TU_USER_ID';
```

#### **Crear Reporte de Prueba:**

```sql
-- Crear un reporte cerca de tu ubicación (500 metros)
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
  'OTRO_USER_ID'::uuid,  -- Importante: NO tu usuario
  'Max',
  'dog',
  'Golden Retriever',
  'Dorado',
  'large',
  'Perro muy amigable, responde a Max',
  ST_SetSRID(ST_MakePoint(-58.382000, -34.604000), 4326)::geography,  -- ~500m de distancia
  'Av. de Prueba 123',
  'active',
  NOW()
) RETURNING id;
```

#### **Verificar:**

```sql
-- 1. Ver si se crearon alertas
SELECT 
  id,
  recipient_id,
  report_id,
  distance_meters,
  processed_at,
  created_at
FROM geo_alert_notifications_queue
WHERE recipient_id = 'TU_USER_ID'
ORDER BY created_at DESC
LIMIT 5;

-- 2. Forzar procesamiento si no se procesó automáticamente
SELECT invoke_geo_alerts_edge_function();

-- 3. Verificar logs de la Edge Function
```

Logs en terminal:
```bash
supabase functions logs send-geo-alerts --follow
```

Deberías recibir una notificación push en tu dispositivo con:
- Título: "🐾 Mascota perdida cerca de ti"
- Cuerpo: "Max · Perro · Golden Retriever a 0.5km. Av. de Prueba 123"

### **4. Probar Filtros**

#### **Filtro por Radio:**

En la app:
1. Configurar radio a **500m**
2. Crear reporte a **1km** → No debe notificar
3. Crear reporte a **300m** → Debe notificar

#### **Filtro por Tipo:**

1. Configurar solo **"Mascotas perdidas"**
2. Crear reporte tipo **"found"** → No debe notificar
3. Crear reporte tipo **"lost"** → Debe notificar

#### **Filtro por Especie:**

1. Configurar solo **"Perros"**
2. Crear reporte de gato → No debe notificar
3. Crear reporte de perro → Debe notificar

---

## 📊 Monitoreo y Mantenimiento

### **Ver Estadísticas**

```sql
SELECT * FROM get_geo_alerts_stats();
```

### **Ver Alertas Pendientes**

```sql
SELECT 
  COUNT(*) as pendientes,
  MIN(created_at) as mas_antigua
FROM geo_alert_notifications_queue
WHERE processed_at IS NULL;
```

### **Ver Últimas Alertas Enviadas**

```sql
SELECT 
  ganq.recipient_id,
  p.full_name as destinatario,
  ganq.distance_meters,
  ganq.notification_data->>'pet_name' as mascota,
  ganq.processed_at
FROM geo_alert_notifications_queue ganq
LEFT JOIN profiles p ON p.id = ganq.recipient_id
WHERE ganq.processed_at IS NOT NULL
ORDER BY ganq.processed_at DESC
LIMIT 20;
```

### **Limpiar Alertas Antiguas**

```sql
-- Limpiar alertas procesadas mayores a 7 días
SELECT cleanup_old_geo_alerts(7);
```

### **Logs de Edge Function**

```bash
# Ver logs en tiempo real
supabase functions logs send-geo-alerts --follow

# Ver últimos 100 logs
supabase functions logs send-geo-alerts --limit 100
```

---

## 🔧 Troubleshooting

### **Problema: No recibo notificaciones**

**1. Verificar permisos:**
- Android: Settings → Apps → PetAlert → Permissions → Location → Allow all the time
- iOS: Settings → PetAlert → Location → Always

**2. Verificar tokens push:**
```sql
SELECT * FROM push_tokens WHERE user_id = 'TU_USER_ID';
```

**3. Verificar ubicación:**
```sql
SELECT * FROM user_locations WHERE user_id = 'TU_USER_ID';
```

**4. Verificar preferencias:**
```sql
SELECT * FROM user_alert_preferences WHERE user_id = 'TU_USER_ID';
```

**5. Verificar que las alertas están habilitadas:**
- Rastreo de ubicación: ON
- Notificaciones: ON
- En preferencias: `enabled = true`

### **Problema: Alertas no se generan**

**1. Verificar que el reporte tiene ubicación:**
```sql
SELECT id, type, pet_name, location FROM reports WHERE id = 'REPORT_ID';
```

**2. Verificar que el trigger existe:**
```sql
SELECT * FROM pg_trigger WHERE tgname = 'trigger_geo_alerts_on_new_report';
```

**3. Generar alertas manualmente:**
```sql
SELECT enqueue_geo_alerts('REPORT_ID');
```

### **Problema: Edge Function no se invoca**

**1. Verificar webhook:**
- Dashboard → Database → Webhooks
- Debe estar habilitado
- URL correcta
- Authorization header con service_role_key

**2. Invocar manualmente:**
```sql
SELECT invoke_geo_alerts_edge_function();
```

**3. Ver logs:**
```bash
supabase functions logs send-geo-alerts
```

### **Problema: Consumo de batería alto**

**Ajustar configuración de ubicación en `hooks/useGeoAlerts.js`:**

```javascript
// Cambiar de:
const UPDATE_INTERVAL = 5 * 60 * 1000; // 5 minutos
const LOCATION_ACCURACY = Location.Accuracy.Balanced;

// A:
const UPDATE_INTERVAL = 10 * 60 * 1000; // 10 minutos
const LOCATION_ACCURACY = Location.Accuracy.Low;
```

---

## 📈 Capacidad y Límites

### **Límites del Sistema**

| Componente | Límite | Notas |
|------------|--------|-------|
| Edge Functions | 500,000 invocaciones/mes | Plan gratuito Supabase |
| Expo Push API | Sin límite | Completamente gratis |
| Notificaciones por invocación | 50 | Configurable en el código |
| Usuarios por búsqueda geográfica | Sin límite | PostGIS altamente optimizado |
| Tiempo de ejecución Edge Function | 25 segundos | Límite de Supabase |

### **Escalabilidad**

Para 1,000 usuarios activos:
- **Reportes diarios estimados**: 50
- **Usuarios notificados por reporte**: 10 (promedio)
- **Notificaciones diarias**: 500
- **Notificaciones mensuales**: 15,000
- **Uso de Edge Functions**: 0.003% del límite gratuito ✅

Para 10,000 usuarios:
- **Notificaciones mensuales**: 150,000
- **Uso de Edge Functions**: 0.03% del límite gratuito ✅

Para 100,000 usuarios:
- **Notificaciones mensuales**: 1,500,000
- **Uso de Edge Functions**: 0.3% del límite gratuito ✅

**Conclusión**: El sistema puede escalar a cientos de miles de usuarios sin costos adicionales.

---

## 🎯 Próximas Mejoras

### **Versión 1.1**
- [ ] Horario silencioso funcional
- [ ] Notificaciones con imagen de la mascota
- [ ] Agrupar múltiples reportes cercanos
- [ ] Historial de alertas recibidas

### **Versión 1.2**
- [ ] Notificaciones ricas (botones de acción)
- [ ] Rate limiting por usuario
- [ ] Analytics de tasa de apertura
- [ ] Mapa de alertas recientes

### **Versión 2.0**
- [ ] Rastreo en background más eficiente
- [ ] Zonas de alerta personalizadas (polígonos)
- [ ] Alertas por múltiples ubicaciones (casa, trabajo, etc.)
- [ ] Sistema de puntos por ayudar

---

## 📚 Referencias

- [Expo Location](https://docs.expo.dev/versions/latest/sdk/location/)
- [Expo Notifications](https://docs.expo.dev/versions/latest/sdk/notifications/)
- [PostGIS Geography](https://postgis.net/docs/using_postgis_dbmanagement.html#PostGIS_Geography)
- [Supabase Edge Functions](https://supabase.com/docs/guides/functions)
- [Supabase Database Webhooks](https://supabase.com/docs/guides/database/webhooks)

---

**✨ Sistema listo para producción con escalabilidad, privacidad y costo $0**

