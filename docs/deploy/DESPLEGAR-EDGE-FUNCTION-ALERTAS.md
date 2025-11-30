# 🚀 Desplegar Edge Function: send-geo-alerts

## ⚠️ IMPORTANTE: Haz esto ANTES de crear el webhook

La Edge Function debe estar desplegada antes de configurar el webhook, porque el webhook apunta a la URL de la función.

---

## 📋 Paso 1: Verificar que tienes Supabase CLI

Abre tu terminal (PowerShell en Windows) y ejecuta:

```bash
supabase --version
```

Si no está instalado, instálalo:

```bash
npm install -g supabase
```

---

## 📋 Paso 2: Autenticarte en Supabase

```bash
supabase login
```

Esto abrirá tu navegador para autenticarte. Una vez autenticado, vuelve a la terminal.

---

## 📋 Paso 3: Vincular tu Proyecto

Necesitas vincular tu proyecto local con el proyecto de Supabase en la nube.

### Opción A: Si ya tienes un proyecto vinculado

```bash
# Ver proyectos vinculados
supabase projects list
```

### Opción B: Vincular proyecto nuevo

```bash
supabase link --project-ref eamsbroadstwkrkjcuvo
```

**Nota:** Reemplaza `eamsbroadstwkrkjcuvo` con tu Project Ref real si es diferente.

---

## 📋 Paso 4: Verificar que la Edge Function existe

Asegúrate de que el archivo existe:

```bash
# En Windows PowerShell
dir supabase\functions\send-geo-alerts\index.ts

# En Mac/Linux
ls supabase/functions/send-geo-alerts/index.ts
```

Deberías ver el archivo `index.ts` listado.

---

## 📋 Paso 5: Desplegar la Edge Function

Ejecuta este comando (reemplaza con tu Project Ref):

```bash
supabase functions deploy send-geo-alerts --project-ref eamsbroadstwkrkjcuvo
```

**Si ya tienes el proyecto vinculado**, puedes usar:

```bash
supabase functions deploy send-geo-alerts
```

---

## ✅ Paso 6: Verificar el Despliegue

### Verificar que se desplegó:

```bash
supabase functions list --project-ref eamsbroadstwkrkjcuvo
```

Deberías ver `send-geo-alerts` en la lista.

### Probar la función manualmente:

```bash
supabase functions invoke send-geo-alerts --project-ref eamsbroadstwkrkjcuvo
```

O desde el Dashboard:
1. Ve a **Supabase Dashboard → Edge Functions**
2. Deberías ver `send-geo-alerts` en la lista
3. Click en ella para ver detalles

---

## 🔍 Ver Logs (Opcional)

Para ver los logs en tiempo real:

```bash
supabase functions logs send-geo-alerts --project-ref eamsbroadstwkrkjcuvo --follow
```

---

## ✅ Checklist de Verificación

Antes de crear el webhook, verifica:

- [ ] Supabase CLI instalado (`supabase --version`)
- [ ] Autenticado en Supabase (`supabase login`)
- [ ] Proyecto vinculado (o usaste `--project-ref`)
- [ ] Archivo `index.ts` existe en `supabase/functions/send-geo-alerts/`
- [ ] Función desplegada exitosamente
- [ ] Función aparece en Dashboard → Edge Functions

---

## 🐛 Troubleshooting

### Error: "Not logged in"

```bash
supabase login
```

### Error: "Project not found"

Verifica tu Project Ref:
1. Ve a **Supabase Dashboard**
2. Click en **Settings** → **General**
3. Copia el **Reference ID**
4. Úsalo en el comando: `--project-ref TU_REF_ID`

### Error: "Function not found"

Verifica que el directorio existe:
```bash
# Windows
dir supabase\functions\send-geo-alerts

# Mac/Linux
ls -la supabase/functions/send-geo-alerts
```

Deberías ver al menos `index.ts` dentro.

### Error: "Permission denied"

Asegúrate de estar autenticado y tener permisos en el proyecto.

---

## 📝 Comandos Rápidos (Copia y Pega)

```bash
# 1. Verificar CLI
supabase --version

# 2. Login (si no estás autenticado)
supabase login

# 3. Desplegar función
supabase functions deploy send-geo-alerts --project-ref eamsbroadstwkrkjcuvo

# 4. Verificar despliegue
supabase functions list --project-ref eamsbroadstwkrkjcuvo

# 5. Ver logs
supabase functions logs send-geo-alerts --project-ref eamsbroadstwkrkjcuvo --follow
```

---

## ✅ Una vez Desplegado

Ahora SÍ puedes crear el webhook. La URL será:

```
https://eamsbroadstwkrkjcuvo.supabase.co/functions/v1/send-geo-alerts
```

Esta URL funcionará porque la Edge Function ya está desplegada.

---

**✨ Después de desplegar, continúa con la configuración del webhook.**

