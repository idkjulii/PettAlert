# 🔗 Relación entre Google Vision y Embeddings en PetAlert

Este documento explica cómo se relacionan y complementan **Google Vision API** y **OpenCLIP Embeddings** en el sistema de búsqueda de mascotas.

## 📊 Resumen Ejecutivo

**Google Vision** y **Embeddings (OpenCLIP)** son dos tecnologías **complementarias** que se usan para diferentes propósitos en el sistema de búsqueda:

| Aspecto | Google Vision | OpenCLIP Embeddings |
|---------|--------------|---------------------|
| **Propósito** | Análisis semántico | Búsqueda por similitud visual |
| **Output** | Etiquetas, colores, especies | Vector de 512 números |
| **Método** | Descripción textual | Representación vectorial completa |
| **Uso Principal** | `/ai-search/` | `/embeddings/search_image` |
| **Almacenamiento** | Columna `labels` (JSONB) | Columna `embedding` (vector(512)) |

## 🔍 ¿Qué hace cada uno?

### Google Vision API

**Función:** Analiza la imagen y extrae información semántica (textual).

**Output:**
```json
{
  "labels": [
    {"label": "Dog", "score": 0.98},
    {"label": "Pet", "score": 0.95},
    {"label": "Golden Retriever", "score": 0.87}
  ],
  "colors": ["#FFD700", "#8B4513", "#FFFFFF"],
  "species": "dog"
}
```

**Se guarda en:** `reports.labels` (JSONB en Supabase)

**Uso:** 
- Detección de especie
- Extracción de características (raza, tamaño, etc.)
- Análisis de colores
- Filtrado inicial de candidatos

---

### OpenCLIP Embeddings

**Función:** Convierte la imagen en un vector numérico que captura la similitud visual completa.

**Output:**
```python
# Vector de 512 dimensiones
[0.123, 0.456, -0.789, ..., 0.234]  # 512 números
```

**Se guarda en:** `reports.embedding` (vector(512) en Supabase con pgvector)

**Uso:**
- Búsqueda por similitud visual directa
- Encuentra imágenes "visualmente similares" sin depender de etiquetas
- Más preciso para encontrar la misma mascota

---

## 🔄 Flujo Completo del Sistema

### Cuando se crea un reporte:

```
┌─────────────────────────────────────────────────────┐
│ 1. Usuario crea reporte con foto                   │
│    📸 Foto de la mascota                           │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ 2. Backend procesa la imagen con Google Vision     │
│    - Detecta labels: "dog", "pet", "golden"        │
│    - Detecta colores: ["#FFD700", "#8B4513"]       │
│    - Determina especie: "dog"                      │
│    📝 Se guarda en: reports.labels (JSONB)         │
└────────────┬────────────────────────────────────────┘
             │
             ▼
┌─────────────────────────────────────────────────────┐
│ 3b. Backend → OpenCLIP (EMBEDDING)                 │
│     - Genera vector[512]                           │
│     - Captura similitud visual completa            │
│     📊 Se guarda en: reports.embedding (vector)    │
└─────────────────────────────────────────────────────┘
```

**Resultado:** Cada reporte tiene:
- ✅ `labels`: Análisis semántico de Google Vision
- ✅ `embedding`: Vector de similitud visual de OpenCLIP

---

## 🔎 Dos Sistemas de Búsqueda Diferentes

### 1. Búsqueda con Google Vision (`/ai-search/`)

**Cómo funciona:**
```
Usuario sube foto
    ↓
Google Vision analiza la foto
    ↓
Extrae labels y colores
    ↓
Compara labels con labels almacenados en BD
    ↓
Calcula similitud basada en intersección de labels
    ↓
Retorna resultados ordenados por similitud de labels
```

**Código:**
```python
# backend/routers/ai_search.py

# 1. Analizar imagen con Google Vision
vision_client.label_detection(image=image)
# → Obtiene: ["dog", "pet", "golden retriever"]

# 2. Buscar candidatos en BD que tengan labels similares
query = sb.table("reports").select("*")
candidates = query.execute().data

# 3. Calcular similitud comparando labels
visual_score = calculate_visual_similarity(
    {"labels": labels},        # Labels de la foto de búsqueda
    candidate.get("labels", {}) # Labels del candidato en BD
)
# → Similitud basada en etiquetas comunes
```

**Ventajas:**
- ✅ Filtrado rápido por especie/raza
- ✅ Interpretable (sabes por qué hay match: "ambos son perros dorados")
- ✅ No requiere embeddings pre-generados

**Limitaciones:**
- ⚠️ Depende de la calidad de las etiquetas detectadas
- ⚠️ No captura similitud visual directa
- ⚠️ Puede perder matches si las etiquetas no coinciden exactamente

---

### 2. Búsqueda con Embeddings (`/embeddings/search_image`)

**Cómo funciona:**
```
Usuario sube foto
    ↓
OpenCLIP genera embedding[512] de la foto
    ↓
Busca en BD usando similitud coseno (pgvector)
    ↓
Compara vector de búsqueda con vectores almacenados
    ↓
Retorna resultados ordenados por similitud vectorial
```

**Código:**
```python
# backend/routers/embeddings.py

# 1. Generar embedding de la imagen de búsqueda
qvec = image_bytes_to_vec(await file.read())
# → Vector[512]: [0.123, 0.456, -0.789, ...]

# 2. Buscar por similitud usando pgvector
sql = """
    SELECT r.id, (1 - (r.embedding <#> %(qvec)s)) as score_clip
    FROM reports r
    WHERE r.embedding IS NOT NULL
    ORDER BY r.embedding <#> %(qvec)s
    LIMIT 10
"""
# → Similitud coseno directa entre vectores
```

**Ventajas:**
- ✅ Similitud visual precisa (encuentra la misma mascota incluso si las etiquetas difieren)
- ✅ Rápido con índices pgvector
- ✅ No depende de etiquetas textuales

**Limitaciones:**
- ⚠️ Requiere que todos los reportes tengan embedding generado
- ⚠️ Menos interpretable (no sabes por qué hay match)

---

## 🤝 ¿Cómo se Complementan?

### Escenario 1: Búsqueda Híbrida (Ideal)

```python
# 1. Filtrar candidatos usando Google Vision labels
candidates = filter_by_species(labels)  # Solo perros
candidates = filter_by_breed(labels)    # Solo golden retrievers

# 2. Ordenar por similitud de embeddings
results = sort_by_embedding_similarity(candidates)

# 3. Combinar scores
final_score = (
    label_similarity * 0.3 +    # 30% Google Vision
    embedding_similarity * 0.7   # 70% Embeddings
)
```

**Beneficio:** Combina lo mejor de ambos mundos:
- Filtrado inteligente (Google Vision)
- Similitud visual precisa (Embeddings)

### Escenario 2: Uso Independiente

**Cuando usar Google Vision:**
- Búsqueda inicial rápida
- Filtrado por especie/raza
- Análisis de características semánticas

**Cuando usar Embeddings:**
- Búsqueda precisa por similitud visual
- Encontrar la misma mascota con alta confianza
- Cuando las etiquetas no son suficientes

---

## 📊 Almacenamiento en la Base de Datos

### Tabla `reports` en Supabase:

```sql
CREATE TABLE reports (
    id UUID PRIMARY KEY,
    -- ... otros campos ...
    
    -- Google Vision: Análisis semántico
    labels JSONB,          -- {"tags": ["dog", "pet"], "colors": [...]}
    colors TEXT[],         -- ["#FFD700", "#8B4513"]
    species TEXT,          -- "dog"
    
    -- OpenCLIP: Embedding vectorial
    embedding vector(512),  -- [0.123, 0.456, -0.789, ...]
    
    -- ... otros campos ...
);
```

**Cuando se guarda cada uno:**

| Campo | Cuándo se genera | Dónde se genera |
|-------|-----------------|-----------------|
| `labels` | Al crear reporte | Backend con Google Vision |
| `colors` | Al crear reporte | Backend con Google Vision |
| `species` | Al crear reporte | Backend con Google Vision |
| `embedding` | Al indexar reporte (opcional) | Backend con OpenCLIP |

---

## 🔄 Flujo Actual en el Proyecto

### Estado Actual:

1. **Google Vision** (en backend):
   - ✅ Implementado en el backend
   - ✅ Genera labels, colores, especie
   - ✅ Se guarda en `reports.labels`

2. **OpenCLIP Embeddings** (en backend):
   - ✅ Ya está implementado
   - ✅ Genera embeddings vectoriales
   - ✅ Se guarda en `reports.embedding`
   - ⚠️ Requiere indexación manual o automática

### Endpoints Disponibles:

```python
# 1. Búsqueda con Google Vision
POST /ai-search/
# → Usa labels para búsqueda y scoring

# 2. Búsqueda con Embeddings
POST /embeddings/search_image
# → Usa embeddings para similitud visual

# 3. Generar embedding para un reporte
POST /embeddings/index/{report_id}
# → Genera y guarda embedding de una imagen
```

---

## 🎯 Recomendaciones

### Para Mejorar la Búsqueda:

1. **Generar embeddings automáticamente:**
   - Configurar el backend para generar embeddings automáticamente al crear reportes

2. **Búsqueda híbrida:**
   - Combinar ambos métodos en un solo endpoint
   - Usar Google Vision para filtrado inicial
   - Usar Embeddings para ranking final

3. **Priorizar embeddings:**
   - Los embeddings capturan similitud visual más precisa
   - Google Vision es útil para filtrado y metadata
   - Ideal: Google Vision para metadata + Embeddings para búsqueda

---

## 📝 Ejemplo de Uso Combinado

```python
# Pseudocódigo de búsqueda híbrida ideal

async def hybrid_search(image_file, user_location):
    # 1. Google Vision: Análisis rápido
    labels, colors, species = analyze_with_google_vision(image_file)
    
    # 2. Filtrar candidatos iniciales
    candidates = filter_by_species_and_location(species, user_location)
    
    # 3. Generar embedding de búsqueda
    query_embedding = generate_embedding(image_file)
    
    # 4. Ordenar por similitud de embeddings
    results = rank_by_embedding_similarity(candidates, query_embedding)
    
    # 5. Combinar scores
    for result in results:
        result.final_score = (
            label_similarity(result.labels, labels) * 0.3 +
            embedding_similarity(result.embedding, query_embedding) * 0.7
        )
    
    return sorted(results, key=lambda x: x.final_score, reverse=True)
```

---

## 🎉 Conclusión

**Google Vision** y **Embeddings** son tecnologías **complementarias**:

- **Google Vision** = "¿Qué es?" (análisis semántico)
- **Embeddings** = "¿Se parece?" (similitud visual)

**Juntos** proporcionan un sistema de búsqueda robusto que combina:
- ✅ Filtrado inteligente (Google Vision)
- ✅ Similitud visual precisa (Embeddings)
- ✅ Metadata rica para mejorar resultados
- ✅ Búsqueda rápida y escalable


