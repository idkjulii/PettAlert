# ✅ Verificación: Migración CLIP → MegaDescriptor

## Estado de la Migración

### ✅ Completado
1. **Migración SQL ejecutada** - Base de datos actualizada a `vector(1536)`
2. **Backend configurado** - Usando MegaDescriptor-L-384
3. **Documentación corregida** - Referencias a 1536 dimensiones

### ⚠️ Pendiente Verificar

#### 1. Variable de Entorno para Generación Local
El código está configurado para generar embeddings localmente, pero la variable por defecto es `false`:

```python
GENERATE_EMBEDDINGS_LOCALLY = (
    os.getenv("GENERATE_EMBEDDINGS_LOCALLY", "false").lower() in ("1", "true", "yes")
)
```

**Verifica tu archivo `.env`** debe tener:
```env
GENERATE_EMBEDDINGS_LOCALLY=true
AUTO_SEND_REPORTS_TO_N8N=true
```

#### 2. Embeddings Existentes
Los reportes creados antes de la migración:
- ❌ Tienen embeddings de 512 dims (CLIP) o ninguno
- ❌ Necesitan regenerarse con MegaDescriptor (1536 dims)

---

## 🔍 Verificaciones Recomendadas

### 1. Verificar Schema de Base de Datos
Ejecuta en Supabase SQL Editor:

```sql
-- Verificar columna embedding
SELECT 
    column_name, 
    data_type,
    udt_name
FROM information_schema.columns 
WHERE table_name = 'reports' 
  AND column_name = 'embedding';

-- Verificar índice HNSW
SELECT 
    indexname, 
    indexdef 
FROM pg_indexes 
WHERE tablename = 'reports' 
  AND indexname LIKE '%embedding%';

-- Ver cantidad de reportes con/sin embeddings
SELECT 
    COUNT(*) as total_reportes,
    COUNT(embedding) as con_embedding,
    COUNT(*) - COUNT(embedding) as sin_embedding,
    COUNT(CASE WHEN embedding IS NOT NULL 
               THEN array_length(embedding::float[], 1) 
               END) as reportes_con_dims
FROM public.reports
WHERE status = 'active';

-- Ver dimensiones de embeddings existentes (si hay)
SELECT 
    id,
    array_length(embedding::float[], 1) as dimensiones,
    created_at
FROM public.reports 
WHERE embedding IS NOT NULL 
LIMIT 5;
```

### 2. Probar Generación de Embedding
Prueba que el backend genere embeddings correctamente:

```bash
# Navega al directorio backend
cd backend

# Prueba generación de embedding con una imagen
curl -X POST "http://127.0.0.1:8010/embeddings/generate" \
  -F "file=@test_image.jpg"

# Deberías ver:
# {
#   "dimensions": 1536,
#   "model": "MegaDescriptor-L-384"
# }
```

### 3. Verificar Variables de Entorno
Crea o actualiza tu archivo `.env` en `backend/`:

```env
# Supabase
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_KEY=tu-clave-service-key
DATABASE_URL=postgresql://...

# Embeddings (MegaDescriptor se descarga automáticamente)
GENERATE_EMBEDDINGS_LOCALLY=true

# N8N ya no se usa - el backend procesa todo localmente

# Embeddings (IMPORTANTE)
GENERATE_EMBEDDINGS_LOCALLY=true
# N8N ya no se usa - el backend procesa todo localmente
```

---

## 🔄 Regenerar Embeddings Existentes

Si tienes reportes creados antes de la migración, necesitas regenerarlos:

### Opción 1: Script Automático (Recomendado)

```bash
cd backend
python -m scripts.regenerate_embeddings_mega
```

Este script:
- ✅ Encuentra todos los reportes con fotos
- ✅ Descarga las imágenes
- ✅ Genera embeddings con MegaDescriptor (1536 dims)
- ✅ Los guarda en Supabase
- ✅ Maneja errores y reintentos

### Opción 2: Verificar Embeddings Faltantes

```bash
cd backend
python -m scripts.generate_missing_embeddings
```

Este script solo regenera reportes que NO tienen embedding.

---

## 📊 Checklist Post-Migración

- [ ] Base de datos tiene columna `embedding vector(1536)`
- [ ] Índice HNSW existe y está activo
- [ ] Función RPC `update_report_embedding` acepta 1536 dims
- [ ] Backend genera embeddings de 1536 dimensiones
- [ ] Variable `GENERATE_EMBEDDINGS_LOCALLY=true` en `.env`
- [ ] Nuevos reportes generan embeddings automáticamente
- [ ] Reportes existentes regenerados con MegaDescriptor

---

## 🧪 Prueba Completa del Flujo

### 1. Crear un reporte de prueba desde el frontend
- Crea un reporte con foto
- Verifica en los logs del backend que dice:
  ```
  📸 [embedding] Reporte creado con fotos. Generando embedding...
  ✅ [embedding] Embedding generado y guardado
  ```

### 2. Verificar en Supabase
```sql
SELECT 
    id,
    array_length(embedding::float[], 1) as dims,
    created_at
FROM public.reports 
ORDER BY created_at DESC 
LIMIT 1;

-- Debería mostrar dims = 1536
```

### 3. Probar búsqueda por similitud
```bash
curl -X POST "http://127.0.0.1:8010/embeddings/search_image?top_k=5" \
  -F "file=@test_image.jpg"
```

---

## 🚨 Posibles Problemas

### Error: "dimension mismatch"
**Causa:** La función RPC no se actualizó correctamente.

**Solución:** Vuelve a ejecutar la parte de la migración que actualiza la función RPC:
```sql
CREATE OR REPLACE FUNCTION update_report_embedding(
    report_id uuid,
    embedding_vector float[]
) RETURNS boolean AS $$
BEGIN
    UPDATE public.reports 
    SET embedding = embedding_vector::vector(1536)
    WHERE id = report_id;
    
    RETURN FOUND;
END;
$$ LANGUAGE plpgsql SECURITY DEFINER;
```

### Embeddings no se generan automáticamente
**Causa:** Variable de entorno no configurada.

**Solución:** 
1. Verifica que el archivo `.env` tenga `GENERATE_EMBEDDINGS_LOCALLY=true`
2. Reinicia el backend
3. Verifica los logs al crear un reporte

### Backend no carga el modelo
**Causa:** Primera carga descarga ~900MB desde HuggingFace.

**Solución:** Espera unos minutos, el modelo se descarga automáticamente la primera vez.

---

## 📝 Notas

- **Rendimiento:** Con índice HNSW, las búsquedas son ~10-50ms en 10k reportes
- **Espacio:** Cada embedding ocupa ~6KB (1536 floats × 4 bytes)
- **Precisión:** MegaDescriptor está especializado en animales, mejor que CLIP
- **Compatibilidad:** 1536 < 2000, funciona con todas las versiones de pgvector

---

**Última actualización:** $(date)

