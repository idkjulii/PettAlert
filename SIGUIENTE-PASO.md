# 🎯 Siguiente Paso: Post-Migración MegaDescriptor

## ✅ Lo que Ya Completaste

1. ✅ **Migración SQL ejecutada** - Base de datos actualizada a `vector(1536)`
2. ✅ **Backend configurado** - MegaDescriptor-L-384 funcionando
3. ✅ **Documentación corregida** - Referencias a 1536 dimensiones
4. ✅ **Scripts preparados** - Listos para regenerar embeddings

---

## 🔴 LO QUE DEBES HACER AHORA

### 1. Verificar el Estado Actual (5 minutos)

Ejecuta este script para ver cuántos embeddings necesitan regenerarse:

```bash
cd backend
python verificar_estado_embeddings.py
```

El script te mostrará:
- ✅ Cuántos reportes tienen embeddings
- ⚠️ Cuántos necesitan regenerarse
- 📊 Las dimensiones de los embeddings existentes (512 vs 1536)
- ⚙️ Estado de tus variables de entorno

---

### 2. Regenerar Embeddings (Tiempo variable)

Si el script anterior muestra que tienes reportes que necesitan embeddings:

```bash
cd backend
python -m scripts.regenerate_embeddings_mega
```

**¿Cuánto tarda?**
- ~2-3 segundos por reporte
- 10 reportes = ~30 segundos
- 100 reportes = ~5 minutos
- 1000 reportes = ~50 minutos

El script muestra el progreso y maneja errores automáticamente.

---

### 3. Verificar que Funciona (2 minutos)

Prueba crear un nuevo reporte con foto desde tu app y verifica:

1. **En los logs del backend** deberías ver:
```
📸 [embedding] Reporte creado con fotos. Generando embedding...
🔄 Cargando MegaDescriptor en cpu...
📊 Dimensión del modelo: 1536
✅ [embedding] Embedding generado y guardado
```

2. **En Supabase SQL Editor** ejecuta:
```sql
SELECT 
    id,
    array_length(embedding::float[], 1) as dims,
    created_at
FROM public.reports 
ORDER BY created_at DESC 
LIMIT 3;
```

Deberías ver `dims = 1536` para los reportes nuevos.

---

## ⚙️ Configuración Importante

Verifica que tu archivo `backend/.env` tenga:

```env
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_KEY=tu-service-key

# IMPORTANTE: Esto debe estar en true
GENERATE_EMBEDDINGS_LOCALLY=true
AUTO_SEND_REPORTS_TO_N8N=true
```

Si no tienes `GENERATE_EMBEDDINGS_LOCALLY=true`, los nuevos reportes NO generarán embeddings automáticamente.

---

## 📊 Cómo Saber si Todo Está Bien

✅ **Señales de que funciona correctamente:**
- Nuevos reportes con foto generan embeddings de 1536 dims
- Búsquedas por imagen devuelven resultados
- Logs del backend muestran "✅ Embedding generado y guardado"

⚠️ **Señales de problemas:**
- Error "dimension mismatch" → La migración SQL no se aplicó correctamente
- Embeddings de 512 dims → Necesitas regenerar (ejecuta el script)
- No se generan embeddings → Verifica `GENERATE_EMBEDDINGS_LOCALLY=true`

---

## 🆘 Solución Rápida de Problemas

### Problema: "dimension mismatch"
```sql
-- Ejecuta esto en Supabase SQL Editor para verificar la dimensión
SELECT 
    column_name, 
    udt_name
FROM information_schema.columns 
WHERE table_name = 'reports' 
  AND column_name = 'embedding';

-- Debería decir: vector o _vector
-- Si dice vector(512), la migración no se aplicó
```

### Problema: Modelo no se descarga
- Primera vez descarga ~900MB de HuggingFace
- Puede tardar 5-10 minutos
- Necesitas internet y ~1GB libre en disco

### Problema: Embeddings no se generan automáticamente
```bash
# Verifica tu .env
cat backend/.env | grep GENERATE_EMBEDDINGS_LOCALLY

# Si no dice "true", agrégalo:
echo "GENERATE_EMBEDDINGS_LOCALLY=true" >> backend/.env

# Reinicia el backend
```

---

## 📁 Archivos Creados

Estos archivos te ayudan en el proceso:

- ✅ `ESTADO-PROYECTO.md` - Resumen completo del estado
- ✅ `VERIFICACION-MIGRACION.md` - Guía detallada de verificación
- ✅ `backend/verificar_estado_embeddings.py` - Script de diagnóstico
- ✅ `backend/MIGRACION-MEGADESCRIPTOR.md` - Guía de migración corregida

---

## 🎯 Resumen de 3 Pasos

```bash
# 1. Verificar estado
cd backend
python verificar_estado_embeddings.py

# 2. Regenerar embeddings (si es necesario)
python -m scripts.regenerate_embeddings_mega

# 3. Crear un reporte de prueba y verificar logs
```

---

**¿Listo?** Empieza con el Paso 1 (verificar estado). El script te dirá exactamente qué hacer después.

