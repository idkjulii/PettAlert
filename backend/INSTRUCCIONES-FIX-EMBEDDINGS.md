# 🔧 FIX: Embeddings Guardados como String

## Problema Encontrado

Los embeddings se estaban guardando como **STRING** en lugar de **ARRAY/VECTOR**, por lo que la búsqueda de matches no funcionaba.

```
❌ Antes: '[-0.03486755,0.0029942612,...]' (STRING de 19,227 caracteres)
✅ Ahora: [-0.03486755,0.0029942612,...]  (VECTOR de 1536 dimensiones)
```

---

## Solución Aplicada

### 1. Migración SQL (`006_fix_embedding_rpc.sql`)

Se modificó la función RPC `update_report_embedding` para:
- Aceptar el embedding como **text** (JSON string)
- Convertir explícitamente a `vector(1536)`

### 2. Código del Backend

Se modificaron los archivos:
- `backend/routers/reports.py` - Para usar `json.dumps()` al guardar
- `backend/scripts/regenerate_embeddings_mega.py` - Para usar `json.dumps()` al regenerar

---

## Pasos para Aplicar el Fix

### PASO 1: Aplicar Migración en Supabase

1. Ve a **Supabase Dashboard → SQL Editor**
2. Ejecuta el contenido de `backend/migrations/006_fix_embedding_rpc.sql`
3. Verifica que retorne `Success. No rows returned`

### PASO 2: Reiniciar el Backend

```bash
# Detener el backend actual (Ctrl+C)
# Reiniciar:
cd backend
python -m uvicorn main:app --host 0.0.0.0 --port 8003 --reload
```

Espera ~60 segundos a que cargue MegaDescriptor.

### PASO 3: Regenerar TODOS los Embeddings

```bash
cd backend
python regenerar_embeddings_ahora.py
```

Esto regenerará todos los embeddings **correctamente como vectores**.

### PASO 4: Verificar

```bash
python verificar_embeddings_detalle.py
```

Deberías ver:
```
✅ Trueno (lost):
   Tipo: ARRAY (dimensiones: 1536)
   
✅ Tito (lost):
   Tipo: ARRAY (dimensiones: 1536)
   
✅ Rox (lost):
   Tipo: ARRAY (dimensiones: 1536)
   
✅ None (found):
   Tipo: ARRAY (dimensiones: 1536)
```

### PASO 5: Probar Matches

Desde la app móvil:
1. Abre un reporte
2. Toca "Buscar coincidencias"
3. **Ahora debería funcionar** y mostrar matches si hay similitud >= 70%

---

## ¿Por Qué Pasó Esto?

La librería `postgrest-py` (Supabase Python) serializa los arrays de Python a JSON strings al enviarlos a funciones RPC. PostgreSQL necesita que el cast `text::vector(1536)` sea explícito para convertir correctamente el JSON string a un vector de pgvector.

---

## Verificación Rápida

Para verificar que todo funciona:

```bash
python debug_matches.py
```

Deberías ver similitudes calculadas correctamente (0.0 a 1.0).

---

## Notas

- **Todos los reportes creados ANTES del fix:** Tienen embeddings como STRING → Necesitan regenerarse
- **Todos los reportes creados DESPUÉS del fix:** Tendrán embeddings como VECTOR automáticamente ✅




