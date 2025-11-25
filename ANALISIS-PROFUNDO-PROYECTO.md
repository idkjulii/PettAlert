# 📊 Análisis Profundo del Proyecto PetAlert

**Fecha de análisis**: 2025-01-27  
**Versión del proyecto**: 1.5.0  
**Estado**: Activo en desarrollo

---

## 🎯 Resumen Ejecutivo

**PetAlert** es una aplicación móvil multiplataforma (iOS/Android) desarrollada con React Native y Expo, diseñada para ayudar a encontrar mascotas perdidas mediante un sistema inteligente de reportes, búsqueda por similitud visual con IA, y comunicación entre usuarios.

### Propósito Principal
Facilitar la recuperación de mascotas perdidas mediante:
- Reportes geolocalizados de mascotas perdidas/encontradas
- Búsqueda inteligente por similitud visual usando embeddings CLIP
- Sistema de matching automático entre reportes
- Mensajería en tiempo real entre usuarios
- Gestión completa de salud veterinaria de mascotas

---

## 🏗️ Arquitectura del Sistema

### Stack Tecnológico

#### Frontend (Móvil)
- **Framework**: React Native 0.81.5 con Expo 54.0.19
- **Navegación**: Expo Router 6.0.13 (file-based routing)
- **Estado Global**: Zustand 4.4.0
- **UI Components**: React Native Paper 5.12.0
- **Mapas**: React Native Maps 1.20.1
- **Base de Datos**: Supabase JS Client 2.39.0
- **Autenticación**: Supabase Auth con Expo Secure Store
- **Notificaciones**: Expo Notifications
- **Ubicación**: Expo Location
- **Imágenes**: Expo Image Picker, Expo Image Manipulator

#### Backend (API)
- **Framework**: FastAPI 0.110+
- **Servidor**: Uvicorn 0.30+
- **Base de Datos**: Supabase (PostgreSQL con PostGIS)
- **IA/ML**: 
  - PyTorch 2.0.0+ con TorchVision
  - MegaDescriptor-L-384 (modelo de embeddings visuales)
  - Hugging Face Hub
- **Procesamiento de Imágenes**: Pillow, NumPy
- **Cliente HTTP**: httpx, requests

#### Base de Datos
- **Motor**: PostgreSQL (Supabase)
- **Extensiones**:
  - PostGIS (geolocalización)
  - pgvector (búsqueda vectorial)
  - uuid-ossp (generación de UUIDs)
- **Almacenamiento**: Supabase Storage (fotos de mascotas)

#### Infraestructura
- **Contenedorización**: Docker (Dockerfile en backend)
- **Orquestación**: Docker Compose
- **CI/CD**: Scripts de deployment (deploy-vm.sh, setup-vm.sh)
- **Monitoreo**: Health checks integrados

---

## 📁 Estructura del Proyecto

### Organización de Directorios

```
petFindnoborres/
├── app/                          # Expo Router (páginas)
│   ├── (auth)/                  # Autenticación
│   │   ├── login.jsx
│   │   └── register.jsx
│   ├── (tabs)/                  # Navegación por pestañas
│   │   ├── index.jsx           # Mapa principal
│   │   ├── reports.jsx         # Mis reportes
│   │   ├── pets.jsx            # Mis mascotas
│   │   ├── messages.jsx        # Mensajes
│   │   └── profile.jsx         # Perfil
│   ├── ai-search.jsx           # Búsqueda por IA
│   ├── messages/               # Conversaciones
│   ├── pets/                   # Gestión de mascotas
│   └── report/                 # Crear reportes
│
├── src/                         # Código fuente organizado
│   ├── components/             # Componentes reutilizables
│   │   ├── Map/               # Componentes de mapa
│   │   └── UI/                # Componentes de UI
│   ├── services/              # Servicios de API
│   │   ├── supabase.js       # Cliente Supabase
│   │   ├── api.js            # Cliente backend
│   │   ├── location.js       # Servicios de ubicación
│   │   ├── aiSearch.js       # Búsqueda IA
│   │   └── searchImage.js    # Búsqueda por imagen
│   ├── stores/               # Estado global (Zustand)
│   │   ├── authStore.js
│   │   └── matchStore.js
│   ├── hooks/                # Hooks personalizados
│   ├── config/               # Configuración
│   └── utils/                # Utilidades
│
├── backend/                    # API FastAPI
│   ├── routers/               # Endpoints de API
│   │   ├── reports.py        # CRUD de reportes
│   │   ├── matches.py        # Sistema de matches
│   │   ├── ai_search.py      # Búsqueda con IA
│   │   ├── embeddings.py     # Generación de embeddings
│   │   ├── embeddings_supabase.py
│   │   ├── rag_search.py     # Búsqueda semántica
│   │   ├── pets.py           # Gestión de mascotas
│   │   └── direct_matches.py
│   ├── services/             # Lógica de negocio
│   │   └── embeddings.py    # Servicio de embeddings
│   ├── migrations/           # Migraciones SQL
│   │   ├── 001_add_embeddings.sql
│   │   ├── 007_pet_health_tracking.sql
│   │   └── 008_add_missing_pets_columns.sql
│   ├── utils/               # Utilidades
│   └── scripts/             # Scripts de mantenimiento
│
├── components/                 # Componentes de Expo
├── assets/                    # Recursos estáticos
├── tests/                     # Pruebas
├── specs/                     # Especificaciones de features
└── .specify/                  # Documentación de proyecto
    └── memory/
        ├── constitution.md   # Principios de desarrollo
        └── features-catalog.md
```

---

## 🗄️ Modelo de Datos

### Tablas Principales

#### 1. **profiles** (Perfiles de Usuario)
- `id` (UUID, FK a auth.users)
- `full_name`, `avatar_url`, `phone`
- `location` (GEOMETRY POINT)
- `created_at`, `updated_at`

#### 2. **pets** (Mascotas Registradas)
- `id` (UUID)
- `owner_id` (FK a profiles)
- `name`, `species`, `breed`, `color`, `size`
- `description`, `distinctive_features`
- `photos` (TEXT[])
- `is_lost` (BOOLEAN)
- `created_at`, `updated_at`

#### 3. **reports** (Reportes de Mascotas)
- `id` (UUID)
- `type` (lost/found)
- `reporter_id` (FK a profiles)
- `pet_id` (FK a pets, nullable)
- `pet_name`, `species`, `breed`, `color`, `size`
- `description`, `distinctive_features`
- `photos` (TEXT[])
- `location` (GEOMETRY POINT)
- `address`, `location_details`
- `incident_date` (DATE)
- `status` (active/resolved/closed)
- `embedding` (vector(512)) - **Para búsqueda visual**
- `labels` (JSONB) - **Etiquetas de Google Vision**
- `resolved_at`, `created_at`, `updated_at`

#### 4. **matches** (Coincidencias entre Reportes)
- `id` (UUID)
- `report_lost_id` (FK a reports)
- `report_found_id` (FK a reports)
- `similarity_score` (FLOAT)
- `distance_km` (FLOAT)
- `confidence` (high/medium/low)
- `status` (pending/confirmed/rejected)
- `created_at`, `updated_at`

#### 5. **conversations** (Conversaciones)
- `id` (UUID)
- `report_id` (FK a reports)
- `participant_1`, `participant_2` (FK a profiles)
- `created_at`, `updated_at`

#### 6. **messages** (Mensajes)
- `id` (UUID)
- `conversation_id` (FK a conversations)
- `sender_id` (FK a profiles)
- `content` (TEXT)
- `image_url` (TEXT, nullable)
- `read_at` (TIMESTAMP)
- `created_at`

#### 7. **Historial de Salud** (Módulo Veterinario)
- `historial_salud` - Eventos médicos
- `vacunacion_tratamiento` - Vacunas y tratamientos
- `medicamentos_activos` - Medicamentos actuales
- `indicador_bienestar` - Métricas de salud
- `recordatorio` - Recordatorios de cuidado
- `documento_medico` - Documentos médicos
- `plan_cuidado` - Planes de cuidado personalizados

---

## 🔄 Flujos Principales del Sistema

### 1. Flujo de Creación de Reporte

```
Usuario → Frontend
  ↓
1. Selecciona tipo (perdida/encontrada)
2. Completa formulario (especie, raza, color, etc.)
3. Sube fotos (máx. 5)
4. Selecciona ubicación (GPS o mapa)
  ↓
Frontend → Backend API
  ↓
POST /reports/
  ↓
Backend:
  1. Valida datos
  2. Guarda reporte en Supabase
  3. Sube fotos a Supabase Storage
  4. Genera embedding CLIP (MegaDescriptor) en background
  5. Guarda embedding en columna vector(512)
  6. Busca matches automáticamente
  7. Retorna reporte creado
  ↓
Frontend muestra confirmación
```

### 2. Flujo de Búsqueda por Similitud Visual

```
Usuario → Frontend
  ↓
1. Selecciona imagen desde galería/cámara
2. Configura tipo de búsqueda (lost/found/both)
3. Configura radio (5/10/25/50 km)
  ↓
Frontend → Backend API
  ↓
POST /embeddings-supabase/search_image
  ↓
Backend:
  1. Genera embedding de imagen de búsqueda
  2. Ejecuta búsqueda vectorial en Supabase:
     - Filtra por tipo opuesto
     - Filtra por radio geográfico
     - Calcula similitud coseno
     - Ordena por score
  3. Retorna top N resultados con scores
  ↓
Frontend muestra resultados ordenados
```

### 3. Flujo de Matching Automático

```
Nuevo reporte creado con embedding
  ↓
Backend ejecuta find_and_save_matches()
  ↓
1. Obtiene embedding del reporte
2. Busca reportes del tipo opuesto:
   - Con embedding válido
   - Status = 'active'
   - Misma especie (opcional)
3. Calcula similitud coseno para cada candidato
4. Filtra por threshold (default: 0.1)
5. Calcula distancia geográfica
6. Guarda matches en tabla 'matches':
   - report_lost_id / report_found_id
   - similarity_score
   - distance_km
   - confidence (high/medium/low)
   - status = 'pending'
  ↓
Usuario puede ver matches en "Mis Reportes"
```

### 4. Flujo de Mensajería

```
Usuario A ve reporte de Usuario B
  ↓
Usuario A toca "Contactar"
  ↓
Frontend:
  1. Obtiene o crea conversación
  2. Navega a pantalla de chat
  ↓
Usuario A envía mensaje
  ↓
Frontend → Supabase
  ↓
INSERT en tabla 'messages'
  ↓
Supabase Realtime notifica a Usuario B
  ↓
Usuario B recibe notificación push
```

---

## 🤖 Sistema de Inteligencia Artificial

### Modelo de Embeddings Visuales

**MegaDescriptor-L-384** (Hugging Face)
- **Dimensión**: Variable (detectada automáticamente, ~512-1024)
- **Input**: Imágenes RGB 384x384
- **Output**: Vector normalizado L2
- **Uso**: Búsqueda por similitud visual entre fotos de mascotas

### Procesamiento de Embeddings

1. **Generación**:
   - Imagen → Preprocesamiento (resize 384x384, normalización)
   - Modelo → Forward pass
   - Output → Normalización L2
   - Vector → Guardado en `reports.embedding` (pgvector)

2. **Búsqueda**:
   - Query embedding → Búsqueda vectorial en Supabase
   - Función RPC: `search_similar_reports`
   - Índice IVF (Inverted File Index) para kNN rápido
   - Filtrado por tipo, especie, ubicación

3. **Optimizaciones**:
   - Pre-carga del modelo al iniciar servidor
   - Semáforo de concurrencia (máx. 2 inferencias simultáneas)
   - Generación asíncrona en background tasks
   - Cache de embeddings (no se regeneran si ya existen)

### Análisis de Imágenes (Google Vision API)

- **Etiquetas**: Detección de objetos, animales, características
- **Colores**: Colores dominantes en imagen
- **Almacenamiento**: JSONB en columna `reports.labels`

---

## 🔐 Seguridad y Autenticación

### Autenticación
- **Proveedor**: Supabase Auth
- **Métodos**: Email/Password
- **Almacenamiento de tokens**: Expo Secure Store
- **Refresh automático**: Habilitado

### Row Level Security (RLS)
- Políticas en todas las tablas principales
- Usuarios solo pueden:
  - Ver todos los reportes públicos
  - Editar/eliminar sus propios reportes
  - Gestionar sus propias mascotas
  - Leer sus propias conversaciones

### Permisos de Aplicación
- **Ubicación**: Cuando está en uso
- **Cámara**: Para tomar fotos
- **Galería**: Para seleccionar imágenes
- **Notificaciones**: Push notifications

---

## 📊 Características Principales

### 1. Reportes de Mascotas
- ✅ Crear reportes de mascotas perdidas/encontradas
- ✅ Subir múltiples fotos (hasta 5)
- ✅ Geolocalización precisa
- ✅ Búsqueda y edición de reportes propios
- ✅ Resolución de reportes

### 2. Búsqueda Inteligente
- ✅ Búsqueda por similitud visual (CLIP embeddings)
- ✅ Búsqueda por análisis de IA (Google Vision)
- ✅ Filtrado geográfico (radio configurable)
- ✅ Scoring combinado (visual + ubicación + metadatos)

### 3. Sistema de Matches
- ✅ Detección automática de coincidencias
- ✅ Visualización de matches con scores
- ✅ Confirmación/rechazo de matches
- ✅ Notificaciones de nuevos matches

### 4. Mensajería
- ✅ Conversaciones entre usuarios
- ✅ Mensajes de texto e imágenes
- ✅ Actualización en tiempo real (Supabase Realtime)
- ✅ Indicadores de lectura

### 5. Gestión de Mascotas
- ✅ Registro de mascotas propias
- ✅ Historial médico completo
- ✅ Vacunaciones y tratamientos
- ✅ Medicamentos activos
- ✅ Recordatorios de cuidado
- ✅ Indicadores de bienestar
- ✅ Documentos médicos
- ✅ Planes de cuidado personalizados

### 6. Mapa Interactivo
- ✅ Visualización de reportes cercanos
- ✅ Filtrado por tipo (perdida/encontrada)
- ✅ Actualización de ubicación del usuario
- ✅ Detalles de reporte en modal

---

## 🚀 Deployment y DevOps

### Configuración de Entorno

**Frontend (.env)**:
```env
EXPO_PUBLIC_SUPABASE_URL=https://xxx.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=xxx
EXPO_PUBLIC_GOOGLE_MAPS_API_KEY=xxx
```

**Backend (backend/.env)**:
```env
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_SERVICE_KEY=xxx
ALLOWED_ORIGINS=http://localhost:5173,...
GENERATE_EMBEDDINGS_LOCALLY=true
```

### Docker
- **Backend**: Dockerfile con Python 3.11, dependencias ML
- **Puerto**: 8003
- **Health check**: `/health` endpoint
- **Restart policy**: unless-stopped

### Scripts de Deployment
- `deploy-vm.sh` - Deployment en VM
- `setup-vm.sh` - Configuración inicial
- `update-backend.sh` - Actualización del backend
- `monitor.sh` - Monitoreo de servicios

---

## 📈 Métricas y Monitoreo

### Health Checks
- **Backend**: `GET /health` - Estado de API y Supabase
- **Versión**: `GET /version` - Información de versión
- **Supabase**: `GET /supabase/status` - Estado de conexión

### Logging
- Logs estructurados en backend (Python print/logger)
- Logs de generación de embeddings
- Logs de búsqueda de matches
- Manejo de errores con traceback

---

## 🧪 Testing

### Estructura de Tests
- **Frontend**: Jest + React Native Testing Library
- **Backend**: pytest + pytest-asyncio
- **Cobertura**: pytest-cov

### Archivos de Test
- `tests/` - Tests unitarios e integración
- `backend/test_*.py` - Tests específicos del backend

---

## 📚 Documentación

### Documentación Técnica
- `README.md` - Guía principal
- `CONFIGURACION-SUPABASE.md` - Configuración de BD
- `INSTRUCCIONES-BASE-DATOS-MASCOTAS.md` - Migraciones
- Múltiples archivos `SOLUCION-*.md` - Troubleshooting

### Especificaciones
- `specs/` - Especificaciones de features
- `.specify/memory/constitution.md` - Principios de desarrollo
- `.specify/memory/features-catalog.md` - Catálogo de features

---

## ⚠️ Puntos de Atención y Mejoras Potenciales

### 1. **Rendimiento**
- ⚠️ Generación de embeddings puede ser lenta (60s primera vez)
- ✅ Mitigado con pre-carga del modelo
- 💡 Considerar: Cache más agresivo, CDN para modelos

### 2. **Escalabilidad**
- ⚠️ Búsqueda vectorial puede ser costosa con muchos reportes
- ✅ Índice IVF para optimización
- 💡 Considerar: Particionado de datos, búsqueda aproximada

### 3. **Seguridad**
- ✅ RLS habilitado en todas las tablas
- ⚠️ Validación de inputs en frontend y backend
- 💡 Considerar: Rate limiting, validación más estricta

### 4. **Testing**
- ⚠️ Cobertura de tests no documentada completamente
- 💡 Priorizar: Tests de endpoints críticos, tests de matching

### 5. **Documentación**
- ✅ Buena documentación de configuración
- ⚠️ Falta documentación de API (Swagger/OpenAPI)
- 💡 Considerar: Generar documentación automática de endpoints

### 6. **Manejo de Errores**
- ✅ Try-catch en funciones críticas
- ⚠️ Algunos errores solo se loguean sin notificar al usuario
- 💡 Mejorar: Mensajes de error más descriptivos en frontend

---

## 🎯 Roadmap y Próximos Pasos

Según la Constitución del proyecto (`.specify/memory/constitution.md`):

1. **Historias de Usuario**: Documentar todas las features existentes
2. **Pruebas Unitarias**: Crear tests para cada funcionalidad
3. **Documentación API**: Swagger/OpenAPI para endpoints
4. **Optimizaciones**: Mejorar rendimiento de búsquedas
5. **Notificaciones Push**: Implementar completamente
6. **Analytics**: Tracking de uso y métricas de negocio

---

## 📝 Conclusión

**PetAlert** es un proyecto bien estructurado con:
- ✅ Arquitectura moderna y escalable
- ✅ Uso avanzado de IA para búsqueda visual
- ✅ Sistema completo de gestión de mascotas
- ✅ Buena separación frontend/backend
- ✅ Base de datos bien diseñada con PostGIS y pgvector

**Fortalezas**:
- Sistema de embeddings visuales robusto
- Integración completa con Supabase
- Módulo de salud veterinaria completo
- Código organizado y mantenible

**Áreas de mejora**:
- Documentación de API
- Cobertura de tests
- Optimizaciones de rendimiento
- Manejo de errores más robusto

El proyecto está en un estado avanzado y listo para producción con algunas mejoras menores.

---

**Versión del análisis**: 1.0  
**Última actualización**: 2025-01-27

