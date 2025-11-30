# 📦 Supabase Edge Functions

Este directorio contiene las Edge Functions de Supabase para PetFind.

## 📂 Estructura

```
supabase/
└── functions/
    └── send-push-notification/
        ├── index.ts      # Función principal
        └── README.md     # Documentación específica
```

## 🚀 Edge Functions Disponibles

### `send-push-notification`

**Propósito**: Procesa la cola de notificaciones push y las envía a través de Expo Push API.

**Invocación**: 
- Automática via trigger de base de datos
- Automática via pg_cron cada 5 minutos
- Manual via HTTP POST

**URL**: `https://TU_PROJECT_REF.supabase.co/functions/v1/send-push-notification`

**Documentación completa**: Ver `send-push-notification/README.md`

## 🛠️ Comandos Útiles

### Autenticación y Setup

```bash
# Instalar Supabase CLI
npm install -g supabase

# Login
supabase login

# Vincular proyecto
supabase link --project-ref TU_PROJECT_REF
```

### Desarrollo

```bash
# Servir función localmente
supabase functions serve send-push-notification

# Ver logs locales
supabase functions logs send-push-notification
```

### Deployment

```bash
# Desplegar función específica
supabase functions deploy send-push-notification

# Desplegar todas las funciones
supabase functions deploy

# Ver logs en producción
supabase functions logs send-push-notification --follow
```

### Testing

```bash
# Test local
curl -X POST http://localhost:54321/functions/v1/send-push-notification \
  -H "Authorization: Bearer YOUR_ANON_KEY"

# Test en producción
curl -X POST https://TU_PROJECT_REF.supabase.co/functions/v1/send-push-notification \
  -H "Authorization: Bearer YOUR_ANON_KEY"
```

## 🔐 Variables de Entorno

Las Edge Functions tienen acceso automático a:

- `SUPABASE_URL` - URL de tu proyecto
- `SUPABASE_SERVICE_ROLE_KEY` - Service role key
- `SUPABASE_ANON_KEY` - Anonymous key

No necesitas configurarlas manualmente.

## 📚 Recursos

- [Documentación oficial de Edge Functions](https://supabase.com/docs/guides/functions)
- [Guía de configuración completa](../CONFIGURAR-NOTIFICACIONES-PUSH.md)
- [Resumen técnico del sistema](../SISTEMA-NOTIFICACIONES-RESUMEN.md)

## 🎯 Próximas Funciones (Futuro)

Ideas para Edge Functions adicionales:

- `process-pet-matches` - Cálculo de matches de mascotas
- `generate-report-summary` - Resumen de reportes con IA
- `send-email-notification` - Notificaciones por email
- `moderate-content` - Moderación automática de contenido

---

Para más información sobre el sistema de notificaciones completo, ver:
- `CONFIGURAR-NOTIFICACIONES-PUSH.md` - Guía de instalación paso a paso
- `SISTEMA-NOTIFICACIONES-RESUMEN.md` - Arquitectura completa del sistema




