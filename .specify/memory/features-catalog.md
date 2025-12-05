# Catálogo de Features Existentes - PetAlert

**Fecha de creación**: 2025-10-05  
**Propósito**: Inventario completo de todas las funcionalidades existentes del sistema para documentar con historias de usuario y pruebas unitarias según la Constitución (Principios IX y X).

---

## Frontend (React Native / Expo)

### 1. Autenticación y Gestión de Usuario

#### 1.1 Login de Usuario
- **Archivo**: `app/(auth)/login.jsx`
- **Funcionalidades**:
  - Inicio de sesión con email y contraseña
  - Validación de campos (email válido, campos no vacíos)
  - Manejo de errores (credenciales inválidas, email no confirmado, demasiados intentos)
  - Navegación a registro y recuperación de contraseña
  - Indicador de carga durante autenticación

#### 1.2 Registro de Usuario
- **Archivo**: `app/(auth)/register.jsx`
- **Funcionalidades**:
  - Registro con nombre completo, email y contraseña
  - Validación de formulario (campos requeridos, email válido, contraseña mínima 6 caracteres)
  - Verificación de coincidencia de contraseñas
  - Indicador de fortaleza de contraseña (Débil/Media/Fuerte)
  - Confirmación de registro y redirección a login
  - Manejo de errores de registro

#### 1.3 Perfil de Usuario
- **Archivo**: `app/(tabs)/profile.jsx`
- **Funcionalidades**:
  - Visualización de información del perfil (nombre, email, teléfono)
  - Edición de datos del perfil (nombre, teléfono)
  - Visualización de estadísticas (email, fecha de registro, estado de verificación)
  - Cierre de sesión con confirmación
  - Manejo de estados de carga

### 2. Reportes de Mascotas

#### 2.1 Crear Reporte de Mascota Perdida
- **Archivo**: `app/report/create-lost.jsx`
- **Funcionalidades**:
  - Formulario completo con información básica (nombre, especie, raza, color, tamaño)
  - Descripción y señas particulares
  - Subida de fotos (máximo 5, desde galería o cámara)
  - Selección de ubicación (GPS actual o selección en mapa)
  - Geocodificación inversa para obtener dirección
  - Campo opcional de recompensa
  - Validación de campos requeridos
  - Modo edición para reportes existentes
  - Subida de fotos a Supabase Storage

#### 2.2 Crear Reporte de Mascota Encontrada
- **Archivo**: `app/report/create-found.jsx`
- **Funcionalidades**:
  - Similar a reporte perdida, pero sin campo de nombre de mascota
  - Campos adicionales: dónde y cuándo se encontró
  - Fecha del encuentro
  - Resto de funcionalidades iguales a reporte perdida

#### 2.3 Visualizar Mis Reportes
- **Archivo**: `app/(tabs)/reports.jsx`
- **Funcionalidades**:
  - Lista de reportes del usuario autenticado
  - Visualización de detalles (tipo, nombre, descripción, fecha, estado)
  - Edición de reportes existentes
  - Eliminación de reportes con confirmación
  - Búsqueda de coincidencias para cada reporte
  - Visualización de matches encontrados con score de similitud
  - Navegación a detalles de reportes coincidentes
  - Manejo de estados de carga y errores

#### 2.4 Mapa Interactivo con Reportes
- **Archivo**: `app/(tabs)/index.jsx` (pantalla principal)
- **Funcionalidades**:
  - Mapa con marcadores de reportes cercanos
  - Filtrado por tipo (perdida/encontrada)
  - Actualización de ubicación del usuario
  - Modal con detalles de reporte al tocar marcador
  - Botón flotante para crear nuevo reporte
  - Pull-to-refresh para actualizar reportes
  - Navegación a detalles completos del reporte

### 3. Búsqueda con Inteligencia Artificial

#### 3.1 Búsqueda por Imagen con IA
- **Archivo**: `app/ai-search.jsx`
- **Funcionalidades**:
  - Configuración de radio de búsqueda (5, 10, 25, 50 km)
  - Búsqueda de coincidencias usando análisis de IA
  - Visualización de resultados con scores de similitud
  - Navegación a detalles de reportes encontrados
  - Manejo de errores de conexión y servidor

### 4. Mensajería

#### 4.1 Lista de Conversaciones
- **Archivo**: `app/(tabs)/messages.jsx`
- **Funcionalidades**:
  - Lista de conversaciones del usuario
  - Visualización de último mensaje y timestamp
  - Indicador de mensajes no leídos
  - Avatar del otro usuario o iniciales
  - Pull-to-refresh para actualizar conversaciones
  - Navegación a conversación individual
  - Manejo de estado no autenticado

#### 4.2 Conversación Individual
- **Archivo**: `app/messages/[conversationId].jsx`
- **Funcionalidades**:
  - Visualización de mensajes de la conversación
  - Envío de mensajes de texto
  - Envío de imágenes
  - Indicadores de estado (enviado, leído)
  - Timestamps formateados
  - Scroll automático a último mensaje
  - Actualización en tiempo real (si está implementado)

### 5. Gestión de Mascotas

#### 5.1 Mis Mascotas
- **Archivo**: `app/(tabs)/pets.jsx`
- **Funcionalidades**:
  - Lista de mascotas registradas del usuario
  - Visualización de información (nombre, especie, raza, tamaño, color)
  - Indicador de estado "perdida" si aplica
  - Fecha de registro
  - Estado vacío si no hay mascotas

---

## Backend (FastAPI)

### 1. API de Reportes

#### 1.1 Gestión de Reportes (`/reports`)
- **Archivo**: `backend/routers/reports.py`
- **Endpoints**:
  - `GET /reports/` - Obtener todos los reportes activos
  - `GET /reports/nearby` - Obtener reportes cercanos por ubicación
  - `GET /reports/{report_id}` - Obtener reporte por ID
  - `POST /reports/` - Crear nuevo reporte
  - `PUT /reports/{report_id}` - Actualizar reporte existente
  - `DELETE /reports/{report_id}` - Eliminar reporte
  - `POST /reports/{report_id}/resolve` - Marcar reporte como resuelto
- **Funcionalidades**:
  - CRUD completo de reportes
  - Cálculo de distancia usando fórmula de Haversine
  - Generación automática de embeddings para búsqueda visual
  - Procesamiento local con MegaDescriptor
  - Validación de datos y manejo de errores
  - Extracción de coordenadas de diferentes formatos (PostGIS, GeoJSON)

#### 1.2 Etiquetas de Reportes (`/reports/{report_id}/labels`)
- **Archivo**: `backend/routers/reports_labels.py`
- **Endpoints**:
  - `POST /reports/{report_id}/labels` - Agregar/actualizar etiquetas de un reporte
- **Funcionalidades**:
  - Procesamiento de etiquetas desde análisis de imágenes
  - Almacenamiento de metadatos de análisis

### 2. API de Coincidencias (Matches)

#### 2.1 Búsqueda de Coincidencias (`/matches`)
- **Archivo**: `backend/routers/matches.py`
- **Endpoints**:
  - `GET /matches/auto-match` - Búsqueda automática de coincidencias
  - `GET /matches/pending` - Obtener matches pendientes
  - `PUT /matches/{match_id}/status` - Actualizar estado de match
- **Funcionalidades**:
  - Algoritmo de matching basado en ubicación, especie y etiquetas
  - Cálculo de scores de similitud
  - Filtrado por radio geográfico
  - Gestión de estados de matches (pending, confirmed, rejected)


#### 3.2 Búsqueda RAG (`/rag-search`)
- **Archivo**: `backend/routers/rag_search.py`
- **Endpoints**:
  - `POST /rag-search/search` - Búsqueda por texto usando RAG
  - `POST /rag-search/search-with-location` - Búsqueda con filtro geográfico
  - `POST /rag-search/save-embedding/{report_id}` - Guardar embedding de reporte
  - `GET /rag-search/embedding/{report_id}` - Obtener embedding de reporte
  - `GET /rag-search/has-embedding/{report_id}` - Verificar si reporte tiene embedding
  - `GET /rag-search/stats` - Estadísticas de embeddings
- **Funcionalidades**:
  - Búsqueda semántica usando embeddings
  - Almacenamiento y recuperación de embeddings
  - Búsqueda con contexto geográfico

### 4. API de Embeddings

#### 4.1 Generación de Embeddings (`/embeddings`)
- **Archivo**: `backend/routers/embeddings.py`
- **Endpoints**:
  - `POST /embeddings/index/{report_id}` - Generar y guardar embedding
  - `POST /embeddings/search_image` - Buscar por similitud de imagen
- **Funcionalidades**:
  - Generación de embeddings para imágenes
  - Búsqueda por similitud visual usando vectores
  - Almacenamiento en Supabase con pgvector

#### 4.2 Embeddings en Supabase (`/embeddings-supabase`)
- **Archivo**: `backend/routers/embeddings_supabase.py`
- **Endpoints**:
  - `POST /embeddings-supabase/generate` - Generar embedding
  - `POST /embeddings-supabase/index/{report_id}` - Indexar reporte
  - `POST /embeddings-supabase/search_image` - Buscar por imagen
- **Funcionalidades**:
  - Integración directa con Supabase para embeddings
  - Búsqueda vectorial usando pgvector


### 6. API Principal

#### 6.1 Endpoints Generales (`/`)
- **Archivo**: `backend/main.py`
- **Endpoints**:
  - `GET /health` - Health check de la API
  - `GET /version` - Información de versión
  - `POST /analyze_image` - Análisis de imagen con Google Vision
  - `POST /caption` - Generar descripción de imagen
  - `GET /supabase/status` - Estado de conexión con Supabase
- **Funcionalidades**:
  - Análisis de imágenes con Google Cloud Vision API
  - Detección de etiquetas y colores dominantes
  - Generación de descripciones automáticas
  - Verificación de estado de servicios

---

## Servicios y Utilidades

### Frontend

#### Servicios de Supabase
- **Archivo**: `src/services/supabase.js`
- **Funcionalidades**:
  - Autenticación (login, registro, logout)
  - Gestión de reportes (CRUD)
  - Gestión de mascotas
  - Gestión de mensajes y conversaciones
  - Consultas a base de datos

#### Servicios de Almacenamiento
- **Archivo**: `src/services/storage.js`
- **Funcionalidades**:
  - Subida de fotos a Supabase Storage
  - Gestión de buckets y permisos

#### Servicios de Ubicación
- **Archivo**: `src/services/location.js`
- **Funcionalidades**:
  - Obtención de ubicación GPS actual
  - Geocodificación inversa (coordenadas → dirección)
  - Manejo de permisos de ubicación

#### Servicios de Búsqueda IA
- **Archivo**: `src/services/aiSearch.js`
- **Funcionalidades**:
  - Búsqueda de coincidencias usando análisis de IA
  - Integración con endpoints de búsqueda

#### Servicios de Búsqueda de Imagen
- **Archivo**: `src/services/searchImage.js`
- **Funcionalidades**:
  - Búsqueda por similitud visual usando CLIP
  - Integración con endpoints de embeddings

### Backend

#### Servicios de Embeddings
- **Archivo**: `backend/services/embeddings.py`
- **Funcionalidades**:
  - Generación de embeddings CLIP para imágenes
  - Conversión de imágenes a vectores
  - Utilidades para procesamiento de imágenes

#### Scripts de Mantenimiento
- **Archivos**: `backend/scripts/`
- **Funcionalidades**:
  - Generación de embeddings faltantes
  - Backfill de embeddings para reportes existentes
  - Utilidades de mantenimiento

---

## Componentes Reutilizables

### Frontend

#### Componentes de Mapa
- **Archivo**: `src/components/Map/MapView.jsx`
- **Funcionalidades**:
  - Renderizado de mapa interactivo
  - Marcadores de reportes
  - Selección de ubicación
  - Visualización de ubicación del usuario

#### Componentes de UI
- **Archivo**: `src/components/UI/ReportModal.jsx`
- **Funcionalidades**:
  - Modal con detalles de reporte
  - Visualización de información completa
  - Acciones (contactar, ver detalles)

---

## Hooks Personalizados

### Frontend

#### Hook de Conversaciones
- **Archivo**: `src/hooks/useConversations.js`
- **Funcionalidades**:
  - Gestión de estado de conversaciones
  - Carga y actualización de conversaciones
  - Manejo de errores y estados de carga

#### Hook de Mensajes
- **Archivo**: `src/hooks/useConversationMessages.js`
- **Funcionalidades**:
  - Gestión de mensajes de una conversación
  - Envío y recepción de mensajes
  - Actualización en tiempo real

#### Hook de Notificaciones Push
- **Archivo**: `src/hooks/usePushNotifications.js`
- **Funcionalidades**:
  - Gestión de notificaciones push
  - Registro de tokens
  - Manejo de notificaciones recibidas

---

## Stores (Estado Global)

### Frontend

#### Store de Autenticación
- **Archivo**: `src/stores/authStore.js`
- **Funcionalidades**:
  - Gestión de estado de autenticación
  - Login, logout, registro
  - Persistencia de sesión
  - Información del usuario autenticado

#### Store de Matches
- **Archivo**: `src/stores/matchStore.js`
- **Funcionalidades**:
  - Gestión de matches por reporte
  - Cache de resultados de búsqueda
  - Estado de matches

---

## Resumen de Features por Categoría

### Autenticación y Usuario (3 features)
1. Login
2. Registro
3. Perfil

### Reportes (4 features)
1. Crear reporte perdida
2. Crear reporte encontrada
3. Ver mis reportes
4. Mapa con reportes

### Búsqueda (1 feature)
1. Búsqueda por IA/CLIP

### Mensajería (2 features)
1. Lista de conversaciones
2. Conversación individual

### Gestión de Mascotas (1 feature)
1. Mis mascotas

### Backend APIs (6 módulos)
1. API de Reportes (7 endpoints)
2. API de Matches (3 endpoints)
3. API de Búsqueda IA (3 endpoints)
4. API de RAG Search (6 endpoints)
5. API de Embeddings (2 módulos, 5 endpoints)
6. Integración n8n (4 endpoints)

**Total**: 11 features frontend + 6 módulos backend con múltiples endpoints

---

## Próximos Pasos

1. ✅ Catálogo de features completado
2. ⏭️ Crear especificaciones con historias de usuario para cada feature
3. ⏭️ Generar pruebas unitarias para cada funcionalidad
4. ⏭️ Validar cumplimiento con la Constitución

