# 🔍 ¿Para qué se ocupa Google Vision en el flujo?

## Respuesta Corta

**Google Vision NO busca coincidencias**. Se usa para **extraer información descriptiva** de la imagen (etiquetas, colores, especie) que se guarda en el reporte para enriquecer los datos.

## ¿Qué hace Google Vision?

Google Vision analiza la imagen y extrae **información textual/descriptiva**:

### 1. **Labels (Etiquetas)**
Detecta qué objetos hay en la imagen:
```json
{
  "labels": [
    {"label": "Dog", "score": 0.98},
    {"label": "Pet", "score": 0.95},
    {"label": "Golden Retriever", "score": 0.87},
    {"label": "Mammal", "score": 0.82},
    {"label": "Carnivore", "score": 0.75}
  ]
}
```

### 2. **Colores Dominantes**
Extrae los 3 colores principales de la imagen:
```json
{
  "colors": ["#FFD700", "#8B4513", "#FFFFFF"]
}
```

### 3. **Detección de Especie**
Identifica automáticamente la especie:
- "dog" → perro
- "cat" → gato
- "bird" → pájaro
- "rabbit" → conejo

## ¿Dónde se usa en el flujo?

### En n8n:

```
1. n8n recibe la imagen
   ↓
2. Google Vision analiza la imagen
   ↓
   Extrae:
   - Labels: ["Dog", "Pet", "Golden Retriever"]
   - Colores: ["#FFD700", "#8B4513"]
   - Especie: "dog"
   ↓
3. n8n envía estos datos al backend
   ↓
4. Backend guarda en el reporte:
   - labels: {...}
   - colors: [...]
   - species: "dog" (si no estaba definida)
```

## ¿Qué NO hace Google Vision?

❌ **NO busca coincidencias** - Eso lo hace el embedding con pgvector
❌ **NO compara imágenes** - Solo analiza una imagen individual
❌ **NO determina similitud** - Solo describe lo que ve

## Comparación: Google Vision vs Embedding

| Aspecto | Google Vision | Embedding (OpenCLIP) |
|---------|---------------|----------------------|
| **¿Qué hace?** | Describe la imagen con texto | Convierte imagen a vector numérico |
| **Output** | Labels, colores, especie | Vector de 512 números |
| **¿Para qué se usa?** | Enriquecer datos del reporte | Buscar coincidencias visuales |
| **¿Busca matches?** | ❌ NO | ✅ SÍ |
| **Ejemplo** | "Es un perro dorado" | `[0.123, 0.456, -0.789, ...]` |

## Flujo Completo en n8n

```
┌─────────────────────────────────────────┐
│  n8n recibe webhook con imagen          │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Google Vision API                      │
│  Analiza la imagen                      │
│  ↓                                      │
│  Retorna:                               │
│  - Labels: ["Dog", "Pet", ...]          │
│  - Colores: ["#FFD700", ...]            │
│  - Especie: "dog"                       │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  Si hay embedding, busca coincidencias  │
│  (Esto NO lo hace Google Vision)        │
│  ↓                                      │
│  Llama a Supabase RPC                   │
│  search_similar_reports()               │
└──────────────┬──────────────────────────┘
               │
               ▼
┌─────────────────────────────────────────┐
│  n8n retorna al backend:                │
│  {                                      │
│    "analysis": {                        │
│      "labels": [...],    ← De Google Vision
│      "colors": [...],    ← De Google Vision
│      "species": "dog"    ← De Google Vision
│    },                                   │
│    "matches": [...]      ← De embedding/pgvector
│  }                                      │
└─────────────────────────────────────────┘
```

## ¿Por qué se usa Google Vision entonces?

### 1. **Enriquecer el Reporte**
Guarda información descriptiva que puede ser útil:
- Labels para búsquedas por texto
- Colores para filtros visuales
- Especie automática si el usuario no la especificó

### 2. **Mejorar la Experiencia del Usuario**
- Muestra descripciones automáticas
- Sugiere información faltante
- Ayuda a categorizar reportes

### 3. **Futuros Usos**
- Búsqueda por texto (buscar "perro dorado")
- Filtros avanzados (filtrar por colores)
- Estadísticas (cuántos perros vs gatos se reportan)

## ¿Se puede prescindir de Google Vision?

**Técnicamente SÍ**, pero perderías:

- ❌ Auto-detección de especie
- ❌ Labels descriptivos
- ❌ Colores dominantes
- ❌ Enriquecimiento de datos

**La búsqueda de coincidencias funcionaría igual** porque usa embeddings, no Google Vision.

## Resumen

**Google Vision = Metadata/Descripción**
- Qué hay en la imagen
- Qué colores tiene
- Qué especie es

**Embedding = Búsqueda Visual**
- Compara imágenes directamente
- Encuentra coincidencias visuales
- Es lo que realmente busca matches

**Son complementarios:**
- Google Vision enriquece los datos
- Embedding busca las coincidencias









