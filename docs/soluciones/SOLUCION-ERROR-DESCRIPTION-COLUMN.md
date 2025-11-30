# 🔧 Solución: Error "Could not find the 'description' column"

## Problema

El error indica que la tabla `pets` no tiene la columna `description` (y posiblemente otras columnas).

```
ERROR: Could not find the 'description' column of 'pets' in the schema cache
```

## Solución Rápida

### Paso 1: Ejecutar la migración de columnas faltantes

1. Ve a **Supabase Dashboard** → **SQL Editor**
2. Abre el archivo: `backend/migrations/008_add_missing_pets_columns.sql`
3. Copia TODO el contenido
4. Pégalo en el SQL Editor
5. Haz clic en **Run**

Esta migración:
- ✅ Agrega la columna `description` si no existe
- ✅ Agrega la columna `distinctive_features` si no existe
- ✅ Agrega la columna `photos` si no existe
- ✅ Agrega la columna `is_lost` si no existe
- ✅ Agrega las columnas `created_at` y `updated_at` si no existen
- ✅ Crea los índices y políticas necesarias

### Paso 2: Verificar que se agregaron las columnas

Ejecuta esto en el SQL Editor:

```sql
-- Ver todas las columnas de la tabla pets
SELECT 
    column_name,
    data_type,
    is_nullable
FROM information_schema.columns
WHERE table_name = 'pets'
ORDER BY ordinal_position;
```

**Deberías ver estas columnas:**
- `id`
- `owner_id`
- `name`
- `species`
- `breed`
- `color`
- `size`
- `description` ✅ (nueva)
- `distinctive_features` ✅ (nueva)
- `photos` ✅ (nueva)
- `is_lost` ✅ (nueva)
- `created_at` ✅ (nueva)
- `updated_at` ✅ (nueva)

### Paso 3: Reiniciar la app

1. Detén la app (Ctrl+C en la terminal)
2. Reinicia con `npx expo start -c` (el `-c` limpia la caché)
3. Intenta crear una mascota nuevamente

## Solución Alternativa (si prefieres recrear la tabla)

Si prefieres recrear la tabla desde cero (⚠️ esto borrará datos existentes):

```sql
-- ⚠️ ADVERTENCIA: Esto borrará todos los datos de mascotas existentes
DROP TABLE IF EXISTS pets CASCADE;

-- Crear tabla completa
CREATE TABLE pets (
    id UUID DEFAULT uuid_generate_v4() PRIMARY KEY,
    owner_id UUID REFERENCES profiles(id) ON DELETE CASCADE,
    name TEXT NOT NULL,
    species TEXT NOT NULL CHECK (species IN ('dog', 'cat', 'bird', 'rabbit', 'other')),
    breed TEXT,
    color TEXT,
    size TEXT CHECK (size IN ('small', 'medium', 'large')),
    description TEXT,
    distinctive_features TEXT,
    photos TEXT[],
    is_lost BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Índices
CREATE INDEX idx_pets_owner ON pets(owner_id);

-- RLS
ALTER TABLE pets ENABLE ROW LEVEL SECURITY;

-- Políticas
CREATE POLICY "Users can view all pets" ON pets FOR SELECT USING (true);
CREATE POLICY "Users can manage own pets" ON pets FOR ALL USING (auth.uid() = owner_id);

-- Trigger
CREATE TRIGGER update_pets_updated_at 
BEFORE UPDATE ON pets 
FOR EACH ROW 
EXECUTE FUNCTION update_updated_at_column();
```

## Verificación Final

Después de ejecutar la migración, prueba crear una mascota desde la app. El error debería desaparecer.

Si el error persiste:
1. Verifica que ejecutaste la migración correctamente
2. Verifica que las columnas existen (usando el SELECT de arriba)
3. Limpia la caché de la app (`npx expo start -c`)
4. Revisa los logs de la consola para ver si hay otros errores


