# 📚 Documentación General - PetAlert MegaDescriptor

## 📋 Tabla de Contenidos

1. [Descripción del Proyecto](#descripción-del-proyecto)
2. [Arquitectura del Sistema](#arquitectura-del-sistema)
3. [Stack Tecnológico](#stack-tecnológico)
4. [Estructura del Proyecto](#estructura-del-proyecto)
5. [Características Principales](#características-principales)
6. [Componentes del Sistema](#componentes-del-sistema)
7. [Configuración e Instalación](#configuración-e-instalación)
8. [Base de Datos](#base-de-datos)
9. [Sistema de IA y Búsqueda](#sistema-de-ia-y-búsqueda)
10. [Despliegue](#despliegue)
11. [Referencias](#referencias)

---

## 🎯 Descripción del Proyecto

**PetAlert** es una aplicación móvil multiplataforma diseñada para ayudar a encontrar mascotas perdidas mediante tecnologías de inteligencia artificial y geolocalización. La aplicación permite a los usuarios:

- **Reportar mascotas perdidas o encontradas** con fotos y ubicación
- **Buscar coincidencias visuales** usando modelos de IA avanzados (MegaDescriptor)
- **Comunicarse entre usuarios** mediante un sistema de mensajería
- **Recibir notificaciones** sobre reportes cercanos
- **Gestionar el historial de salud** de sus mascotas

### Objetivo Principal

Conectar a dueños de mascotas perdidas con personas que las han encontrado, utilizando búsqueda por similitud visual basada en embeddings y análisis de imágenes con IA.

---

## 🏗️ Arquitectura del Sistema

El proyecto sigue una arquitectura de **tres capas**:

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND (Mobile)                    │
│  React Native + Expo | Expo Router |          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ HTTP/HTTPS
                       │
┌──────────────────────▼──────────────────────────────────┐
│                    BACKEND API                          │
│  FastAPI (Python) | MegaDescriptor |          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       │ PostgreSQL + pgvector
                       │
┌──────────────────────▼──────────────────────────────────┐
│              BASE DE DATOS (Supabase)                    │
│  PostgreSQL | pgvector | Storage | Auth | Realtime      │
└─────────────────────────────────────────────────────────┘
```

### Componentes Principales

1. **Frontend (React Native/Expo)**
   - Aplicación móvil multiplataforma (iOS/Android)
   - Navegación con Expo Router
   - Integración con servicios de ubicación y cámara

2. **Backend (FastAPI)**
   - API REST para procesamiento de imágenes
   - Generación de embeddings con MegaDescriptor
   - Búsqueda por similitud visual
   - Gestión de matches y coincidencias

3. **Base de Datos (Supabase)**
   - PostgreSQL con extensión pgvector
   - Autenticación y autorización
   - Almacenamiento de archivos (Storage)
   - Sistema de notificaciones push
   

---

## 🛠️ Stack Tecnológico

### Frontend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **React Native** | 0.81.5 | Framework móvil multiplataforma |
| **Expo** | ~54.0.25 | Plataforma de desarrollo |
| **Expo Router** | ~6.0.13 | Navegación basada en archivos |
| **React Native Paper** | ^5.12.0 | Componentes UI Material Design |
| **React Native Maps** | 1.20.1 | Mapas interactivos |
| **Supabase JS** | ^2.86.0 | Cliente de Supabase |

### Backend

| Tecnología | Versión | Propósito |
|------------|---------|-----------|
| **FastAPI** | >=0.110 | Framework web asíncrono |
| **timm** | >=0.9.0 | Modelos pre-entrenados |
| **MegaDescriptor-L-384** | - | Modelo de embeddings visuales |
| **pgvector** | - | Extensión PostgreSQL para vectores |
| **Supabase Python** | - | Cliente de Supabase |

### Base de Datos

| Tecnología | Propósito |
|------------|-----------|
| **PostgreSQL** | Base de datos relacional |
| **pgvector** | Almacenamiento y búsqueda de vectores |
| **Supabase Auth** | Autenticación de usuarios |
| **Supabase Storage** | Almacenamiento de imágenes |
| **Supabase Realtime** | Actualizaciones en tiempo real |

### DevOps y Deployment

- **Docker** - Containerización del backend
- **Google Cloud Platform** - Hosting de servicios
- **EAS Build** - Compilación de aplicaciones móviles
- **Git** - Control de versiones

---

## 📁 Estructura del Proyecto

```
petAlertMegaDescriptor/
├── app/                          # Páginas de Expo Router
│   ├── (auth)/                   # Pantallas de autenticación
│   │   ├── login.jsx
│   │   ├── register.jsx
│   │   └── forgot-password.jsx
│   ├── (tabs)/                   # Pestañas principales
│   │   ├── index.jsx             # Mapa principal
│   │   ├── reports.jsx           # Mis reportes
│   │   ├── pets.jsx              # Mis mascotas
│   │   ├── messages.jsx          # Mensajes
│   │   └── profile.jsx           # Perfil
│   ├── report/                   # Crear/ver reportes
│   │   ├── create-lost.jsx
│   │   ├── create-found.jsx
│   │   └── [id].jsx
│   ├── pets/                     # Gestión de mascotas
│   │   ├── create.jsx
│   │   └── [petId]/
│   ├── messages/                 # Sistema de mensajería
│   │   └── [conversationId].jsx
│   ├── ai-search.jsx             # Búsqueda con IA
│   └── _layout.jsx               # Layout raíz
│
├── src/                          # Código fuente
│   ├── components/               # Componentes reutilizables
│   │   ├── Map/                  # Componentes del mapa
│   │   └── UI/                   # Componentes de interfaz
│   ├── services/                 # Servicios de API
│   │   ├── supabase.js           # Cliente de Supabase
│   │   ├── location.js           # Servicios de ubicación
│   │   ├── aiSearch.js           # Búsqueda con IA
│   │   └── imagePickerService.js # Selección de imágenes
│   ├── stores/                   # Gestión de estado
│   │   ├── authStore.js          # Store de autenticación
│   │   └── matchStore.js         # Store de matches
│   ├── hooks/                    # Custom hooks
│   │   ├── usePushNotifications.js
│   │   ├── useConversations.js
│   │   └── useConversationMessages.js
│   ├── config/                   # Configuración
│   │   ├── env.js                # Variables de entorno
│   │   └── backend.js             # Configuración del backend
│   └── utils/                    # Utilidades
│       └── eventBus.js           # Sistema de eventos
│
├── backend/                      # Backend Python
│   ├── main.py                   # Aplicación FastAPI principal
│   ├── routers/                  # Endpoints de la API
│   │   ├── embeddings.py         # Generación de embeddings
│   │   ├── ai_search.py          # Búsqueda con IA
│   │   ├── matches.py            # Gestión de matches
│   │   ├── reports.py            # CRUD de reportes
│   │   └── pets.py               # Gestión de mascotas
│   ├── services/                 # Servicios del backend
│   │   └── embeddings.py         # Servicio de embeddings
│   ├── utils/                    # Utilidades del backend
│   │   └── supabase_client.py    # Cliente de Supabase
│   ├── migrations/               # Migraciones SQL
│   │   ├── 001_add_embeddings.sql
│   │   ├── 005_migrate_to_megadescriptor.sql
│   │   └── ...
│   ├── scripts/                  # Scripts de utilidad
│   │   └── backfill_embeddings.py
│   ├── requirements.txt          # Dependencias Python
│   └── Dockerfile                # Imagen Docker
│
├── supabase/                     # Configuración de Supabase
│   └── migrations/               # Migraciones de Supabase
│
├── docs/                         # Documentación
│   ├── guias/                    # Guías paso a paso
│   ├── configuracion/            # Configuración de servicios
│   ├── deploy/                   # Guías de deployment
│   ├── soluciones/               # Soluciones a problemas
│   └── diagnosticos/             # Herramientas de diagnóstico
│
├── components/                   # Componentes de plantilla Expo
├── assets/                       # Imágenes y archivos estáticos
├── scripts/                      # Scripts de automatización
├── tests/                        # Tests automatizados
│
├── package.json                  # Dependencias Node.js
├── app.config.js                 # Configuración de Expo
├── eas.json                      # Configuración de EAS Build
├── docker-compose.yml            # Orquestación Docker
├── env.example                   # Plantilla de variables de entorno
└── README.md                     # Documentación principal
```

---

## ✨ Características Principales

### 1. 🔐 Autenticación y Usuarios

- **Registro e inicio de sesión** con Supabase Auth
- **Recuperación de contraseña** por email
- **Gestión de perfiles** de usuario
- **Sesiones persistentes** con almacenamiento seguro

### 2. 📍 Reportes de Mascotas

- **Crear reportes de mascotas perdidas** con:
  - Foto de la mascota
  - Ubicación GPS
  - Descripción detallada
  - Especie, raza, color
  - Fecha y hora del evento
  
- **Crear reportes de mascotas encontradas** con información similar
- **Visualizar reportes en mapa** con marcadores personalizados
- **Filtros avanzados** por tipo, especie, fecha, ubicación

### 3. 🔍 Búsqueda con Inteligencia Artificial

#### Búsqueda por Similitud Visual (MegaDescriptor)

- **Modelo**: MegaDescriptor-L-384
- **Dimensiones de embedding**: 1536
- **Tecnología**: pgvector para búsqueda k-NN
- **Funcionalidad**: 
  - Subir foto de una mascota
  - Generar embedding con MegaDescriptor
  - Buscar reportes similares en la base de datos
  - Mostrar resultados ordenados por similitud

#### Búsqueda Híbrida

- **Búsqueda por características** (color, especie, raza)
- **Filtros geográficos** (radio de búsqueda)
- **Puntuación combinada** de similitud

### 4. 🗺️ Mapa Interactivo

- **Visualización de reportes** en mapa
- **Marcadores personalizados** por tipo de reporte
- **Navegación a detalles** desde marcadores
- **Actualización automática** de reportes cercanos

### 5. 💬 Sistema de Mensajería

- **Conversaciones entre usuarios** sobre reportes
- **Mensajes en tiempo real** con Supabase Realtime
- **Notificaciones push** de nuevos mensajes
- **Historial de conversaciones** persistente

### 6. 🔔 Notificaciones

- **Notificaciones push** para:
  - Nuevos reportes cercanos
  - Matches encontrados
  - Nuevos mensajes
  - Alertas geográficas personalizadas

- **Configuración de alertas geográficas**:
  - Radio de alerta personalizable
  - Tipos de reportes a recibir
  - Frecuencia de notificaciones

### 7. 🐾 Gestión de Mascotas

- **Registro de mascotas propias**
- **Historial de salud**:
  - Vacunaciones
  - Medicamentos
  - Eventos de salud
  - Recordatorios
  - Wellness checks

### 8. 🤝 Sistema de Matches

- **Detección automática** de posibles coincidencias
- **Puntuación de similitud** entre reportes
- **Notificaciones** cuando se encuentra un match
- **Historial de matches** guardado

---

## 🔧 Componentes del Sistema

### Frontend - Componentes Principales

#### Navegación (Expo Router)

- **`(auth)/`**: Flujo de autenticación
- **`(tabs)/`**: Navegación principal con pestañas
- **`report/`**: Creación y visualización de reportes
- **`pets/`**: Gestión de mascotas
- **`messages/`**: Sistema de mensajería

#### Servicios

- **`supabase.js`**: Cliente de Supabase para operaciones de base de datos
- **`location.js`**: Servicios de geolocalización
- **`aiSearch.js`**: Integración con búsqueda por IA
- **`imagePickerService.js`**: Selección y procesamiento de imágenes

#### Stores (Zustand)

- **`authStore.js`**: Estado de autenticación del usuario
- **`matchStore.js`**: Estado de matches y coincidencias

### Backend - Endpoints Principales

#### `/embeddings/`

- `POST /embeddings/index/{report_id}`: Generar embedding para un reporte
- `POST /embeddings/search_image`: Buscar por similitud visual
- `GET /embeddings/status`: Estado del servicio de embeddings

#### `/ai-search/`

- `POST /ai-search/search`: Búsqueda híbrida con IA
- `POST /ai-search/analyze`: Análisis de imagen con IA

#### `/matches/`

- `GET /matches/{report_id}`: Obtener matches de un reporte
- `POST /matches/create`: Crear match manualmente
- `GET /matches/user`: Matches del usuario actual

#### `/reports/`

- `GET /reports`: Listar reportes
- `POST /reports`: Crear reporte
- `GET /reports/{id}`: Obtener reporte específico
- `PUT /reports/{id}`: Actualizar reporte
- `DELETE /reports/{id}`: Eliminar reporte

#### `/pets/`

- `GET /pets`: Listar mascotas del usuario
- `POST /pets`: Crear mascota
- `GET /pets/{id}`: Obtener mascota específica
- `PUT /pets/{id}`: Actualizar mascota

---

## ⚙️ Configuración e Instalación

### Prerrequisitos

- **Node.js** (v18 o superior)
- **npm** o **yarn**
- **Python** (3.9 o superior)
- **Expo CLI** (`npm install -g expo-cli`)
- **Docker** (opcional, para backend)
- **Cuenta de Supabase**

### Instalación del Frontend

```bash
# 1. Clonar el repositorio
git clone <repository-url>
cd petAlertMegaDescriptor

# 2. Instalar dependencias
npm install

# 3. Configurar variables de entorno
cp env.example .env
# Editar .env con tus credenciales de Supabase

# 4. Iniciar servidor de desarrollo
npm start
```

### Instalación del Backend

```bash
# 1. Navegar a la carpeta backend
cd backend

# 2. Crear entorno virtual (recomendado)
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Configurar variables de entorno
cp env.example .env
# Editar .env con tus credenciales de Supabase

# 5. Iniciar servidor
uvicorn main:app --reload --port 8003
```

### Configuración de Variables de Entorno

#### Frontend (`.env`)

```env
# Supabase Configuration
EXPO_PUBLIC_SUPABASE_URL=https://tu-proyecto.supabase.co
EXPO_PUBLIC_SUPABASE_ANON_KEY=tu-clave-anonima-aqui

# App Configuration
EXPO_PUBLIC_APP_NAME=PetAlert
EXPO_PUBLIC_APP_VERSION=1.0.0

# Backend URL
EXPO_PUBLIC_BACKEND_URL=http://localhost:8003
# O para desarrollo en red:
# EXPO_PUBLIC_BACKEND_URL=http://192.168.0.204:8003
```

#### Backend (`backend/.env`)

```env
# Supabase Configuration
SUPABASE_URL=https://tu-proyecto.supabase.co
SUPABASE_SERVICE_KEY=tu-clave-service-role-aqui

# CORS Configuration
ALLOWED_ORIGINS=http://localhost:8081,http://127.0.0.1:8081

# Embeddings Configuration
GENERATE_EMBEDDINGS_LOCALLY=true
```

### Configuración de Supabase

1. **Crear proyecto en Supabase**
2. **Ejecutar migraciones SQL** desde `backend/migrations/`
3. **Configurar Storage** para imágenes
4. **Configurar autenticación** (Email/Password)
5. **Habilitar extensión pgvector**:

```sql
create extension if not exists vector;
```

6. **Configurar políticas RLS** (Row Level Security)

---

## 🗄️ Base de Datos

### Esquema Principal

#### Tabla: `reports`

Almacena los reportes de mascotas perdidas/encontradas.

```sql
CREATE TABLE reports (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  type TEXT NOT NULL, -- 'lost' o 'found'
  species TEXT,
  breed TEXT,
  color TEXT,
  description TEXT,
  location POINT, -- Coordenadas geográficas
  photo_url TEXT,
  embedding vector(1536), -- Embedding de MegaDescriptor
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabla: `pets`

Almacena las mascotas registradas por los usuarios.

```sql
CREATE TABLE pets (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID REFERENCES auth.users(id),
  name TEXT NOT NULL,
  species TEXT,
  breed TEXT,
  color TEXT,
  photo_url TEXT,
  birth_date DATE,
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabla: `matches`

Almacena las coincidencias detectadas entre reportes.

```sql
CREATE TABLE matches (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  lost_report_id UUID REFERENCES reports(id),
  found_report_id UUID REFERENCES reports(id),
  similarity_score FLOAT,
  status TEXT, -- 'pending', 'confirmed', 'rejected'
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabla: `conversations`

Almacena las conversaciones entre usuarios.

```sql
CREATE TABLE conversations (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  report_id UUID REFERENCES reports(id),
  user1_id UUID REFERENCES auth.users(id),
  user2_id UUID REFERENCES auth.users(id),
  created_at TIMESTAMP DEFAULT NOW()
);
```

#### Tabla: `messages`

Almacena los mensajes de las conversaciones.

```sql
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  conversation_id UUID REFERENCES conversations(id),
  sender_id UUID REFERENCES auth.users(id),
  content TEXT NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
```

### Índices Vectoriales

Para optimizar la búsqueda por similitud:

```sql
-- Índice IVF para búsqueda rápida de vectores
CREATE INDEX idx_reports_embedding_ivf
  ON reports USING ivfflat (embedding vector_cosine_ops)
  WITH (lists = 100);
```

### Funciones RPC

- `generate_embedding(report_id)`: Genera embedding para un reporte
- `search_similar_reports(embedding, top_k)`: Busca reportes similares
- `create_match(lost_id, found_id)`: Crea un match entre reportes

---

## 🤖 Sistema de IA y Búsqueda

### Modelo MegaDescriptor

**MegaDescriptor-L-384** es el modelo utilizado para generar embeddings visuales:

- **Arquitectura**: Swin-L-384 (Swin Transformer Large)
- **Dimensiones de embedding**: 1536
- **Tamaño de entrada**: 384x384 píxeles
- **Tamaño del modelo**: ~900MB
- **Framework**: PyTorch con timm

### Flujo de Búsqueda por Similitud

1. **Usuario sube imagen** de una mascota
2. **Backend procesa imagen**:
   - Redimensiona a 384x384
   - Genera embedding con MegaDescriptor
   - Vector de 1536 dimensiones
3. **Búsqueda en base de datos**:
   - Usa pgvector para búsqueda k-NN
   - Calcula similitud coseno
   - Retorna top-K resultados
4. **Frontend muestra resultados** ordenados por similitud

### Algoritmo de Puntuación

Para búsquedas híbridas, se combinan múltiples factores:

```
Puntuación Total = 
  Similitud Visual × 0.4 +      // 40% - Embedding MegaDescriptor
  Similitud de Colores × 0.3 +  // 30% - Colores dominantes
  Proximidad Geográfica × 0.2 + // 20% - Distancia del usuario
  Relevancia Temporal × 0.1     // 10% - Antigüedad del reporte
```

### Optimizaciones

- **Pre-carga del modelo** al iniciar el servidor
- **Caché de embeddings** para evitar recálculos
- **Búsqueda asíncrona** para no bloquear la API
- **Índices vectoriales** para búsqueda rápida

---

## 🚀 Despliegue

### Frontend (EAS Build)

```bash
# 1. Configurar EAS
eas build:configure

# 2. Build para Android
eas build --platform android --profile production

# 3. Build para iOS
eas build --platform ios --profile production
```

### Backend (Docker + Google Cloud)

```bash
# 1. Construir imagen Docker
cd backend
docker build -t petalert-backend .

# 2. Ejecutar con docker-compose
docker-compose up -d

# 3. O desplegar en Google Cloud
# Ver docs/deploy/GUIA-COMPLETA-DOCKER-GOOGLE-CLOUD.md
```

### Variables de Entorno en Producción

Asegúrate de configurar:

- `EXPO_PUBLIC_BACKEND_URL`: URL pública del backend
- `SUPABASE_URL`: URL de Supabase
- `SUPABASE_SERVICE_KEY`: Service role key (solo backend)
- `ALLOWED_ORIGINS`: Orígenes permitidos para CORS

---

## 📖 Referencias

### Documentación Adicional

- **[README.md](./README.md)**: Documentación principal del proyecto
- **[docs/README.md](./docs/README.md)**: Índice completo de documentación
- **[docs/guias/LEE-ESTO-PRIMERO.md](./docs/guias/LEE-ESTO-PRIMERO.md)**: Guía de inicio rápido
- **[backend/README.md](./backend/README.md)**: Documentación del backend

### Guías Principales

- **Configuración de Supabase**: `docs/configuracion/CONFIGURACION-SUPABASE.md`
- **Build de la App**: `docs/guias/GUIA-SIMPLE-BUILD-APP.md`
- **Deploy con Docker**: `docs/guias/GUIA-COMPLETA-DOCKER-GOOGLE-CLOUD.md`
- **Sistema de IA**: `docs/README-AI-SEARCH.md`
- **Alertas Geográficas**: `docs/guias/GUIA-ALERTAS-GEOGRAFICAS.md`

### Especificaciones

- **Especificaciones de Features**: `specs/README.md`
- **Historias de Usuario**: `specs/*/spec.md`

### Recursos Externos

- [Expo Documentation](https://docs.expo.dev/)
- [Supabase Documentation](https://supabase.com/docs)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [pgvector Documentation](https://github.com/pgvector/pgvector)
- [MegaDescriptor Model](https://huggingface.co/models?search=megadescriptor)

---

## 📝 Notas Adicionales

### Costos de Cómputo

El proyecto incluye un notebook (`calculo_costo_megadescriptor.ipynb`) para calcular los costos asociados con el uso de MegaDescriptor en producción.

### Testing

- **Frontend**: Jest + React Native Testing Library
- **Backend**: pytest + pytest-asyncio
- Ver `docs/README-TESTING.md` para más información

### Contribución

1. Fork el repositorio
2. Crea una rama para tu feature (`git checkout -b feature/nueva-caracteristica`)
3. Commit tus cambios (`git commit -m 'Agrega nueva característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abre un Pull Request

---

## 📄 Licencia

Este proyecto está licenciado bajo la Licencia MIT.

---

## 🙏 Agradecimientos

- [Expo](https://expo.dev) por el framework de desarrollo
- [Supabase](https://supabase.com) por la plataforma de backend
- [React Native Paper](https://reactnativepaper.com) por los componentes de UI
- La comunidad de React Native por el apoyo y recursos
- Hugging Face por los modelos pre-entrenados

---

**Última actualización**: 2024

