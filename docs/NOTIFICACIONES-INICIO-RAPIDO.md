# ⚡ Notificaciones Push - Inicio Rápido

## 🎯 ¿Qué tengo que hacer?

Seguir estos **8 pasos** para activar las notificaciones push en tu app PetFind:

---

## 📋 Checklist de Instalación

### ✅ Paso 1: Instalar Supabase CLI

**Windows:**
```bash
npm install -g supabase
```

**Verificar:**
```bash
supabase --version
```

---

### ✅ Paso 2: Autenticarse

```bash
supabase login
```

Te pedirá un access token. Generarlo en:
👉 https://app.supabase.com/account/tokens

---

### ✅ Paso 3: Vincular Proyecto

```bash
supabase link --project-ref TU_PROJECT_REF
```

**¿Dónde está mi project-ref?**
- Supabase Dashboard → Settings → General → Reference ID

---

### ✅ Paso 4: Habilitar pg_net

En **SQL Editor** de Supabase Dashboard:

```sql
CREATE EXTENSION IF NOT EXISTS pg_net;
```

---

### ✅ Paso 5: Ejecutar Migración SQL

**Opción A - Manual (Recomendado):**
1. Abre: `backend/migrations/009_notification_system.sql`
2. Copia TODO el contenido
3. Pégalo en **SQL Editor** de Supabase
4. Ejecuta

**Opción B - CLI:**
```bash
supabase db push
```

---

### ✅ Paso 6: Desplegar Edge Function

```bash
supabase functions deploy send-push-notification
```

---

### ✅ Paso 7: Configurar Variables

Ve a: **Supabase Dashboard → Settings → Database → Custom PostgreSQL Configuration**

Agrega estas 2 variables:

```ini
app.supabase_url = https://TU_PROJECT_REF.supabase.co
app.supabase_service_role_key = TU_SERVICE_ROLE_KEY
```

**¿Dónde está mi service_role_key?**
- Supabase Dashboard → Settings → API → service_role (secret)

⚠️ **IMPORTANTE**: Usa `service_role`, NO `anon`

---

### ✅ Paso 8: Verificar

En **SQL Editor**:

```sql
SELECT * FROM check_notification_system_status();
```

Deberías ver:
```
status_item        | status_value | details
-------------------+--------------+------------------------
Pendientes         | 0            | Notificaciones en cola
Procesadas hoy     | 0            | Enviadas en 24h
Usuarios con tokens| 0            | Pueden recibir push
Cron jobs activos  | 2            | Tareas programadas
Última procesada   | Nunca        | Timestamp última
```

---

## 🎉 ¡Listo!

### Probar el sistema:

1. Abre tu app PetFind en 2 dispositivos
2. Inicia sesión con usuarios diferentes
3. Usuario A envía mensaje a Usuario B
4. Usuario B debería recibir notificación 🔔

---

## 🐛 ¿No funciona?

### Ver logs en tiempo real:

```bash
supabase functions logs send-push-notification --follow
```

### Verificar que hay notificaciones en cola:

```sql
SELECT * FROM message_notifications_queue 
WHERE processed_at IS NULL;
```

### Verificar tokens registrados:

```sql
SELECT COUNT(*) FROM push_tokens;
```

### Forzar procesamiento manual:

```sql
SELECT invoke_push_notification_edge_function();
```

---

## 📞 Ayuda

Si algo falla, revisa:

1. **Documentación completa**: `CONFIGURAR-NOTIFICACIONES-PUSH.md`
2. **Arquitectura técnica**: `SISTEMA-NOTIFICACIONES-RESUMEN.md`
3. **README de Edge Function**: `supabase/functions/send-push-notification/README.md`

---

## 🚀 Script Automatizado

**Windows:**
```bash
CONFIGURAR-NOTIFICACIONES-RAPIDO.bat
```

**Linux/Mac:**
```bash
./configurar-notificaciones.sh
```

---

## ⏱️ Tiempo estimado

- **Con script**: ~10 minutos
- **Manual**: ~15 minutos

## 💰 Costo

- ✅ **$0.00 USD** (completamente gratis)

---

**¡Tu sistema de notificaciones estará listo en menos de 15 minutos!** 🎉



