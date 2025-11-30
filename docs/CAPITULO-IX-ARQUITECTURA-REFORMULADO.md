# Capítulo IX: Arquitectura de la Solución

## Introducción

La arquitectura del sistema PetAlert ha sido diseñada siguiendo principios de modularidad, escalabilidad y eficiencia computacional. La solución integra tecnologías modernas de visión por computadora, geolocalización en tiempo real e infraestructura cloud, permitiendo la identificación inteligente de mascotas perdidas mediante comparación visual automatizada.

El sistema está desplegado en **Google Cloud Platform**, utiliza **Docker** para la contenedorización de servicios, y se apoya en **Supabase** (PostgreSQL) como plataforma de base de datos con extensiones especializadas para operaciones geoespaciales (PostGIS) y búsqueda vectorial (pgvector).

---

## Arquitectura General del Sistema

La arquitectura de PetAlert se estructura en tres capas fundamentales que operan de manera coordinada:

### 1. Capa de Presentación (Frontend)

**Tecnologías:** React Native, Expo, Expo Router

El frontend móvil está desarrollado con **React Native** sobre el framework **Expo**, lo que permite despliegue multiplataforma (iOS y Android) desde una única base de código. La navegación se gestiona mediante **Expo Router**, que implementa un sistema de enrutamiento basado en archivos similar a Next.js.

**Componentes principales:**

- **React Native Paper**: Biblioteca de componentes UI que sigue las guías de Material Design
- **React Native Maps**: Visualización de mapas interactivos con marcadores personalizados para reportes
- **Zustand**: Gestión de estado global ligera y eficiente
- **Expo Location**: Servicios de geolocalización del dispositivo
- **Expo Image Picker**: Captura y selección de imágenes desde la cámara o galería
- **Supabase Client**: SDK para autenticación, base de datos y almacenamiento

**Responsabilidades funcionales:**

1. **Autenticación y gestión de sesión**: Implementa Supabase Auth para registro e inicio de sesión, manteniendo el estado de autenticación de forma persistente con políticas de seguridad RLS (Row Level Security).

2. **Navegación entre pantallas**: Estructura organizada en grupos de rutas:
   - Grupo de autenticación: `(auth)/login.jsx`, `(auth)/register.jsx`
   - Grupo de pestañas principales: `(tabs)/index.jsx` (mapa), `(tabs)/reports.jsx`, `(tabs)/pets.jsx`, `(tabs)/messages.jsx`, `(tabs)/profile.jsx`

3. **Gestión de imágenes y reportes**: Permite capturar o seleccionar imágenes, subirlas a Supabase Storage y enviar metadatos al backend FastAPI para procesamiento mediante IA.

4. **Visualización georreferenciada**: Muestra en tiempo real los reportes de mascotas perdidas/encontradas sobre un mapa interactivo, utilizando marcadores personalizados con información contextual.

5. **Búsqueda asistida por IA**: Interfaz para búsqueda por imagen (`ai-search.jsx`), donde el usuario puede tomar o cargar una foto y recibir coincidencias visuales de reportes similares.

6. **Mensajería en tiempo real**: Integración con Supabase Realtime para comunicación bidireccional entre usuarios interesados en un reporte específico.

---

### 2. Capa de Lógica de Negocio (Backend)

**Tecnologías:** FastAPI, Python 3.11, Docker

El backend está implementado en **Python 3.11** utilizando el framework **FastAPI**, reconocido por su alto rendimiento, validación automática de datos con Pydantic, y documentación interactiva (Swagger/OpenAPI).

**Estructura del backend:**

```
backend/
├── main.py                      # Punto de entrada de la aplicación
├── routers/                     # Endpoints organizados por dominio
│   ├── reports.py              # CRUD de reportes
│   ├── embeddings_supabase.py  # Generación de embeddings
│   ├── ai_search.py            # Búsqueda por imagen
│   ├── matches.py              # Detección de coincidencias
│   ├── pets.py                 # Gestión de mascotas
│   └── rag_search.py           # Búsqueda híbrida (visual + texto)
├── services/
│   └── embeddings.py           # Servicio de IA (MegaDescriptor)
├── utils/
│   └── supabase_client.py      # Cliente optimizado de Supabase
├── migrations/                  # Migraciones SQL
├── Dockerfile                   # Imagen Docker del backend
└── requirements.txt             # Dependencias Python
```

**Funcionalidades principales:**

1. **API RESTful**: Exposición de endpoints documentados automáticamente en `/docs`
2. **Procesamiento de imágenes**: Descarga, normalización y generación de embeddings
3. **Gestión de reportes**: Creación, actualización, búsqueda y cierre de casos
4. **Detección automática de coincidencias**: Comparación vectorial entre reportes perdidos y encontrados
5. **Integración con Supabase**: Almacenamiento de datos, autenticación y storage

**Middleware CORS configurado:**
```python
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,  # Configurable via .env
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

---

### 3. Capa de Datos y Persistencia

**Tecnologías:** Supabase (PostgreSQL 15), PostGIS, pgvector

**Supabase** es una plataforma open-source construida sobre PostgreSQL que provee:

- Base de datos relacional completa
- Autenticación y autorización (Supabase Auth)
- Almacenamiento de archivos (Supabase Storage)
- Realtime subscriptions (Supabase Realtime)
- Edge Functions (opcional)

**Extensiones habilitadas:**

1. **PostGIS**: Extensión espacial de PostgreSQL que permite almacenar y consultar datos geográficos.
   - Columna `location GEOMETRY(POINT, 4326)` en tablas `reports` y `profiles`
   - Índices espaciales GIST para consultas eficientes
   - Funciones geográficas: cálculo de distancias, búsqueda por radio, etc.

2. **pgvector**: Extensión para almacenamiento y búsqueda de vectores de alta dimensión.
   - Columna `embedding VECTOR(1536)` en tabla `reports`
   - Índice HNSW (Hierarchical Navigable Small World) para búsquedas kNN ultrarrápidas
   - Soporte para similitud coseno, distancia euclidiana y producto interno

**Configuración del índice vectorial:**
```sql
CREATE INDEX idx_reports_embedding_hnsw
  ON public.reports 
  USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

Parámetros optimizados:
- `m = 16`: Número de conexiones por nodo (balance velocidad/precisión)
- `ef_construction = 64`: Tamaño de la lista dinámica durante construcción

**Rendimiento observado:**
- Sin índice: ~1-2 segundos para 10,000 reportes
- Con índice HNSW: ~10-50 ms para 10,000 reportes

---

## Servicio de Inteligencia Artificial

### Modelo: MegaDescriptor-L-384

El corazón del sistema de reconocimiento visual es el modelo **MegaDescriptor-L-384** (BVRA/MegaDescriptor-L-384), alojado en Hugging Face Model Hub.

**Características técnicas:**

| Aspecto | Especificación |
|---------|----------------|
| Arquitectura base | Vision Transformer (ViT) + Swin Transformer |
| Especialización | Reconocimiento y re-identificación de animales |
| Resolución de entrada | 384×384 píxeles RGB |
| Dimensiones del embedding | 1536 (float32) |
| Parámetros del modelo | ~300M |
| Framework | PyTorch + timm (Torch Image Models) |
| Normalización | Media=[0.5, 0.5, 0.5], Std=[0.5, 0.5, 0.5] |

**Justificación de la elección:**

1. **Especialización en fauna**: Entrenado con datasets de animales (wildlife re-identification)
2. **Alta capacidad discriminativa**: Captura características sutiles (patrones de pelaje, rasgos faciales, proporciones corporales)
3. **Robustez**: Funciona con diferentes iluminaciones, ángulos y fondos
4. **Open-source**: Disponible públicamente, sin costos de API por inferencia

**Implementación del servicio de embeddings:**

```python
# backend/services/embeddings.py
import torch
import torchvision.transforms as T
import timm

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
MODEL_NAME = "hf-hub:BVRA/MegaDescriptor-L-384"

def _load_model():
    """Carga MegaDescriptor desde Hugging Face Hub"""
    model = timm.create_model(MODEL_NAME, pretrained=True, num_classes=0)
    model = model.to(DEVICE).eval()
    
    transforms = T.Compose([
        T.Resize(size=(384, 384)),
        T.ToTensor(),
        T.Normalize([0.5, 0.5, 0.5], [0.5, 0.5, 0.5])
    ])
    
    return model, transforms

async def image_bytes_to_vec_async(image_bytes: bytes) -> np.ndarray:
    """Genera embedding normalizado L2 de 1536 dimensiones"""
    img = Image.open(io.BytesIO(image_bytes)).convert("RGB")
    
    with torch.inference_mode():
        img_tensor = transforms(img).unsqueeze(0).to(DEVICE)
        feats = model(img_tensor)
        
        # Normalización L2 para usar distancia coseno
        feats = feats / feats.norm(dim=-1, keepdim=True)
        vec = feats.squeeze(0).detach().cpu().numpy().astype("float32")
    
    return vec
```

**Control de concurrencia:**
```python
_inference_semaphore = asyncio.Semaphore(2)  # Máximo 2 inferencias simultáneas
```

**Optimización de memoria:**
- Liberación explícita de tensores después de inferencia
- `torch.cuda.empty_cache()` en GPU
- Pre-carga del modelo al iniciar el servidor (startup event)

---

### Flujo de Procesamiento de Imágenes

1. **Captura/Selección de imagen** → Usuario toma foto o selecciona desde galería
2. **Subida a Supabase Storage** → Frontend sube imagen y obtiene URL pública
3. **Envío al backend** → POST `/reports/` con metadatos + URL de imagen
4. **Descarga y preprocesamiento** → Backend descarga imagen, la convierte a RGB 384×384
5. **Generación de embedding** → MegaDescriptor produce vector de 1536 dimensiones normalizado
6. **Almacenamiento en PostgreSQL** → Vector guardado en columna `embedding VECTOR(1536)`
7. **Búsqueda de coincidencias** → Función RPC `search_similar_reports()` compara con embeddings existentes
8. **Retorno de resultados** → Backend devuelve lista de reportes similares ordenados por score de similitud

---

## Búsqueda por Similitud Vectorial

### Función SQL: search_similar_reports

```sql
CREATE OR REPLACE FUNCTION search_similar_reports(
    query_embedding VECTOR(1536),
    match_threshold FLOAT DEFAULT 0.7,
    match_count INT DEFAULT 10,
    filter_species TEXT DEFAULT NULL,
    filter_type TEXT DEFAULT NULL
)
RETURNS TABLE (
    id UUID,
    similarity_score FLOAT,
    species TEXT,
    type TEXT,
    photos TEXT[],
    description TEXT,
    location JSONB,
    created_at TIMESTAMPTZ
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        r.id,
        1 - (r.embedding <#> query_embedding) AS similarity_score,
        r.species,
        r.type,
        r.photos,
        r.description,
        r.location,
        r.created_at
    FROM public.reports r
    WHERE 
        r.embedding IS NOT NULL
        AND r.status = 'active'
        AND (1 - (r.embedding <#> query_embedding)) >= match_threshold
        AND (filter_species IS NULL OR r.species = filter_species)
        AND (filter_type IS NULL OR r.type = filter_type)
    ORDER BY r.embedding <#> query_embedding
    LIMIT match_count;
END;
$$ LANGUAGE plpgsql;
```

**Operadores de pgvector:**
- `<#>`: Producto interno negativo (para similitud coseno con vectores normalizados)
- `<=>`: Distancia euclidiana (L2)
- `<->`: Distancia Manhattan (L1)

**Interpretación de similitud coseno:**
- 1.0: Imágenes casi idénticas
- 0.9-1.0: Muy alta similitud (misma mascota, ángulo/iluminación diferente)
- 0.8-0.9: Alta similitud (mascota similar, misma raza)
- 0.7-0.8: Similitud moderada (características compartidas)
- <0.7: Baja similitud (descartado por defecto)

---

## Infraestructura Cloud: Google Cloud Platform

### Google Compute Engine

El backend de PetAlert está desplegado en una máquina virtual (VM) de **Google Cloud Compute Engine**, configurada específicamente para cargas de trabajo de machine learning.

**Especificaciones de la VM:**

| Parámetro | Valor |
|-----------|-------|
| Nombre de instancia | petalert-backend |
| Región | us-central1-a |
| Tipo de máquina | e2-medium (2 vCPUs, 4 GB RAM) |
| Sistema operativo | Ubuntu 22.04 LTS |
| Tipo de disco | Balanced persistent disk |
| Tamaño del disco | 50 GB |
| IP externa | Estática (reservada) |
| Etiquetas de red | petalert-backend, http-server |

**Justificación técnica:**

1. **e2-medium**: Serie E2 cost-optimized con balance entre rendimiento y precio. Suficiente para inferencia de MegaDescriptor (300M parámetros) con modelos pre-cargados en memoria.

2. **Ubuntu 22.04 LTS**: Soporte extendido hasta 2027, compatibilidad completa con Docker y dependencias de PyTorch.

3. **50 GB de disco**: Distribución estimada:
   - Sistema operativo: ~8 GB
   - Docker images: ~4 GB
   - Modelo MegaDescriptor (cache): ~2 GB
   - Logs y aplicación: ~5 GB
   - Espacio disponible: ~31 GB

4. **IP estática**: Permite configurar un DNS permanente y evita reconfiguraciones del frontend tras reinicios de la VM.

---

### Configuración de Red y Firewall

**Regla de firewall personalizada:**

```yaml
Nombre: allow-petalert-backend
Tipo: Ingress (tráfico entrante)
Destinos: Instancias con tag "petalert-backend"
Filtros de origen: 0.0.0.0/0 (acceso público)
Protocolo: TCP
Puerto: 8003
Acción: Permitir
Prioridad: 1000
```

**Configuración de red de la VM:**
- Red VPC: default
- Subred: us-central1
- IP interna: 10.128.0.x (asignada automáticamente)
- IP externa: Reservada estáticamente para acceso público
- Tags de red: `petalert-backend`, `http-server`

**Acceso remoto:**
- SSH mediante Google Cloud Console (puerto 22, gestión automática de claves)
- Consola serial disponible para troubleshooting

---

## Containerización con Docker

### Dockerfile del Backend

El backend se ejecuta completamente dentro de un contenedor Docker, garantizando consistencia entre entornos de desarrollo, staging y producción.

```dockerfile
# Imagen base optimizada con Python 3.11
FROM python:3.11-slim

# Instalar dependencias del sistema necesarias para PyTorch y psycopg
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar requirements y instalar dependencias de Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del backend
COPY . .

# Crear directorio para logs
RUN mkdir -p /app/logs

# Exponer puerto 8003 (FastAPI)
EXPOSE 8003

# Variables de entorno para producción
ENV PYTHONUNBUFFERED=1
ENV GENERATE_EMBEDDINGS_LOCALLY=true

# Comando de inicio: Uvicorn con 2 workers
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8003", "--workers", "2"]
```

**Optimizaciones del Dockerfile:**

1. **python:3.11-slim**: Imagen ligera (~150 MB vs ~900 MB de python:3.11 completo)
2. **Instalación en capas**: Separación de dependencias del sistema, requirements y código para aprovechar cache de Docker
3. **--no-cache-dir**: Evita almacenar cache de pip, reduciendo tamaño de la imagen
4. **Limpieza de apt**: `rm -rf /var/lib/apt/lists/*` libera ~40 MB después de instalar paquetes
5. **PYTHONUNBUFFERED=1**: Asegura que los logs de Python se escriban inmediatamente

---

### docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    ports:
      - "8003:8003"
    environment:
      - SUPABASE_URL=${SUPABASE_URL}
      - SUPABASE_SERVICE_KEY=${SUPABASE_SERVICE_KEY}
      - ALLOWED_ORIGINS=${ALLOWED_ORIGINS}
      - GENERATE_EMBEDDINGS_LOCALLY=true
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

**Configuración explicada:**

- **restart: unless-stopped**: Reinicio automático del contenedor tras fallos o reinicios del sistema
- **healthcheck**: Endpoint `/health` verificado cada 30s. Si falla 3 veces consecutivas, el contenedor se marca como unhealthy
- **start_period: 40s**: Tiempo de gracia al inicio (carga del modelo MegaDescriptor tarda ~20-30s)
- **Variables de entorno**: Inyectadas desde archivo `.env` en el host

---

### Comandos de Gestión Docker

**Construcción y despliegue:**
```bash
# Construir imagen
docker-compose build

# Iniciar servicio en background
docker-compose up -d

# Ver logs en tiempo real
docker-compose logs -f backend

# Reiniciar servicio
docker-compose restart backend

# Detener y eliminar contenedor
docker-compose down

# Reconstruir tras cambios en código
docker-compose up -d --build
```

**Monitoreo:**
```bash
# Estado de contenedores
docker-compose ps

# Uso de recursos (CPU, RAM, red, I/O)
docker stats

# Espacio usado por imágenes
docker system df

# Limpieza de recursos no utilizados
docker system prune -a
```

---

## Modelo de Datos

### Diagrama Entidad-Relación

El modelo de datos de PetAlert está diseñado para soportar autenticación, gestión de mascotas, reportes georreferenciados, mensajería bidireccional y búsqueda vectorial.

**Diagrama disponible en:**
https://dbdiagram.io/d/691fa6da228c5bbc1ad31ff8

---

### Descripción de Tablas

#### **auth.users** (Supabase Auth)
Tabla interna gestionada por Supabase Auth para credenciales de autenticación.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | Identificador único del usuario (PK) |
| email | TEXT | Correo electrónico |
| encrypted_password | TEXT | Contraseña hasheada (bcrypt) |
| email_confirmed_at | TIMESTAMPTZ | Confirmación de email |
| created_at | TIMESTAMPTZ | Fecha de registro |

**Relación:** 1:1 con `profiles`

---

#### **profiles**
Información extendida del usuario, visible públicamente según políticas RLS.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | FK → auth.users(id), PK |
| full_name | TEXT | Nombre completo del usuario |
| avatar_url | TEXT | URL de foto de perfil (Supabase Storage) |
| phone | TEXT | Teléfono de contacto |
| location | GEOMETRY(POINT, 4326) | Ubicación geográfica (PostGIS) |
| created_at | TIMESTAMPTZ | Fecha de creación del perfil |
| updated_at | TIMESTAMPTZ | Última actualización |

**Índices:**
- `idx_profiles_location GIST(location)` → Búsquedas geoespaciales

**Políticas RLS:**
- SELECT: Todos los usuarios pueden ver perfiles
- UPDATE: Solo el usuario puede actualizar su propio perfil
- INSERT: Solo al crear el perfil asociado a su auth.users

**Relaciones:**
- 1:N con `pets` (un usuario puede tener múltiples mascotas)
- 1:N con `reports` (un usuario puede crear múltiples reportes)
- 1:N con `conversations` (como participant_1 o participant_2)
- 1:N con `messages` (mensajes enviados)
- 1:N con `push_tokens` (múltiples dispositivos)

---

#### **pets**
Mascotas registradas en el sistema, independientes de los reportes.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | Identificador único (PK) |
| owner_id | UUID | FK → profiles(id) |
| name | TEXT | Nombre de la mascota |
| species | TEXT | dog, cat, bird, rabbit, other |
| breed | TEXT | Raza (opcional) |
| color | TEXT | Color predominante |
| size | TEXT | small, medium, large |
| description | TEXT | Descripción general |
| distinctive_features | TEXT | Marcas, señas particulares |
| photos | TEXT[] | Array de URLs (Supabase Storage) |
| is_lost | BOOLEAN | Indica si actualmente está perdida |
| created_at | TIMESTAMPTZ | Fecha de registro |
| updated_at | TIMESTAMPTZ | Última actualización |

**Índices:**
- `idx_pets_owner ON pets(owner_id)`

**Políticas RLS:**
- SELECT: Todos pueden ver
- INSERT/UPDATE/DELETE: Solo el owner_id = auth.uid()

**Relaciones:**
- N:1 con `profiles` (cada mascota tiene un dueño)
- 1:N con `reports` (una mascota puede tener múltiples reportes históricos)

---

#### **reports**
Núcleo funcional del sistema. Cada reporte representa un caso de mascota perdida o encontrada.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | Identificador único (PK) |
| type | TEXT | 'lost' o 'found' |
| reporter_id | UUID | FK → profiles(id) |
| pet_id | UUID | FK → pets(id), NULL si no está registrada |
| pet_name | TEXT | Nombre de la mascota |
| species | TEXT | dog, cat, bird, rabbit, other |
| breed | TEXT | Raza |
| color | TEXT | Color |
| size | TEXT | small, medium, large |
| description | TEXT | Descripción del caso |
| distinctive_features | TEXT | Señas particulares |
| photos | TEXT[] | Array de URLs de fotos |
| **embedding** | **VECTOR(1536)** | **Vector de MegaDescriptor (IA)** |
| **location** | **GEOMETRY(POINT, 4326)** | **Ubicación geográfica (PostGIS)** |
| address | TEXT | Dirección textual |
| location_details | TEXT | Detalles adicionales del lugar |
| incident_date | DATE | Fecha del incidente |
| status | TEXT | 'active', 'resolved', 'closed' |
| resolved_at | TIMESTAMPTZ | Cuándo se resolvió |
| created_at | TIMESTAMPTZ | Fecha de creación |
| updated_at | TIMESTAMPTZ | Última actualización |

**Índices críticos:**
```sql
-- Geoespacial
CREATE INDEX idx_reports_location ON reports USING GIST (location);

-- Vectorial (HNSW para kNN)
CREATE INDEX idx_reports_embedding_hnsw 
  ON reports USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);

-- Consultas frecuentes
CREATE INDEX idx_reports_type_status ON reports (type, status);
CREATE INDEX idx_reports_species ON reports (species);
CREATE INDEX idx_reports_reporter ON reports (reporter_id);
```

**Políticas RLS:**
- SELECT: Todos pueden ver reportes activos o sus propios reportes
- INSERT: Solo usuarios autenticados pueden crear reportes
- UPDATE: Solo el reporter_id = auth.uid()

**Relaciones:**
- N:1 con `profiles` (reportado por un usuario)
- N:1 con `pets` (puede estar asociado a una mascota registrada)
- 1:N con `conversations` (pueden generarse múltiples conversaciones por reporte)
- 1:N con `matches` (como lost_report_id o found_report_id)

---

#### **matches**
Tabla de coincidencias visuales entre reportes de tipo "lost" y "found", detectadas automáticamente por IA o marcadas manualmente.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | Identificador único (PK) |
| lost_report_id | UUID | FK → reports(id) WHERE type='lost' |
| found_report_id | UUID | FK → reports(id) WHERE type='found' |
| similarity_score | FLOAT | Score de similitud coseno (0.0-1.0) |
| matched_by | TEXT | 'ai', 'manual', 'auto' |
| status | TEXT | 'pending', 'confirmed', 'rejected' |
| created_at | TIMESTAMPTZ | Fecha de detección |
| updated_at | TIMESTAMPTZ | Última actualización |

**Índices:**
```sql
CREATE INDEX idx_matches_lost_report ON matches (lost_report_id);
CREATE INDEX idx_matches_found_report ON matches (found_report_id);
CREATE INDEX idx_matches_similarity ON matches (similarity_score DESC);
```

**Políticas RLS:**
- SELECT: Usuarios involucrados en los reportes (reporter_id de lost o found)
- UPDATE: Usuarios involucrados pueden actualizar status

**Relaciones:**
- N:1 con `reports` (lost_report_id)
- N:1 con `reports` (found_report_id)

---

#### **conversations**
Canal de comunicación bidireccional entre dos usuarios respecto a un reporte específico.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | Identificador único (PK) |
| report_id | UUID | FK → reports(id) |
| participant_1 | UUID | FK → profiles(id) |
| participant_2 | UUID | FK → profiles(id) |
| created_at | TIMESTAMPTZ | Fecha de inicio de conversación |
| updated_at | TIMESTAMPTZ | Última actualización |

**Constraint único:**
```sql
UNIQUE(report_id, participant_1, participant_2)
```

**Índices:**
```sql
CREATE INDEX idx_conversations_report ON conversations (report_id);
CREATE INDEX idx_conversations_participant_1 ON conversations (participant_1);
CREATE INDEX idx_conversations_participant_2 ON conversations (participant_2);
```

**Políticas RLS:**
- SELECT: Solo los participantes pueden ver la conversación
- INSERT: Usuarios autenticados pueden iniciar conversación si son parte de ella

**Relaciones:**
- N:1 con `reports` (conversación asociada a un reporte)
- N:1 con `profiles` (participant_1)
- N:1 con `profiles` (participant_2)
- 1:N con `messages` (múltiples mensajes por conversación)

---

#### **messages**
Mensajes individuales dentro de una conversación.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | Identificador único (PK) |
| conversation_id | UUID | FK → conversations(id) |
| sender_id | UUID | FK → profiles(id) |
| content | TEXT | Contenido del mensaje |
| image_url | TEXT | URL de imagen adjunta (opcional) |
| read_at | TIMESTAMPTZ | Cuándo fue leído (NULL si no leído) |
| created_at | TIMESTAMPTZ | Fecha de envío |

**Índices:**
```sql
CREATE INDEX idx_messages_conversation ON messages (conversation_id);
CREATE INDEX idx_messages_sender ON messages (sender_id);
CREATE INDEX idx_messages_created_at ON messages (created_at DESC);
```

**Políticas RLS:**
- SELECT: Solo participantes de la conversación
- INSERT: Solo sender_id = auth.uid() y participante de la conversación

**Suscripción Realtime:**
```javascript
const subscription = supabase
  .channel(`conversation:${conversationId}`)
  .on('postgres_changes', {
    event: 'INSERT',
    schema: 'public',
    table: 'messages',
    filter: `conversation_id=eq.${conversationId}`
  }, (payload) => {
    // Nuevo mensaje recibido en tiempo real
    addMessageToUI(payload.new);
  })
  .subscribe();
```

**Relaciones:**
- N:1 con `conversations` (cada mensaje pertenece a una conversación)
- N:1 con `profiles` (enviado por un usuario)

---

#### **push_tokens**
Tokens de dispositivos registrados para notificaciones push mediante Expo Notifications.

| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | UUID | Identificador único (PK) |
| user_id | UUID | FK → profiles(id) |
| token | TEXT | Expo Push Token (ej: ExponentPushToken[...]) |
| device_id | TEXT | Identificador del dispositivo |
| platform | TEXT | 'ios', 'android', 'web' |
| created_at | TIMESTAMPTZ | Fecha de registro |
| updated_at | TIMESTAMPTZ | Última actualización |

**Constraint único:**
```sql
UNIQUE(user_id, device_id)
```

**Índices:**
```sql
CREATE INDEX idx_push_tokens_user ON push_tokens (user_id);
CREATE INDEX idx_push_tokens_token ON push_tokens (token);
```

**Políticas RLS:**
- SELECT/INSERT/UPDATE/DELETE: Solo el user_id = auth.uid()

**Relaciones:**
- N:1 con `profiles` (un usuario puede tener múltiples dispositivos)

---

## Flujo de Operación del Sistema

### Caso de Uso: Reportar Mascota Perdida

**1. Autenticación del usuario**
```
Frontend → Supabase Auth: signInWithPassword()
Supabase Auth → Frontend: { user, session }
Zustand Store: Actualiza estado global con sesión
```

**2. Captura de imagen**
```
Usuario: Presiona botón "Reportar mascota perdida"
Frontend: Expo Image Picker → Captura/selecciona foto
Frontend: Comprime imagen a max 1024x1024 (calidad 80%)
```

**3. Subida a Supabase Storage**
```
Frontend → Supabase Storage: upload('reports/uuid-timestamp.jpg', imageBlob)
Supabase Storage → Frontend: { publicURL }
```

**4. Creación del reporte**
```
Frontend → Backend FastAPI: POST /reports/
Body: {
  type: "lost",
  reporter_id: userId,
  pet_name: "Max",
  species: "dog",
  breed: "Golden Retriever",
  photos: ["https://supabase.co/storage/reports/..."],
  location: { lat: -34.6037, lng: -58.3816 },
  description: "Perdido en Parque Centenario..."
}
```

**5. Procesamiento en backend**
```python
# backend/routers/reports.py

@router.post("/reports/")
async def create_report(report: ReportCreate):
    # 1. Insertar reporte en DB (sin embedding aún)
    new_report = supabase.table("reports").insert({
        "type": report.type,
        "reporter_id": report.reporter_id,
        # ... otros campos
    }).execute()
    
    report_id = new_report.data[0]["id"]
    
    # 2. Descargar imagen desde Supabase Storage
    image_url = report.photos[0]
    response = requests.get(image_url)
    image_bytes = response.content
    
    # 3. Generar embedding con MegaDescriptor
    from services.embeddings import image_bytes_to_vec_async
    embedding = await image_bytes_to_vec_async(image_bytes)  # 1536 dims
    
    # 4. Guardar embedding en DB
    supabase.rpc("update_report_embedding", {
        "report_uuid": report_id,
        "embedding_vector": embedding.tolist()
    }).execute()
    
    # 5. Buscar coincidencias automáticas
    matches = supabase.rpc("search_similar_reports", {
        "query_embedding": embedding.tolist(),
        "match_threshold": 0.75,
        "match_count": 10,
        "filter_type": "found"  # Solo reportes de tipo "encontrado"
    }).execute()
    
    # 6. Guardar matches en tabla matches
    for match in matches.data:
        if match["similarity_score"] >= 0.80:
            supabase.table("matches").insert({
                "lost_report_id": report_id,
                "found_report_id": match["id"],
                "similarity_score": match["similarity_score"],
                "matched_by": "ai"
            }).execute()
    
    # 7. Enviar notificaciones push a usuarios con mascotas similares
    if len(matches.data) > 0:
        send_push_notifications(matches.data)
    
    return {"report_id": report_id, "matches_found": len(matches.data)}
```

**6. Visualización en el mapa**
```javascript
// Frontend: app/(tabs)/index.jsx

useEffect(() => {
  // Suscripción en tiempo real a nuevos reportes
  const subscription = supabase
    .channel('public:reports')
    .on('postgres_changes', {
      event: 'INSERT',
      schema: 'public',
      table: 'reports'
    }, (payload) => {
      addMarkerToMap(payload.new);
    })
    .subscribe();
  
  return () => subscription.unsubscribe();
}, []);
```

---

### Caso de Uso: Búsqueda por Imagen

**1. Usuario inicia búsqueda**
```
Usuario: Navega a "Buscar por foto" (ai-search.jsx)
Frontend: Expo Image Picker → Usuario toma foto de mascota encontrada
```

**2. Envío directo al endpoint de IA**
```javascript
// Frontend: ai-search.jsx

const searchByImage = async (imageUri) => {
  const formData = new FormData();
  formData.append('file', {
    uri: imageUri,
    type: 'image/jpeg',
    name: 'search.jpg'
  });
  
  const response = await fetch(`${BACKEND_URL}/embeddings/search_image`, {
    method: 'POST',
    body: formData,
    headers: { 'Content-Type': 'multipart/form-data' }
  });
  
  const matches = await response.json();
  setSearchResults(matches);
};
```

**3. Procesamiento en backend**
```python
# backend/routers/embeddings_supabase.py

@router.post("/embeddings/search_image")
async def search_by_image(file: UploadFile = File(...)):
    # 1. Leer imagen
    image_bytes = await file.read()
    
    # 2. Generar embedding
    embedding = await image_bytes_to_vec_async(image_bytes)
    
    # 3. Buscar en BD (RPC)
    results = supabase.rpc("search_similar_reports", {
        "query_embedding": embedding.tolist(),
        "match_threshold": 0.70,
        "match_count": 20
    }).execute()
    
    # 4. Enriquecer resultados con datos del reporter
    enriched_results = []
    for result in results.data:
        reporter = supabase.table("profiles") \
            .select("full_name, phone, avatar_url") \
            .eq("id", result["reporter_id"]) \
            .single() \
            .execute()
        
        enriched_results.append({
            **result,
            "reporter": reporter.data,
            "distance_km": calculate_distance(user_location, result["location"])
        })
    
    return enriched_results
```

**4. Presentación de resultados**
```javascript
// Frontend: Renderiza lista de coincidencias

<FlatList
  data={searchResults}
  renderItem={({ item }) => (
    <MatchCard
      photo={item.photos[0]}
      species={item.species}
      breed={item.breed}
      similarity={item.similarity_score}
      distance={item.distance_km}
      onPress={() => navigation.navigate('ReportDetail', { id: item.id })}
    />
  )}
/>
```

---

## Seguridad y Optimización

### Row Level Security (RLS)

Todas las tablas tienen políticas RLS habilitadas, asegurando que los usuarios solo puedan acceder a datos autorizados.

**Ejemplo: Políticas de reports**
```sql
-- Solo ver reportes activos o propios
CREATE POLICY "Users can view active or own reports"
  ON reports FOR SELECT
  USING (
    status = 'active' 
    OR auth.uid() = reporter_id
  );

-- Solo crear reportes como usuario autenticado
CREATE POLICY "Users can create reports"
  ON reports FOR INSERT
  WITH CHECK (auth.uid() = reporter_id);

-- Solo actualizar propios reportes
CREATE POLICY "Users can update own reports"
  ON reports FOR UPDATE
  USING (auth.uid() = reporter_id);
```

---

### Optimización de Consultas

**1. Índices compuestos para filtros frecuentes:**
```sql
CREATE INDEX idx_reports_active_species 
  ON reports (status, species) 
  WHERE status = 'active';
```

**2. Índice GIST para búsquedas geoespaciales:**
```sql
-- Búsqueda de reportes en un radio de 5 km
SELECT id, address, ST_Distance(location, ST_SetSRID(ST_MakePoint(-58.3816, -34.6037), 4326)::geography) / 1000 AS distance_km
FROM reports
WHERE ST_DWithin(
  location::geography,
  ST_SetSRID(ST_MakePoint(-58.3816, -34.6037), 4326)::geography,
  5000  -- 5 km en metros
)
ORDER BY distance_km;
```

**3. Índice HNSW para búsqueda vectorial:**
```sql
-- Parámetros optimizados para dataset de ~10K reportes
CREATE INDEX idx_reports_embedding_hnsw
  ON reports USING hnsw (embedding vector_cosine_ops)
  WITH (m = 16, ef_construction = 64);
```

---

### Manejo de Errores y Logging

**Backend:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/app/logs/backend.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

@router.post("/reports/")
async def create_report(report: ReportCreate):
    try:
        # ... lógica de creación
        logger.info(f"Reporte creado: {report_id}")
    except Exception as e:
        logger.error(f"Error creando reporte: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error interno del servidor")
```

**Frontend:**
```javascript
import * as Sentry from '@sentry/react-native';

Sentry.init({
  dsn: 'https://...',
  enableInExpoDevelopment: false,
});

try {
  const response = await apiService.createReport(reportData);
} catch (error) {
  Sentry.captureException(error);
  Alert.alert('Error', 'No se pudo crear el reporte. Intenta nuevamente.');
}
```

---

## Costos de Infraestructura

### Google Cloud Platform

**Configuración actual (e2-medium en us-central1):**

| Recurso | Especificación | Costo Mensual (USD) |
|---------|----------------|---------------------|
| VM e2-medium | 2 vCPU, 4 GB RAM, 730 hrs/mes | $24.27 |
| Disco persistente | 50 GB Balanced | $8.00 |
| IP externa estática | 1 dirección IP | $3.00 |
| Transferencia de datos | ~100 GB egress/mes | $12.00 |
| **TOTAL** | | **$47.27/mes** |

**Optimizaciones de costo:**
- Usar **Committed Use Discounts** (descuento del 37% por compromiso de 1 año): ~$35/mes
- Implementar **autoscaling** con apagado automático en horarios de bajo uso (no recomendado para producción 24/7)
- Migrar a **Cloud Run** (serverless) para pago por uso real (viable para tráfico bajo)

---

### Supabase

**Plan Free Tier:**
- Base de datos: 500 MB (suficiente para ~50K reportes con embeddings)
- Storage: 1 GB (suficiente para ~200-500 imágenes comprimidas)
- Egress: 2 GB/mes
- Realtime: Hasta 200 conexiones concurrentes

**Cuándo migrar a Plan Pro ($25/mes):**
- Superar 500 MB de base de datos (~50K reportes)
- Necesitar backups automáticos (Point-In-Time Recovery)
- Requerir más de 5 GB de storage
- Superar 2 GB de egress mensual

---

### Estimación Total

**Costos mensuales estimados:**

| Servicio | Plan | Costo |
|----------|------|-------|
| Google Compute Engine | e2-medium (730 hrs) | $47.27 |
| Supabase | Free Tier | $0.00 |
| Expo | Free | $0.00 |
| **TOTAL** | | **$47.27/mes** |

**Costos adicionales opcionales:**
- Dominio personalizado: ~$12/año
- Certificado SSL: $0 (Let's Encrypt gratuito)
- Monitoreo (Cloud Monitoring): Incluido en free tier de GCP
- Sentry (error tracking): Free tier (5K events/mes)

---

## Monitoreo y Observabilidad

### Google Cloud Monitoring

**Métricas monitoreadas:**
- CPU utilization
- Memory usage
- Disk I/O
- Network traffic
- HTTP response times

**Alertas configuradas:**
```yaml
Alerta: High CPU Usage
Condición: CPU > 80% por más de 5 minutos
Notificación: Email + SMS

Alerta: Backend Down
Condición: Healthcheck fails 3 veces consecutivas
Notificación: Email + Slack
```

---

### Cloud Logging

**Logs centralizados:**
```bash
# Ver logs en tiempo real desde Google Cloud Console
gcloud logging tail --project=petalert

# Filtrar errores
gcloud logging read "severity>=ERROR" --limit 50

# Exportar logs a BigQuery para análisis
gcloud logging sinks create bigquery-sink \
  bigquery.googleapis.com/projects/petalert/datasets/logs
```

---

### Healthcheck Endpoint

```python
# backend/main.py

@app.get("/health")
async def health_check():
    """Endpoint de salud para Docker healthcheck y monitoreo externo"""
    try:
        # Verificar conexión a Supabase
        supabase.table("profiles").select("id").limit(1).execute()
        
        # Verificar modelo de IA cargado
        from services.embeddings import _model
        model_loaded = _model is not None
        
        return {
            "status": "healthy",
            "timestamp": datetime.utcnow().isoformat(),
            "supabase": "connected",
            "ai_model": "loaded" if model_loaded else "not_loaded",
            "version": "1.5.0"
        }
    except Exception as e:
        logger.error(f"Healthcheck failed: {e}")
        raise HTTPException(status_code=503, detail="Service unavailable")
```

---

## Conclusión

La arquitectura de PetAlert representa una solución moderna, escalable y eficiente para el problema de las mascotas perdidas. La integración de **Google Cloud Compute Engine** para infraestructura confiable, **Docker** para portabilidad y consistencia, **Supabase** como plataforma de base de datos robusta, y **MegaDescriptor** como modelo de IA especializado, ha permitido construir un sistema capaz de:

1. **Procesar imágenes de mascotas en tiempo real** (~2-3 segundos por reporte completo)
2. **Buscar entre miles de reportes en milisegundos** (gracias a pgvector + HNSW)
3. **Escalar horizontalmente** (agregar más workers de Uvicorn o múltiples VMs con load balancer)
4. **Mantener costos bajos** (~$47/mes para infraestructura inicial)
5. **Proveer experiencia móvil nativa** en iOS y Android desde un único codebase

El diseño modular permite futuras mejoras sin refactorizaciones mayores:
- Integración de notificaciones push avanzadas
- Sistema de recompensas y gamificación
- Expansión del modelo de IA con fine-tuning en dataset propio
- Migración a arquitectura de microservicios si el tráfico lo justifica

---

## Referencias Técnicas

- **MegaDescriptor Paper:** BVRA. "Animal Re-identification with Deep Learning". Hugging Face Model Hub.
- **pgvector Documentation:** https://github.com/pgvector/pgvector
- **PostGIS Documentation:** https://postgis.net/docs/
- **FastAPI Documentation:** https://fastapi.tiangolo.com/
- **React Native Documentation:** https://reactnative.dev/
- **Supabase Documentation:** https://supabase.com/docs
- **Google Cloud Compute Engine:** https://cloud.google.com/compute/docs
- **Docker Documentation:** https://docs.docker.com/


