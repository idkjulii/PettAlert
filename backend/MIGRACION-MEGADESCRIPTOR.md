# 🚀 Guía de Migración: CLIP → MegaDescriptor

Esta guía te ayudará a migrar tu base de datos de embeddings CLIP (512 dims) a MegaDescriptor (1536 dims).

## ⚠️ ADVERTENCIAS IMPORTANTES

1. **Esta migración ELIMINARÁ todos los embeddings existentes** porque cambian las dimensiones de 512 a 1536. Deberás regenerar todos los embeddings después de la migración.

2. **Índice HNSW**: La migración crea automáticamente un índice HNSW para búsquedas rápidas. Como 1536 < 2000, es compatible con todas las versiones de pgvector.

## 📋 Pasos de Migración

### **Paso 1: Ejecutar la Migración SQL en Supabase**

1. Abre tu proyecto en [Supabase Dashboard](https://app.supabase.com)
2. Ve a **SQL Editor** (en el menú lateral)
3. Haz clic en **New Query**
4. Copia y pega el contenido completo del archivo:
   ```
   backend/migrations/005_migrate_to_megadescriptor.sql
   ```
5. Haz clic en **Run** (o presiona `Ctrl+Enter`)
6. Verifica que no haya errores en la salida

### **Paso 2: Verificar la Migración**

Ejecuta esta consulta en Supabase SQL Editor para verificar:

```sql
-- Verificar que la columna tiene 1536 dimensiones
SELECT 
    column_name, 
    data_type,
    udt_name
FROM information_schema.columns 
WHERE table_name = 'reports' 
  AND column_name = 'embedding';

-- Deberías ver: embedding | USER-DEFINED | vector
```

### **Paso 3: Regenerar Embeddings**

Después de la migración, necesitas regenerar todos los embeddings. Tienes dos opciones:

#### **Opción A: Regeneración Automática (Recomendada)**

Los nuevos reportes generarán embeddings automáticamente con MegaDescriptor cuando se creen.

#### **Opción B: Regeneración Manual de Reportes Existentes**

Crea y ejecuta el script de regeneración:

```bash
cd backend
python -m scripts.regenerate_embeddings_mega
```

> **Nota**: Este script aún no existe. Debes crearlo siguiendo el ejemplo que se proporcionó en la guía de migración.

## 🔍 Verificación Post-Migración

### **1. Probar Generación de Embedding**

```bash
# Desde el backend
curl -X POST "http://127.0.0.1:8010/embeddings/generate" \
  -F "file=@test_image.jpg"
```

Deberías ver en la respuesta:
```json
{
  "dimensions": 1536,
  "model": "MegaDescriptor-L-384"
}
```

### **2. Verificar en Base de Datos**

```sql
-- Verificar que un embedding tiene 1536 dimensiones
SELECT 
    id,
    array_length(embedding::float[], 1) as dims
FROM public.reports 
WHERE embedding IS NOT NULL 
LIMIT 1;

-- Deberías ver: dims = 1536
```

## 📊 Cambios Realizados

| Aspecto | Antes (CLIP) | Después (MegaDescriptor) |
|---------|--------------|--------------------------|
| Dimensiones | 512 | 1536 |
| Modelo | ViT-B/32 | Swin-L-384 |
| Tamaño imagen | 224x224 | 384x384 |
| Índice | IVFFlat | HNSW |
| Especialización | General | Animales |
| Tamaño modelo | ~150MB | ~900MB |

## 🐛 Solución de Problemas

### **Error: "column cannot have more than 2000 dimensions"**

Este error no debería ocurrir porque MegaDescriptor genera 1536 dimensiones (menos que el límite de 2000). Si ves este error:

1. Verifica tu versión de pgvector: `SELECT * FROM pg_extension WHERE extname = 'vector';`
2. Si es < 0.5.0, contacta a Supabase para actualizar
3. La migración crea automáticamente un índice HNSW que funciona con todas las versiones modernas de pgvector

### **Error: "dimension mismatch"**

Si ves este error, significa que la migración no se ejecutó correctamente. Verifica:
1. Que ejecutaste la migración SQL completa
2. Que la columna `embedding` es `vector(1536)`
3. Que la función RPC `update_report_embedding` acepta 1536 dims

### **Error: "model not found"**

El modelo MegaDescriptor se descarga automáticamente la primera vez. Asegúrate de:
- Tener conexión a internet
- Tener ~1GB de espacio libre
- Esperar la descarga (puede tardar varios minutos)

### **Embeddings no se generan**

Verifica que:
1. `timm` y `huggingface-hub` están instalados
2. El backend está corriendo
3. Revisa los logs del backend para ver errores

## ✅ Checklist Final

- [ ] Migración SQL ejecutada en Supabase
- [ ] Columna `embedding` es `vector(1536)`
- [ ] Índice HNSW creado automáticamente
- [ ] Función RPC actualizada
- [ ] Backend reiniciado
- [ ] Prueba de generación de embedding exitosa
- [ ] Embeddings regenerados (opcional, para reportes existentes)

## 📝 Notas Adicionales

- **Primera carga**: La primera vez que uses MegaDescriptor, descargará ~900MB desde HuggingFace
- **Rendimiento**: Los embeddings de 1536 dims son más precisos pero ocupan 3x más espacio que CLIP
- **Con índice HNSW**: La migración crea un índice HNSW automáticamente (1536 < 2000, compatible con todas las versiones de pgvector)
- **Velocidad con índice**: ~10-50ms para buscar en 10k reportes
- **Velocidad sin índice**: ~1s para buscar en 10k reportes

---

**¿Problemas?** Revisa los logs del backend y la consola de Supabase para más detalles.

