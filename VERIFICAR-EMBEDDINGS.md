# 🔍 Guía para Verificar y Solucionar Problemas con Embeddings

## Problema
Los embeddings no se están guardando en la columna `embedding` de la tabla `reports` en Supabase.

## Pasos de Diagnóstico

### 1. Verificar que la función RPC existe en Supabase

**Ejecuta este SQL en el SQL Editor de Supabase:**

```sql
-- Verificar que la función existe
SELECT 
    proname as function_name,
    pg_get_function_arguments(oid) as arguments
FROM pg_proc 
WHERE proname = 'update_report_embedding';
```

**Si no existe, ejecuta la migración:**

```sql
-- Función SQL para actualizar embedding correctamente
CREATE OR REPLACE FUNCTION update_report_embedding(
    report_id uuid,
    embedding_vector float[]
) RETURNS boolean AS $$
BEGIN
    UPDATE public.reports 
    SET embedding = embedding_vector::vector(512)
    WHERE id = report_id;
    
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql;
```

### 2. Verificar que la columna embedding existe

```sql
-- Verificar estructura de la tabla
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'reports' 
AND column_name = 'embedding';
```

**Si no existe, ejecuta:**

```sql
-- Habilitar pgvector
CREATE EXTENSION IF NOT EXISTS vector;

-- Agregar columna de embedding
ALTER TABLE public.reports
  ADD COLUMN IF NOT EXISTS embedding vector(512);

-- Crear índice para búsqueda rápida
CREATE INDEX IF NOT EXISTS idx_reports_embedding_ivf
  ON public.reports USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

### 3. Ejecutar script de diagnóstico

```bash
# Desde la carpeta backend
cd backend
python test_embedding_generation.py
```

Este script verificará:
- ✅ Conexión con Supabase
- ✅ Existencia de la función RPC
- ✅ Generación de embeddings
- ✅ Flujo completo de guardado

### 4. Verificar que el backend está corriendo

```bash
# Verificar salud del backend
curl http://localhost:8003/health
```

### 5. Probar manualmente la generación de embeddings

Usa el endpoint de embeddings del backend para generar embeddings para un reporte específico.

### 6. Verificar logs del backend

Cuando creas un reporte, deberías ver en los logs del backend:

```
📸 [embedding] Reporte creado con fotos. Generando embedding para reporte {id}...
🔄 [embedding] Generando embedding para reporte {id} desde {url}
💾 [embedding] Guardando embedding en BD para reporte {id}...
✅ [embedding] Embedding guardado exitosamente para reporte {id}
```

### 7. Verificar desde el frontend

Cuando creas un reporte desde la app, verifica en la consola del navegador que los embeddings se están generando correctamente.

## Soluciones Comunes

### Problema: Función RPC no existe

**Solución:** Ejecuta la migración `002_update_embedding_function.sql` en Supabase.

### Problema: Backend no accesible

**Solución:** 
1. Verifica que el backend esté corriendo en el puerto 8003
2. Verifica que `EXPO_PUBLIC_BACKEND_URL` esté configurada correctamente en el frontend
3. Verifica la configuración de red/firewall

### Problema: Embeddings se generan pero no se guardan

**Solución:**
1. Verifica que la función RPC tenga permisos correctos
2. Verifica que `SUPABASE_SERVICE_KEY` tenga permisos de escritura
3. Revisa los logs del backend para ver errores específicos

### Problema: No se llama al endpoint

**Solución:**
1. Verifica que el frontend esté llamando al endpoint correcto del backend
2. Verifica que el backend esté en la URL correcta
3. Revisa la consola del navegador para errores de red

## Generar Embeddings para Reportes Existentes

Si tienes reportes existentes sin embeddings, puedes procesarlos usando el script:

```bash
cd backend
python scripts/generate_missing_embeddings.py
```

Esto generará embeddings para todos los reportes que tengan fotos.

## Verificar que los Embeddings se Guardaron

En Supabase, ejecuta:

```sql
-- Ver cuántos reportes tienen embeddings
SELECT 
    COUNT(*) as total_reports,
    COUNT(embedding) as reports_with_embedding,
    COUNT(*) - COUNT(embedding) as reports_without_embedding
FROM public.reports
WHERE status = 'active';

-- Ver un embedding de ejemplo
SELECT id, embedding 
FROM public.reports 
WHERE embedding IS NOT NULL 
LIMIT 1;
```
