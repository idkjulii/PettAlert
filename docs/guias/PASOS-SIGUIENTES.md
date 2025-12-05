# 🚀 Pasos Siguientes - Guía de Implementación

## ✅ Checklist de Implementación

### 📋 Fase 1: Preparación (15 minutos)

#### 1.1 Verificar Base de Datos en Supabase
- [ ] Ir a Supabase Dashboard → SQL Editor
- [ ] Ejecutar estas queries para verificar:

```sql
-- Verificar que pgvector esté habilitado
SELECT * FROM pg_extension WHERE extname = 'vector';

-- Verificar que la columna embedding exista
SELECT column_name, data_type 
FROM information_schema.columns 
WHERE table_name = 'reports' AND column_name = 'embedding';
```

#### 1.2 Ejecutar Migraciones SQL
- [ ] Abrir `backend/migrations/003_rag_functions.sql`
- [ ] Copiar todo el contenido
- [ ] Pegarlo en Supabase SQL Editor
- [ ] Ejecutar (Run)
- [ ] Verificar que no haya errores

#### 1.3 Configurar Variables de Entorno
- [ ] Abrir `backend/.env`
- [ ] Verificar que existan:
  ```env
  SUPABASE_URL=https://tu-proyecto.supabase.co
  SUPABASE_SERVICE_KEY=tu_service_key
  ```

---

### 📋 Fase 2: Configurar Generación Automática de Embeddings (30 minutos)

El backend ya genera embeddings automáticamente cuando se crean reportes. Todo se procesa localmente con MegaDescriptor.

---

### 📋 Fase 3: Probar el Sistema (20 minutos)

#### 3.1 Verificar que el Backend Funcione
- [ ] Iniciar el backend:
  ```bash
  cd backend
  python -m uvicorn main:app --reload --port 8003
  ```
- [ ] Verificar que esté corriendo:
  ```bash
  curl http://localhost:8003/health
  ```

#### 3.2 Verificar Endpoints de RAG
- [ ] Probar endpoint de estadísticas:
  ```bash
  curl http://localhost:8003/rag/stats
  ```
- [ ] Deberías ver algo como:
  ```json
  {
    "total_reports": 10,
    "reports_with_embedding": 0,
    "active_reports_with_embedding": 0,
    "coverage_percentage": 0.0
  }
  ```

#### 3.3 Probar con una Imagen de Prueba
- [ ] Crear un reporte de prueba en tu app
- [ ] Verificar que se generó el embedding:
  ```bash
  curl "http://localhost:8003/rag/has-embedding/{report_id}"
  ```

---

### 📋 Fase 4: Procesar Imágenes Existentes (Variable)

#### 4.1 Procesar Todas las Imágenes
- [ ] Usar el script de generación de embeddings:
  ```bash
  cd backend
  python scripts/generate_missing_embeddings.py
  ```
- [ ] Monitorear progreso:
  ```bash
  curl "http://localhost:8003/rag/stats"
  ```

#### 4.2 Verificar Resultados
- [ ] Esperar a que termine el procesamiento
- [ ] Verificar estadísticas:
  ```bash
  curl "http://localhost:8003/rag/stats"
  ```
- [ ] Deberías ver que `reports_with_embedding` aumentó

---

### 📋 Fase 5: Implementar Búsqueda RAG (30 minutos)

#### 5.1 Crear Función de Búsqueda en Frontend
- [ ] Abrir tu servicio de búsqueda (probablemente `src/services/aiSearch.js`)
- [ ] Agregar función para búsqueda RAG:

```javascript
searchWithRAG: async (imageUri, searchParams) => {
  try {
    // 1. Generar embedding de la imagen de búsqueda
    const formData = new FormData();
    formData.append("file", {
      uri: imageUri,
      type: "image/jpeg",
      name: "search.jpg",
    });

    const embeddingRes = await fetch(buildUrl('EMBEDDINGS_GENERATE'), {
      method: "POST",
      body: formData,
    });

    if (!embeddingRes.ok) {
      throw new Error("Error generando embedding");
    }

    const { embedding } = await embeddingRes.json();

    // 2. Buscar usando RAG
    const searchRes = await fetch(buildUrl('RAG_SEARCH'), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        embedding: embedding,
        match_threshold: searchParams.threshold || 0.7,
        match_count: searchParams.limit || 10,
        filter_species: searchParams.species,
        filter_type: searchParams.type,
      }),
    });

    if (!searchRes.ok) {
      throw new Error("Error en búsqueda RAG");
    }

    const results = await searchRes.json();

    return {
      success: true,
      data: {
        results: results.results || [],
        count: results.count || 0,
      },
      error: null,
    };
  } catch (error) {
    console.error("Error en búsqueda RAG:", error);
    return {
      success: false,
      data: null,
      error: error.message,
    };
  }
}
```

#### 5.2 Agregar URLs en Config
- [ ] Abrir `src/config/backend.js` o similar
- [ ] Agregar:
  ```javascript
  EMBEDDINGS_GENERATE: '/embeddings/generate',
  RAG_SEARCH: '/rag/search',
  RAG_SEARCH_WITH_LOCATION: '/rag/search-with-location',
  ```

#### 5.3 Probar Búsqueda RAG
- [ ] En tu app, probar búsqueda con una imagen
- [ ] Verificar que encuentre resultados similares

---

### 📋 Fase 6: Optimización y Monitoreo

#### 6.1 Verificar Índices en Supabase
- [ ] Ir a Supabase Dashboard → Database → Indexes
- [ ] Verificar que existan:
  - `idx_reports_embedding_ivf`
  - `idx_reports_location` (si existe columna location)

#### 6.2 Configurar Monitoreo
- [ ] Agregar logging en el backend para ver errores
- [ ] Configurar alertas si el procesamiento falla

#### 6.3 Optimizar Búsquedas
- [ ] Ajustar `match_threshold` según tus necesidades:
  - `0.8` = Muy estricto (solo muy similares)
  - `0.7` = Balanceado (recomendado)
  - `0.5` = Menos estricto (más resultados)

---

## 🎯 Orden Recomendado de Ejecución

### Hoy (1 hora):
1. ✅ Fase 1: Preparación
2. ✅ Fase 2: Configurar generación automática de embeddings
3. ✅ Fase 3: Probar el Sistema

### Esta Semana:
4. ✅ Fase 4: Procesar Imágenes Existentes
5. ✅ Fase 5: Implementar Búsqueda RAG

### Próximos Días:
6. ✅ Fase 6: Optimización y Monitoreo

---

## 🐛 Solución de Problemas Comunes

### Error: "No se puede generar embeddings"
- Verificar que el backend esté corriendo
- Verificar que las variables de entorno estén configuradas
- Verificar firewall/red

### Error: "Embedding debe tener 512 dimensiones"
- Verificar que el endpoint `/embeddings/generate` funcione
- Probar directamente:
  ```bash
  curl -X POST "http://localhost:8003/embeddings/generate" \
    -F "file=@test.jpg"
  ```

### Error: "Reporte no encontrado"
- Verificar que el `report_id` exista en Supabase
- Verificar permisos en Supabase (service key)

### Búsqueda RAG muy lenta
- Verificar que los índices estén creados
- Reducir `match_count`
- Aumentar `match_threshold` para menos resultados

---

## ✅ Checklist Final

Antes de considerar que está completo:

- [ ] Migraciones SQL ejecutadas
- [ ] Backend generando embeddings automáticamente
- [ ] Backend corriendo y accesible
- [ ] Al menos una imagen procesada exitosamente
- [ ] Embedding guardado en Supabase
- [ ] Búsqueda RAG funcionando
- [ ] Frontend integrado con búsqueda RAG
- [ ] Estadísticas mostrando cobertura de embeddings

---

## 🎉 Siguiente Paso Inmediato

**Empieza con la Fase 1:**
1. Abre Supabase SQL Editor
2. Ejecuta las migraciones de `backend/migrations/003_rag_functions.sql`
3. Verifica que no haya errores

**Luego pasa a la Fase 2:**
1. Verifica que el backend esté generando embeddings automáticamente
2. Crea un reporte de prueba
3. Verifica que se generó el embedding

---

## 📞 ¿Necesitas Ayuda?

Si te atascas en algún paso:
1. Revisa los logs del backend
2. Verifica que todas las URLs sean correctas
3. Prueba cada endpoint individualmente
4. Verifica que las variables de entorno estén configuradas

**¡Tú puedes hacerlo!** 🚀



