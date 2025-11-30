# 🔧 Configurar Variables PostgreSQL con SQL

## ⚠️ Si no encuentras "Custom PostgreSQL Configuration"

Puedes configurar las variables directamente con SQL. Esto es más directo y funciona en todos los planes.

---

## 📋 Método: Usar SQL Editor

### **Paso 1: Abrir SQL Editor**

1. En Supabase Dashboard, click en **SQL Editor** (en el menú lateral)
2. Click en **+ New query**

### **Paso 2: Ejecutar este SQL**

Copia y pega este código SQL (reemplaza los valores con los tuyos):

```sql
-- Configurar variable: app.supabase_url
ALTER DATABASE postgres SET app.supabase_url = 'https://eamsbroadstwkrkjcuvo.supabase.co';

-- Configurar variable: app.supabase_service_role_key
-- ⚠️ IMPORTANTE: Reemplaza TU_SERVICE_ROLE_KEY con tu service_role key real
ALTER DATABASE postgres SET app.supabase_service_role_key = 'TU_SERVICE_ROLE_KEY_AQUI';
```

### **Paso 3: Obtener tu Service Role Key**

1. En Supabase Dashboard, click en **Settings** (⚙️)
2. Click en **API** (en el submenú)
3. Busca la sección **Project API keys**
4. Copia el valor de **service_role** (⚠️ NO uses la `anon` key)
5. Pégala en el SQL reemplazando `TU_SERVICE_ROLE_KEY_AQUI`

### **Paso 4: Ejecutar**

1. Reemplaza `TU_SERVICE_ROLE_KEY_AQUI` con tu service_role key real
2. Click en **Run** (o presiona Ctrl+Enter)

### **Paso 5: Verificar**

Ejecuta esta query para verificar:

```sql
-- Ver todas las variables configuradas
SELECT name, setting 
FROM pg_settings 
WHERE name LIKE 'app.%';
```

Deberías ver:
- `app.supabase_url`
- `app.supabase_service_role_key`

---

## 🔍 Alternativa: Verificar en Settings

Si quieres intentar encontrarlo en la UI:

1. En **Settings → Database**, scroll hacia abajo
2. Busca una sección llamada:
   - "Custom PostgreSQL Configuration"
   - "PostgreSQL Configuration"
   - "Database Configuration"
   - "Environment Variables"

Si no aparece, usa el método SQL de arriba (es más confiable).

---

## ✅ Después de Configurar

Una vez configuradas las variables, continúa con:
- **Paso 4: Crear el Webhook**

---

## 🐛 Si hay Error

Si obtienes un error de permisos, intenta con:

```sql
-- En lugar de ALTER DATABASE, usa SET
SET app.supabase_url = 'https://eamsbroadstwkrkjcuvo.supabase.co';
SET app.supabase_service_role_key = 'TU_SERVICE_ROLE_KEY';
```

Pero esto solo dura para la sesión actual. El método `ALTER DATABASE` es permanente.

