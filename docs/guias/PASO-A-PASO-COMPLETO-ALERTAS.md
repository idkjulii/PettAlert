# 📍 Guía Paso a Paso: Sistema de Alertas Geográficas

## 🎯 Resumen: 5 Pasos en Orden

1. ✅ **Ejecutar migración SQL** → Supabase Dashboard → SQL Editor
2. ✅ **Desplegar Edge Function** → Terminal (PowerShell)
3. ✅ **Configurar variables PostgreSQL** → Supabase Dashboard → Settings → Database
4. ✅ **Crear Webhook** → Supabase Dashboard → Database → Webhooks
5. ✅ **Compilar app** → Terminal (PowerShell)

---

## 📋 PASO 1: Ejecutar Migración SQL

### **Dónde:** Supabase Dashboard → SQL Editor

### **Pasos detallados:**

1. **Abre tu navegador** y ve a: https://app.supabase.com

2. **Selecciona tu proyecto** (o haz login si no estás autenticado)

3. **En el menú lateral izquierdo**, busca y click en:
   ```
   SQL Editor
   ```
   (Está en la sección "Database" del menú)

4. **Click en el botón verde:**
   ```
   + New query
   ```
   (Está en la esquina superior derecha)

5. **Abre el archivo de migración** en tu editor de código:
   ```
   backend/migrations/011_geo_alerts_system.sql
   ```

6. **Selecciona TODO el contenido** del archivo (Ctrl+A) y cópialo (Ctrl+C)

7. **Pega el contenido** en el editor SQL de Supabase (Ctrl+V)

8. **Click en el botón:**
   ```
   Run
   ```
   (O presiona Ctrl+Enter)

9. **Espera a que termine** (puede tardar 10-30 segundos)

10. **Verifica el resultado:**
    - Deberías ver mensajes de éxito en la parte inferior
    - Busca el mensaje: "SISTEMA DE ALERTAS GEOGRÁFICAS INSTALADO"

### ✅ Verificación:

Ejecuta esta query en el mismo SQL Editor:

```sql
SELECT * FROM get_geo_alerts_stats();
```

Deberías ver 5 filas con estadísticas del sistema.

---

## 📋 PASO 2: Desplegar Edge Function

### **Dónde:** Terminal (PowerShell en Windows)

### **Pasos detallados:**

1. **Abre PowerShell:**
   - Presiona `Windows + X`
   - Selecciona "Windows PowerShell" o "Terminal"
   - O busca "PowerShell" en el menú inicio

2. **Navega a tu proyecto:**
   ```powershell
   cd "C:\Users\maria\OneDrive\Escritorio\lpm\petFindnoborres"
   ```
   (Ajusta la ruta si es diferente)

3. **Verifica que tienes Supabase CLI:**
   ```powershell
   supabase --version
   ```
   
   **Si no está instalado:**
   ```powershell
   npm install -g supabase
   ```
   (Espera a que termine la instalación)

4. **Autentícate en Supabase:**
   ```powershell
   supabase login
   ```
   - Esto abrirá tu navegador
   - Haz login en Supabase si es necesario
   - Autoriza el acceso
   - Vuelve a PowerShell

5. **Verifica que el archivo existe:**
   ```powershell
   dir supabase\functions\send-geo-alerts\index.ts
   ```
   Deberías ver el archivo listado.

6. **Despliega la función:**
   ```powershell
   supabase functions deploy send-geo-alerts --project-ref eamsbroadstwkrkjcuvo
   ```
   
   **Nota:** Reemplaza `eamsbroadstwkrkjcuvo` con tu Project Ref real.
   
   **Para encontrar tu Project Ref:**
   - Ve a Supabase Dashboard
   - Settings → General
   - Copia el "Reference ID"

7. **Espera a que termine** (puede tardar 30-60 segundos)

8. **Deberías ver:**
   ```
   Deploying function send-geo-alerts...
   Function send-geo-alerts deployed successfully
   ```

### ✅ Verificación:

1. **En PowerShell, ejecuta:**
   ```powershell
   supabase functions list --project-ref eamsbroadstwkrkjcuvo
   ```
   Deberías ver `send-geo-alerts` en la lista.

2. **O en el navegador:**
   - Ve a Supabase Dashboard
   - Click en **Edge Functions** (en el menú lateral)
   - Deberías ver `send-geo-alerts` en la lista

---

## 📋 PASO 3: Configurar Variables PostgreSQL

### **Dónde:** Supabase Dashboard → Settings → Database

### **Pasos detallados:**

1. **En Supabase Dashboard**, click en:
   ```
   Settings
   ```
   (Icono de engranaje ⚙️ en el menú lateral izquierdo)

2. **En el submenú de Settings**, click en:
   ```
   Database
   ```
   (Está en la lista de opciones)

3. **Scroll hacia abajo** hasta encontrar la sección:
   ```
   Custom PostgreSQL Configuration
   ```
   (Está casi al final de la página)

4. **Click en el botón:**
   ```
   Add new configuration
   ```
   O si ya hay configuraciones, busca un botón para agregar más.

5. **Agrega la primera variable:**
   - **Key:** `app.supabase_url`
   - **Value:** `https://eamsbroadstwkrkjcuvo.supabase.co`
     (Reemplaza con tu Project URL real)
   - Click en **Save** o **Add**

6. **Agrega la segunda variable:**
   - **Key:** `app.supabase_service_role_key`
   - **Value:** Tu Service Role Key
     (Para obtenerla: Settings → API → service_role key)
   - Click en **Save** o **Add**

### 🔑 Cómo obtener tu Service Role Key:

1. En Supabase Dashboard, ve a **Settings → API**
2. Busca la sección **Project API keys**
3. Copia el valor de **service_role** (⚠️ NO uses la `anon` key)
4. Pégala en la variable `app.supabase_service_role_key`

### ✅ Verificación:

Las dos variables deberían aparecer en la lista de configuraciones.

---

## 📋 PASO 4: Crear Webhook

### **Dónde:** Supabase Dashboard → Database → Webhooks

### **Pasos detallados:**

1. **En Supabase Dashboard**, en el menú lateral, click en:
   ```
   Database
   ```

2. **En el submenú de Database**, click en:
   ```
   Webhooks
   ```
   (Está en la lista de opciones)

3. **Click en el botón:**
   ```
   Create a new webhook
   ```
   (Botón verde en la esquina superior derecha)

4. **Sección "General":**
   - **Name:** `process-geo-alerts-immediately`
     (Sin espacios, solo letras, números y guiones)
   - Click **Next** o continúa

5. **Sección "Conditions to fire webhook":**
   - **Table:** Selecciona `geo_alert_notifications_queue` del dropdown
   - **Events:** Marca SOLO la casilla **Insert** ☑️
     (Deja Update y Delete sin marcar)
   - Click **Next** o continúa

6. **Sección "Webhook configuration":**
   - **Type of webhook:** Selecciona **HTTP Request** (card con icono de globo)
   - Click **Next** o continúa

7. **Sección "HTTP Request":**
   
   **Method:**
   - Selecciona `POST` del dropdown
   
   **URL:**
   - Ingresa: `https://eamsbroadstwkrkjcuvo.supabase.co/functions/v1/send-geo-alerts`
   - ⚠️ Reemplaza `eamsbroadstwkrkjcuvo` con tu Project Ref
   - ⚠️ Asegúrate de que la URL esté COMPLETA (termina en `/send-geo-alerts`)
   
   **Timeout:**
   - Cambia de `5000` a `25000` (25 segundos)
   - ⚠️ **MUY IMPORTANTE:** Debe ser 25000, no 5000
   
   **HTTP Headers:**
   - Click en **+ Add a new header**
   - **Key:** `Content-Type`
   - **Value:** `application/json`
   - Click **Add** o **Save**
   
   - Click en **+ Add a new header** (otra vez)
   - **Key:** `Authorization`
   - **Value:** `Bearer TU_SERVICE_ROLE_KEY`
     (Reemplaza `TU_SERVICE_ROLE_KEY` con tu service_role key real)
   - Click **Add** o **Save**

8. **Click en el botón verde:**
   ```
   Create webhook
   ```
   (Esquina inferior derecha)

### ✅ Verificación:

1. Deberías ver el webhook en la lista de webhooks
2. Estado debería ser **Active** (verde)
3. Puedes click en el webhook para ver detalles

---

## 📋 PASO 5: Compilar App con Nuevos Permisos

### **Dónde:** Terminal (PowerShell)

### **Pasos detallados:**

1. **Abre PowerShell** (si no lo tienes abierto)

2. **Navega a tu proyecto:**
   ```powershell
   cd "C:\Users\maria\OneDrive\Escritorio\lpm\petFindnoborres"
   ```

3. **Regenera la configuración nativa:**
   ```powershell
   npx expo prebuild --clean
   ```
   (Esto puede tardar 1-2 minutos)

4. **Compila para Android:**
   ```powershell
   npx expo run:android
   ```
   (Esto puede tardar varios minutos la primera vez)

   **O para iOS (si tienes Mac):**
   ```powershell
   npx expo run:ios
   ```

### ✅ Verificación:

La app debería compilar y ejecutarse con los nuevos permisos de ubicación.

---

## 🧪 PASO 6: Testing (Opcional pero Recomendado)

### **Dónde:** Supabase Dashboard → SQL Editor + Tu App

### **Pasos detallados:**

1. **Abre la app** en tu dispositivo/emulador

2. **Ve a Perfil → Alertas Geográficas** (si agregaste el botón)

3. **Activa "Rastreo de ubicación"**

4. **Acepta permisos** cuando se soliciten

5. **En Supabase Dashboard → SQL Editor**, ejecuta:

```sql
-- Ver tu ubicación registrada
SELECT * FROM user_locations WHERE user_id = auth.uid();

-- Ver estadísticas
SELECT * FROM get_geo_alerts_stats();
```

6. **Crea un reporte de prueba cercano:**

```sql
-- Reemplaza las coordenadas con ubicaciones cercanas a ti
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

7. **Deberías recibir una notificación push** en tu dispositivo

8. **Verifica en SQL:**
```sql
-- Ver notificaciones creadas
SELECT 
    id,
    recipient_id,
    distance_meters,
    processed_at,
    created_at
FROM geo_alert_notifications_queue
ORDER BY created_at DESC
LIMIT 5;
```

---

## 📊 Checklist Final

Antes de considerar que todo está listo, verifica:

- [ ] Migración SQL ejecutada sin errores
- [ ] Edge Function desplegada y aparece en Dashboard
- [ ] Variables PostgreSQL configuradas (2 variables)
- [ ] Webhook creado y activo
- [ ] App compilada con nuevos permisos
- [ ] Botón de alertas agregado en el perfil (opcional)
- [ ] Testing realizado y notificaciones funcionan

---

## 🐛 Si Algo No Funciona

### **Error en SQL:**
- Verifica que PostGIS está habilitado: `SELECT PostGIS_Version();`
- Si no está, ejecuta: `CREATE EXTENSION IF NOT EXISTS postgis;`

### **Error al desplegar Edge Function:**
- Verifica que estás autenticado: `supabase login`
- Verifica tu Project Ref en Dashboard → Settings → General

### **Webhook no se invoca:**
- Verifica que la URL es correcta y completa
- Verifica que el timeout es 25000ms
- Verifica que el Authorization header tiene el service_role key

### **No recibo notificaciones:**
- Verifica que tienes tokens push: `SELECT * FROM push_tokens WHERE user_id = auth.uid();`
- Verifica que tu ubicación está registrada: `SELECT * FROM user_locations WHERE user_id = auth.uid();`
- Verifica logs: `supabase functions logs send-geo-alerts --follow`

---

## 📚 Documentación Adicional

- **Guía completa:** `GUIA-ALERTAS-GEOGRAFICAS.md`
- **Inicio rápido:** `INICIO-RAPIDO-ALERTAS-GEOGRAFICAS.md`
- **Configurar webhook:** `CONFIGURACION-WEBHOOK-ALERTAS-GEO.md`
- **Desplegar función:** `DESPLEGAR-EDGE-FUNCTION-ALERTAS.md`

---

**✨ ¡Sigue estos pasos en orden y tendrás el sistema funcionando!**

