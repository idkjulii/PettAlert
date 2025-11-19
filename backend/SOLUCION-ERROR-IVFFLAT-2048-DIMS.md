# 🔧 Solución: Error pgvector con 2048 dimensiones

## ❌ Problema

Al ejecutar la migración para MegaDescriptor, obtienes este error:

```
ERROR: 54000: column cannot have more than 2000 dimensions for ivfflat index
```

O incluso con HNSW:

```
ERROR: 54000: column cannot have more than 2000 dimensions for hnsw index
```

## 📖 Explicación

**pgvector** tiene límites de dimensiones que dependen de la versión:

- **Versiones antiguas** (< 0.7.0): Límite de **2000 dims** para todos los índices
- **Versiones nuevas** (≥ 0.7.0): Soportan **16,000 dims** para HNSW

MegaDescriptor genera embeddings de **2048 dimensiones**, que excede el límite de versiones antiguas.

## ✅ Soluciones

### **Solución 1: Sin Índice (RECOMENDADA para empezar)**

La más simple. Funciona bien hasta ~10,000 reportes.

```sql
-- No crear índice
-- La búsqueda será secuencial pero funcional
ALTER TABLE public.reports
  ADD COLUMN embedding vector(2048);
```

**Ventajas:**
- ✅ Funciona inmediatamente
- ✅ No requiere actualizar pgvector
- ✅ Suficiente para la mayoría de casos

**Desventajas:**
- ⚠️ Búsquedas más lentas con muchos reportes (>10k)

### **Solución 2: Verificar versión de pgvector**

Verifica qué versión tienes:

```sql
SELECT * FROM pg_extension WHERE extname = 'vector';
```

Si ves versión **≥ 0.7.0**, entonces puedes usar HNSW con 2048 dims.

### **Solución 3: Actualizar pgvector (Requiere permisos)**

Si tienes acceso, actualiza pgvector en Supabase:

```sql
ALTER EXTENSION vector UPDATE;
```

Luego crea el índice:

```sql
CREATE INDEX idx_reports_embedding_hnsw
  ON public.reports USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

## 🚀 Qué hacer ahora

1. **Copia de nuevo** el contenido actualizado de `backend/migrations/005_migrate_to_megadescriptor.sql`
2. **Pégalo en Supabase SQL Editor**
3. **Ejecuta la query**
4. Ahora debería funcionar sin errores

## 📊 Comparación: IVFFlat vs HNSW

| Característica | IVFFlat | HNSW |
|---------------|---------|------|
| Límite dimensiones | 2000 | Sin límite |
| Velocidad construcción | ⚡ Rápido | 🐌 Más lento |
| Velocidad búsqueda | 🐌 Aceptable | ⚡ Muy rápido |
| Precisión | 📊 Buena | 📈 Excelente |
| Uso memoria | 💾 Bajo | 💾 Medio |
| **Recomendado para 2048 dims** | ❌ No | ✅ Sí |

## 🎯 Parámetros HNSW

Los parámetros que usamos:

- **m = 16**: Número de conexiones por nodo (más = mejor precisión, más memoria)
- **ef_construction = 64**: Calidad durante construcción (más = mejor índice, más tiempo)

Estos son buenos valores por defecto para 2048 dimensiones.

## 📚 Referencias

- [pgvector GitHub - HNSW](https://github.com/pgvector/pgvector#hnsw)
- [Documentación HNSW](https://github.com/nmslib/hnswlib)

---

**Resumen**: HNSW es mejor que IVFFlat para MegaDescriptor (2048 dims). El archivo de migración ya está corregido.

