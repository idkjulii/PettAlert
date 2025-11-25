# 📋 Instrucciones: Configurar Base de Datos para Módulo de Mascotas

## ⚠️ IMPORTANTE: Lee esto primero

Estas instrucciones son para configurar las tablas necesarias para el módulo completo de "Mis Mascotas" con seguimiento de salud veterinaria.

## 📍 Paso 1: Ir a Supabase Dashboard

1. Abre tu navegador y ve a [supabase.com](https://supabase.com)
2. Inicia sesión en tu cuenta
3. Selecciona tu proyecto
4. En el menú lateral izquierdo, haz clic en **SQL Editor**

## 📍 Paso 2: Verificar que la tabla `pets` existe

Antes de ejecutar la migración, verifica que ya tienes la tabla básica `pets`:

```sql
-- Ejecuta esto para verificar
SELECT * FROM information_schema.tables 
WHERE table_name = 'pets';
```

**Si NO aparece ningún resultado**, primero necesitas crear la tabla básica. Ejecuta esto:

```sql
-- Crear tabla básica de mascotas (si no existe)
CREATE TABLE IF NOT EXISTS pets (
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

-- Crear índice
CREATE INDEX IF NOT EXISTS idx_pets_owner ON pets(owner_id);

-- Habilitar RLS
ALTER TABLE pets ENABLE ROW LEVEL SECURITY;

-- Políticas RLS para pets
CREATE POLICY IF NOT EXISTS "Users can view all pets" ON pets
    FOR SELECT USING (true);

CREATE POLICY IF NOT EXISTS "Users can manage own pets" ON pets
    FOR ALL USING (auth.uid() = owner_id);
```

## 📍 Paso 3: Ejecutar la migración de salud veterinaria

Ahora ejecuta la migración completa. Tienes dos opciones:

### Opción A: Copiar y pegar el archivo completo (Recomendado)

1. Abre el archivo: `backend/migrations/007_pet_health_tracking.sql`
2. Copia TODO el contenido del archivo
3. Pégalo en el SQL Editor de Supabase
4. Haz clic en **Run** (o presiona Ctrl+Enter)
5. Espera a que termine (puede tardar unos segundos)

### Opción B: Ejecutar sección por sección

Si prefieres ejecutar paso a paso, copia y ejecuta cada sección:

#### 3.1 Habilitar extensiones (si no están habilitadas)

```sql
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
```

#### 3.2 Crear todas las tablas

Copia y ejecuta TODO el contenido del archivo `backend/migrations/007_pet_health_tracking.sql`

## 📍 Paso 4: Verificar que todo se creó correctamente

Ejecuta este script para verificar que todas las tablas se crearon:

```sql
-- Verificar tablas creadas
SELECT 
    table_name,
    (SELECT COUNT(*) FROM information_schema.columns 
     WHERE table_name = t.table_name) as column_count
FROM information_schema.tables t
WHERE table_schema = 'public' 
  AND table_name IN (
    'pets',
    'historial_salud',
    'vacunacion_tratamiento',
    'medicamentos_activos',
    'indicador_bienestar',
    'recordatorio',
    'documento_medico',
    'plan_cuidado',
    'checklist_cuidado'
  )
ORDER BY table_name;
```

**Deberías ver 9 tablas** con sus respectivos conteos de columnas.

## 📍 Paso 5: Verificar políticas RLS

Ejecuta esto para verificar que las políticas de seguridad están activas:

```sql
-- Verificar políticas RLS
SELECT 
    schemaname,
    tablename,
    policyname,
    permissive,
    roles,
    cmd
FROM pg_policies
WHERE tablename IN (
    'pets',
    'historial_salud',
    'vacunacion_tratamiento',
    'medicamentos_activos',
    'indicador_bienestar',
    'recordatorio',
    'documento_medico',
    'plan_cuidado',
    'checklist_cuidado'
)
ORDER BY tablename, policyname;
```

**Deberías ver múltiples políticas** para cada tabla.

## 📍 Paso 6: Verificar la función SQL

Ejecuta esto para verificar que la función de resumen de salud existe:

```sql
-- Verificar función
SELECT 
    routine_name,
    routine_type
FROM information_schema.routines
WHERE routine_schema = 'public'
  AND routine_name = 'obtener_resumen_salud_mascota';
```

**Deberías ver 1 resultado** con el nombre de la función.

## 📍 Paso 7: Verificar Storage Buckets (para fotos)

1. En Supabase Dashboard, ve a **Storage** (en el menú lateral)
2. Verifica que existe el bucket `pet-photos`
3. Si NO existe, créalo:
   - Haz clic en **New bucket**
   - Nombre: `pet-photos`
   - Marca como **Public bucket**
   - Haz clic en **Create bucket**

## ✅ Verificación Final

Ejecuta este script completo para verificar TODO:

```sql
-- VERIFICACIÓN COMPLETA
DO $$
DECLARE
    table_count INTEGER;
    policy_count INTEGER;
    function_count INTEGER;
BEGIN
    -- Contar tablas
    SELECT COUNT(*) INTO table_count
    FROM information_schema.tables
    WHERE table_schema = 'public' 
      AND table_name IN (
        'pets', 'historial_salud', 'vacunacion_tratamiento',
        'medicamentos_activos', 'indicador_bienestar', 'recordatorio',
        'documento_medico', 'plan_cuidado', 'checklist_cuidado'
      );
    
    -- Contar políticas
    SELECT COUNT(*) INTO policy_count
    FROM pg_policies
    WHERE tablename IN (
        'pets', 'historial_salud', 'vacunacion_tratamiento',
        'medicamentos_activos', 'indicador_bienestar', 'recordatorio',
        'documento_medico', 'plan_cuidado', 'checklist_cuidado'
    );
    
    -- Contar función
    SELECT COUNT(*) INTO function_count
    FROM information_schema.routines
    WHERE routine_schema = 'public'
      AND routine_name = 'obtener_resumen_salud_mascota';
    
    RAISE NOTICE '✅ Tablas creadas: % (esperado: 9)', table_count;
    RAISE NOTICE '✅ Políticas RLS: % (esperado: al menos 18)', policy_count;
    RAISE NOTICE '✅ Función SQL: % (esperado: 1)', function_count;
    
    IF table_count = 9 AND policy_count >= 18 AND function_count = 1 THEN
        RAISE NOTICE '🎉 ¡TODO ESTÁ CONFIGURADO CORRECTAMENTE!';
    ELSE
        RAISE WARNING '⚠️ Algo falta. Revisa los números arriba.';
    END IF;
END $$;
```

## 🚨 Solución de Problemas

### Error: "relation already exists"
- **Causa**: Las tablas ya existen
- **Solución**: No es un problema, las tablas se crean con `IF NOT EXISTS`, así que se saltan si ya existen

### Error: "permission denied"
- **Causa**: No tienes permisos suficientes
- **Solución**: Asegúrate de estar usando el SQL Editor con permisos de administrador

### Error: "function already exists"
- **Causa**: La función ya existe
- **Solución**: No es un problema, el script usa `CREATE OR REPLACE FUNCTION`

### Error: "extension does not exist"
- **Causa**: La extensión uuid-ossp no está disponible
- **Solución**: En Supabase normalmente está disponible. Si no, contacta soporte.

## 📝 Resumen de lo que se crea

Después de ejecutar la migración, tendrás:

1. **9 tablas nuevas** para el módulo de salud:
   - `historial_salud` - Historial médico
   - `vacunacion_tratamiento` - Vacunas y tratamientos
   - `medicamentos_activos` - Medicamentos actuales
   - `indicador_bienestar` - Métricas de salud
   - `recordatorio` - Recordatorios
   - `documento_medico` - Documentos médicos
   - `plan_cuidado` - Planes de cuidado
   - `checklist_cuidado` - Items del plan
   - `pets` - (si no existía)

2. **Políticas RLS** para seguridad (cada usuario solo ve/gestiona sus propias mascotas)

3. **Índices** para mejorar el rendimiento

4. **Función SQL** `obtener_resumen_salud_mascota()` para calcular resúmenes de salud

5. **Triggers** para actualizar `updated_at` automáticamente

## 🎯 Siguiente Paso

Una vez que hayas ejecutado todo correctamente:

1. **Reinicia tu app** (si está corriendo)
2. **Prueba crear una mascota** desde la app
3. **Verifica que puedas ver el detalle** con las pestañas de salud

¡Listo! 🎉

