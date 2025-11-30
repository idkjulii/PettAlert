# 📍 Edge Function: send-geo-alerts

## Descripción

Esta Edge Function procesa la cola de alertas geográficas y envía notificaciones push a los usuarios que están cerca de un nuevo reporte de mascota perdida o encontrada.

## Funcionamiento

1. **Lee la cola** de `geo_alert_notifications_queue` (máximo 50 alertas por invocación)
2. **Para cada alerta:**
   - Obtiene los tokens push del destinatario
   - Construye el mensaje de notificación con información de distancia
   - Envía a Expo Push API
   - Marca la alerta como procesada
3. **Limpia** alertas antiguas (mayores a 7 días)

## Datos de la Notificación

```typescript
{
  title: "🐾 Mascota perdida cerca de ti" | "🎉 Mascota encontrada cerca de ti",
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

## Invocación

### Automática (Recomendada)

Se invoca automáticamente mediante:
- **Trigger de base de datos**: Al insertar en `geo_alert_notifications_queue`
- **Database Webhook**: Configurado en Dashboard → Database → Webhooks
- **Cron backup**: Cada 5 minutos (opcional)

### Manual

```sql
-- Desde SQL
SELECT invoke_geo_alerts_edge_function();
```

```bash
# Desde CLI
supabase functions invoke send-geo-alerts --method POST
```

## Configuración de Webhook

1. Ve a **Supabase Dashboard → Database → Webhooks**
2. Crea nuevo webhook:
   - **Name**: `process-geo-alerts`
   - **Table**: `geo_alert_notifications_queue`
   - **Events**: `INSERT`
   - **Type**: `HTTP Request`
   - **HTTP Request**:
     - **Method**: `POST`
     - **URL**: `https://YOUR_PROJECT.supabase.co/functions/v1/send-geo-alerts`
     - **Headers**: 
       - `Authorization: Bearer YOUR_SERVICE_ROLE_KEY`
       - `Content-Type: application/json`
   - **Timeout**: 25000ms
   - **HTTP Method**: POST

## Variables de Entorno

Automáticamente disponibles en Edge Functions:
- `SUPABASE_URL`: URL del proyecto
- `SUPABASE_SERVICE_ROLE_KEY`: Clave de service role

## Despliegue

```bash
# Desplegar la función
supabase functions deploy send-geo-alerts

# Ver logs en tiempo real
supabase functions logs send-geo-alerts --follow
```

## Monitoreo

### Ver estado del sistema

```sql
SELECT * FROM get_geo_alerts_stats();
```

Retorna:
- Usuarios con ubicación activa
- Usuarios con alertas habilitadas
- Alertas pendientes
- Alertas enviadas hoy
- Radio promedio de alertas

### Ver logs

```bash
supabase functions logs send-geo-alerts --follow
```

### Forzar procesamiento

```sql
SELECT invoke_geo_alerts_edge_function();
```

## Capacidad

- **Límite de Expo**: Sin límite para notificaciones push
- **Edge Functions**: 500,000 invocaciones/mes (plan gratuito)
- **Procesamiento**: 50 alertas por invocación
- **Tiempo de ejecución**: ~2-5 segundos para 50 alertas
- **Capacidad mensual**: 25,000,000 alertas/mes

## Optimización

- Procesa máximo 50 alertas por invocación (balance entre velocidad y timeout)
- Limpieza automática de alertas mayores a 7 días
- Índices optimizados en la base de datos
- Procesamiento asíncrono (no bloquea la inserción del reporte)

## Manejo de Errores

- Si un usuario no tiene tokens → Se marca como procesada
- Si falla el envío a Expo → Se registra error pero continúa con las demás
- Si falla la función → El webhook reintenta automáticamente (3 veces)
- Si todo falla → El cron backup lo procesa en 5 minutos

## Seguridad

- ✅ Usa `service_role_key` para acceso completo a la BD
- ✅ RLS en las tablas evita acceso directo de usuarios
- ✅ Solo triggers y service_role pueden escribir en la cola
- ✅ Tokens push nunca se exponen al frontend

## Testing

### Probar localmente

```bash
# Iniciar funciones localmente
supabase functions serve send-geo-alerts

# En otra terminal, invocar
curl -i --location --request POST 'http://localhost:54321/functions/v1/send-geo-alerts' \
  --header 'Authorization: Bearer YOUR_SERVICE_ROLE_KEY' \
  --header 'Content-Type: application/json'
```

### Crear alerta de prueba

```sql
-- 1. Asegúrate de tener tu ubicación registrada
SELECT * FROM upsert_user_location(
  auth.uid(),
  -34.603722,  -- latitud
  -58.381592,  -- longitud
  10.0         -- precisión en metros
);

-- 2. Crea un reporte de prueba (automáticamente genera alertas)
INSERT INTO reports (
  type,
  reporter_id,
  pet_name,
  species,
  location,
  address,
  status
) VALUES (
  'lost',
  auth.uid(),
  'Max',
  'dog',
  ST_SetSRID(ST_MakePoint(-58.380000, -34.604000), 4326)::geography,
  'Av. de Prueba 123',
  'active'
);

-- 3. Verificar que se crearon alertas
SELECT COUNT(*) FROM geo_alert_notifications_queue WHERE processed_at IS NULL;

-- 4. Procesar manualmente
SELECT invoke_geo_alerts_edge_function();
```

## Troubleshooting

### No se envían alertas

1. Verifica que el webhook esté configurado:
   ```sql
   -- Ver alertas pendientes
   SELECT * FROM geo_alert_notifications_queue WHERE processed_at IS NULL;
   ```

2. Revisa los logs:
   ```bash
   supabase functions logs send-geo-alerts
   ```

3. Fuerza procesamiento manual:
   ```sql
   SELECT invoke_geo_alerts_edge_function();
   ```

### Usuario no recibe notificaciones

1. Verifica que tiene ubicación registrada:
   ```sql
   SELECT * FROM user_locations WHERE user_id = 'USER_UUID';
   ```

2. Verifica que tiene alertas habilitadas:
   ```sql
   SELECT * FROM user_alert_preferences WHERE user_id = 'USER_UUID';
   ```

3. Verifica que tiene tokens push:
   ```sql
   SELECT * FROM push_tokens WHERE user_id = 'USER_UUID';
   ```

### Alertas no se generan

1. Verifica que el reporte tiene ubicación:
   ```sql
   SELECT id, type, pet_name, location FROM reports WHERE id = 'REPORT_UUID';
   ```

2. Verifica que el trigger está activo:
   ```sql
   SELECT * FROM pg_trigger WHERE tgname = 'trigger_geo_alerts_on_new_report';
   ```

3. Crea alertas manualmente:
   ```sql
   SELECT enqueue_geo_alerts('REPORT_UUID');
   ```

## Próximas Mejoras

- [ ] Agrupar notificaciones si hay múltiples reportes cercanos
- [ ] Permitir notificaciones ricas con imagen de la mascota
- [ ] Implementar rate limiting por usuario
- [ ] Analytics de tasa de apertura de alertas
- [ ] Permitir responder directamente desde la notificación


