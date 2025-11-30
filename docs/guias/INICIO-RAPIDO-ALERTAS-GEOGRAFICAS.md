# 🚀 Inicio Rápido: Alertas Geográficas

## ¿Qué es este sistema?

Un sistema completo de notificaciones push que alerta a los usuarios cuando se reporta una mascota perdida o encontrada **cerca de su ubicación** (1km por defecto).

**Ejemplo:**
- María está en casa (coordenadas: -34.603722, -58.381592)
- Juan reporta que perdió a su perro Max a 500 metros de María
- María recibe instantáneamente una notificación: "🐾 Mascota perdida cerca de ti: Max · Perro · Golden a 0.5km"

---

## ✨ Características principales

- ✅ Notificaciones push instantáneas
- ✅ Radio configurable (500m, 1km, 2km, 5km)
- ✅ Filtros por tipo (perdidas/encontradas) y especie
- ✅ Bajo consumo de batería
- ✅ Privacidad garantizada (ubicación encriptada)
- ✅ Sin costo adicional (usa plan gratuito de Supabase y Expo)

---

## 🎯 Instalación en 5 pasos

### **Paso 1: Ejecutar migración SQL (2 minutos)**

1. Abre **Supabase Dashboard → SQL Editor**
2. Click en **New Query**
3. Copia el contenido completo de: `backend/migrations/011_geo_alerts_system.sql`
4. Click en **Run**
5. Verifica que aparece: "✅ SISTEMA DE ALERTAS GEOGRÁFICAS INSTALADO"

### **Paso 2: Desplegar Edge Function (1 minuto)**

```bash
# En tu terminal
supabase functions deploy send-geo-alerts --project-ref TU_PROJECT_REF
```

### **Paso 3: Configurar Webhook (2 minutos)**

1. Ve a **Supabase Dashboard → Database → Webhooks**
2. Click **Create a new hook**
3. Llena el formulario:
   - **Name**: `process-geo-alerts`
   - **Table**: `geo_alert_notifications_queue`
   - **Events**: ☑️ `INSERT`
   - **Type**: `HTTP Request`
   - **Method**: `POST`
   - **URL**: `https://TU_PROJECT_REF.supabase.co/functions/v1/send-geo-alerts`
   - **Headers**:
     ```
     Authorization: Bearer TU_SERVICE_ROLE_KEY
     Content-Type: application/json
     ```
   - **Timeout**: `25000`
4. Click **Create webhook**

### **Paso 4: Configurar variables de PostgreSQL (1 minuto)**

1. Ve a **Supabase Dashboard → Settings → Database**
2. Scroll hasta **Custom PostgreSQL Configuration**
3. Agrega estas dos variables:
   ```
   app.supabase_url = https://TU_PROJECT_REF.supabase.co
   app.supabase_service_role_key = TU_SERVICE_ROLE_KEY
   ```
4. Click **Save**

### **Paso 5: Compilar app con nuevos permisos (5 minutos)**

```bash
# Regenerar configuración nativa
npx expo prebuild --clean

# Compilar para Android
npx expo run:android

# O para iOS
npx expo run:ios
```

---

## 🧪 Testing en 3 pasos

### **1. Activa las alertas en la app**

1. Abre la app
2. Ve a **Perfil → Alertas Geográficas**
3. Activa **"Rastreo de ubicación"**
4. Acepta permisos cuando se soliciten
5. Verifica que aparece: "📍 Última actualización: HH:MM:SS"

### **2. Verifica en la base de datos**

Ejecuta en SQL Editor:

```sql
-- Ver tu ubicación registrada
SELECT * FROM user_locations WHERE user_id = auth.uid();

-- Ver estadísticas del sistema
SELECT * FROM get_geo_alerts_stats();
```

### **3. Crea un reporte de prueba**

En SQL Editor (reemplaza las coordenadas con ubicaciones cercanas a ti):

```sql
INSERT INTO reports (
    type,
    reporter_id,
    pet_name,
    species,
    breed,
    location,
    address,
    status
) VALUES (
    'lost',
    auth.uid(),  -- O el ID de otro usuario
    'Max',
    'dog',
    'Golden Retriever',
    ST_SetSRID(ST_MakePoint(-58.382000, -34.604000), 4326)::geography,
    'Av. de Prueba 123',
    'active'
) RETURNING id;
```

**Resultado esperado:**
- Deberías recibir una notificación push en tu dispositivo
- Título: "🐾 Mascota perdida cerca de ti"
- Cuerpo: "Max · Perro · Golden Retriever a 0.5km. Av. de Prueba 123"

---

## 📱 ¿Cómo lo usa el usuario final?

### **Primera vez:**

1. Usuario abre la app
2. Va a **Perfil**
3. Toca **"Alertas Geográficas"**
4. Activa **"Rastreo de ubicación"**
5. Acepta permisos
6. ¡Listo! Ya recibirá alertas

### **Uso diario:**

- La app actualiza la ubicación automáticamente en segundo plano
- Cuando alguien reporta una mascota cerca, el usuario recibe notificación
- Puede tocar la notificación para ver el reporte completo
- Puede ajustar el radio, filtros, etc. en cualquier momento

---

## ⚙️ Configuraciones disponibles

El usuario puede personalizar:

- **Radio de alertas**: 500m, 1km, 2km, 5km
- **Tipos de reportes**: Solo perdidas, solo encontradas, o ambas
- **Especies**: Perros, gatos, aves, otros, o todas
- **Horario silencioso**: (próximamente) No recibir alertas en ciertos horarios

---

## 🔧 Troubleshooting

### **"No recibo notificaciones"**

Verifica:
1. ✅ Rastreo de ubicación está activado en la app
2. ✅ Notificaciones están habilitadas en la app
3. ✅ Tienes tokens push registrados: `SELECT * FROM push_tokens WHERE user_id = auth.uid();`
4. ✅ Tu ubicación está registrada: `SELECT * FROM user_locations WHERE user_id = auth.uid();`

### **"Las alertas no se generan"**

Verifica:
1. ✅ El reporte tiene ubicación (campo `location` no es NULL)
2. ✅ El reporte está activo (`status = 'active'`)
3. ✅ Hay usuarios con ubicación cercana

### **"Edge Function no se invoca"**

Verifica:
1. ✅ Webhook está configurado y habilitado
2. ✅ URL del webhook es correcta
3. ✅ Authorization header tiene el service_role_key correcto

Ver logs:
```bash
supabase functions logs send-geo-alerts --follow
```

---

## 📊 Capacidad del sistema

Para tu referencia:

| Usuarios activos | Reportes/día | Notificaciones/mes | Costo |
|-----------------|--------------|-------------------|-------|
| 1,000 | 50 | 15,000 | $0 ✅ |
| 10,000 | 500 | 150,000 | $0 ✅ |
| 100,000 | 5,000 | 1,500,000 | $0 ✅ |

El sistema usa el plan gratuito de Supabase y Expo Push. Sin costos adicionales.

---

## 📚 Documentación adicional

- **Guía completa**: `GUIA-ALERTAS-GEOGRAFICAS.md` (todo el detalle técnico)
- **Scripts de despliegue**: 
  - Windows: `scripts/deploy-geo-alerts.bat`
  - Mac/Linux: `scripts/deploy-geo-alerts.sh`
- **Script de verificación**: `scripts/verificar-geo-alerts.ps1`

---

## 🆘 ¿Necesitas ayuda?

1. Lee primero: `GUIA-ALERTAS-GEOGRAFICAS.md`
2. Ejecuta: `.\scripts\verificar-geo-alerts.ps1` para diagnóstico
3. Revisa los logs: `supabase functions logs send-geo-alerts`

---

## 📍 Arquitectura simplificada

```
Usuario reporta mascota perdida
          ↓
Sistema busca usuarios cercanos (1km)
          ↓
Crea notificaciones para esos usuarios
          ↓
Edge Function las procesa y envía
          ↓
Usuarios reciben notificación push
          ↓
Tocan notificación → Ven el reporte
```

---

**✨ ¡Listo! Tu app ahora alerta a usuarios cuando hay mascotas perdidas cerca.**

Para dudas o mejoras, consulta la guía completa en `GUIA-ALERTAS-GEOGRAFICAS.md`

