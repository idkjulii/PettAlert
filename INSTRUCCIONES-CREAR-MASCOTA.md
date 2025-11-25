# 📝 Instrucciones: Crear Mascota de Prueba

## Opción 1: Desde Supabase (Rápido)

1. Ve a tu **Supabase Dashboard**
2. Abre el **SQL Editor**
3. Copia y pega el contenido del archivo `CREAR-MASCOTA-PRUEBA.sql`
4. Ejecuta el script
5. Recarga la app y deberías ver tu mascota

## Opción 2: Crear manualmente en Supabase

1. Ve a **Supabase Dashboard** → **Table Editor** → **pets**
2. Haz clic en **Insert** → **Insert row**
3. Completa los campos:
   - `owner_id`: `b3b9d127-50e0-4217-8c6b-cc2936b326bb` (tu ID)
   - `name`: `Firulais` (o el nombre que quieras)
   - `species`: `dog` (o `cat`, `bird`, `rabbit`, `other`)
   - `breed`: `Labrador Retriever` (opcional)
   - `color`: `Dorado` (opcional)
   - `size`: `large` (o `small`, `medium`)
   - `description`: `Perro muy amigable` (opcional)
   - `is_lost`: `false`
4. Haz clic en **Save**

## Verificar que funcionó

Después de crear la mascota:

1. Recarga la app (pull-to-refresh en la pantalla de mascotas)
2. Deberías ver tu mascota en la lista
3. Toca la mascota para ver el detalle con las pestañas de salud

## Próximos pasos

Una vez que veas tu mascota, podrás:
- ✅ Ver el detalle completo
- ✅ Navegar entre las pestañas (Info, Salud, Bienestar, Recordatorios)
- ⏳ Agregar eventos de salud (cuando se implementen los formularios)
- ⏳ Agregar vacunaciones (cuando se implementen los formularios)
- ⏳ Agregar indicadores de bienestar (cuando se implementen los formularios)

## Nota importante

Si quieres agregar datos de salud (peso, vacunas, etc.), primero debes ejecutar la migración SQL:
- `backend/migrations/007_pet_health_tracking.sql`

Esto creará las tablas necesarias para el módulo de salud.

