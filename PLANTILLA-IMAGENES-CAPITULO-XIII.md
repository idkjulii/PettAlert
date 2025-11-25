# 📸 Plantilla para Imágenes del Capítulo XIII

Este documento te ayudará a organizar y numerar correctamente las imágenes que necesitas agregar al Capítulo XIII.

---

## 📱 APLICACIÓN MÓVIL

### Imagen 1: Pantalla de Login
**Ubicación en el capítulo:** Sección 2.3 - Funcionalidades Principales → Autenticación de Usuarios

**Descripción para pie de imagen:**
```
Imagen 1: Pantalla de inicio de sesión con autenticación mediante Supabase. 
El usuario puede ingresar con email y contraseña o registrarse como nuevo usuario.
Fuente: captura de pantalla de la aplicación PetAlert
```

**Qué debe mostrarse:**
- Campo de email
- Campo de contraseña
- Botón "Iniciar Sesión"
- Link "¿No tienes cuenta? Regístrate"
- Logo de la app (si existe)

---

### Imagen 2: Pantalla de Mapa Interactivo
**Ubicación en el capítulo:** Sección 2.3 - Funcionalidades Principales → Pantalla Principal

**Descripción para pie de imagen:**
```
Imagen 2: Mapa interactivo mostrando reportes de mascotas perdidas (marcadores rojos) 
y encontradas (marcadores verdes). El mapa se centra automáticamente en la ubicación 
del usuario y muestra reportes cercanos.
Fuente: captura de pantalla de la aplicación PetAlert
```

**Qué debe mostrarse:**
- Mapa con varios marcadores (rojos y verdes)
- Ubicación actual del usuario
- Botón flotante para crear nuevo reporte
- Tab bar inferior (navegación)

---

### Imagen 3: Formulario de Crear Reporte - Mascota Perdida
**Ubicación en el capítulo:** Sección 2.3 - Funcionalidades Principales → Creación de Reportes

**Descripción para pie de imagen:**
```
Imagen 3: Formulario para reportar mascota perdida. Incluye campos para especie, 
raza, color, tamaño, descripción, selección de foto y ubicación en mapa.
Fuente: captura de pantalla de la aplicación PetAlert
```

**Qué debe mostrarse:**
- Campos del formulario llenos con datos de ejemplo
- Foto de una mascota seleccionada
- Mapa con ubicación marcada
- Botón "Crear Reporte"

---

### Imagen 4: Búsqueda Inteligente con IA
**Ubicación en el capítulo:** Sección 2.3 - Funcionalidades Principales → Búsqueda Inteligente

**Descripción para pie de imagen:**
```
Imagen 4: Resultados de búsqueda por similitud visual usando inteligencia artificial. 
Muestra reportes ordenados por score de similitud (0-1), con foto, descripción y 
distancia desde la ubicación del usuario.
Fuente: captura de pantalla de la aplicación PetAlert
```

**Qué debe mostrarse:**
- Lista de resultados
- Cada resultado con:
  - Foto de la mascota
  - Score de similitud (ej: 0.89)
  - Especie y raza
  - Distancia (ej: 2.5 km)
  - Botón para ver detalles/contactar

---

### Imagen 5: Sistema de Mensajería
**Ubicación en el capítulo:** Sección 2.3 - Funcionalidades Principales → Sistema de Mensajería

**Descripción para pie de imagen:**
```
Imagen 5: Chat entre usuarios para coordinar el reencuentro de mascotas. 
Incluye mensajes en tiempo real, indicadores de lectura y timestamp.
Fuente: captura de pantalla de la aplicación PetAlert
```

**Qué debe mostrarse:**
- Conversación con varios mensajes
- Mensajes del usuario alineados a la derecha
- Mensajes del otro usuario alineados a la izquierda
- Timestamps
- Campo de texto para escribir nuevo mensaje

---

### Imagen 6: Perfil de Usuario y Mis Mascotas
**Ubicación en el capítulo:** Sección 2.3 - Funcionalidades Principales → Gestión de Mascotas

**Descripción para pie de imagen:**
```
Imagen 6: Pantalla de perfil de usuario mostrando información personal y lista 
de mascotas registradas. Cada mascota incluye foto, nombre, especie y raza.
Fuente: captura de pantalla de la aplicación PetAlert
```

**Qué debe mostrarse:**
- Avatar del usuario
- Nombre y email
- Lista de mascotas con foto
- Opciones de configuración
- Botón "Cerrar Sesión"

---

## 🖥️ BACKEND Y DOCUMENTACIÓN

### Imagen 7: Documentación Automática - Swagger UI (Vista General)
**Ubicación en el capítulo:** Sección 3.3 - Endpoints Principales

**Descripción para pie de imagen:**
```
Imagen 7: Documentación automática de la API generada por FastAPI (Swagger UI). 
Muestra la lista completa de endpoints organizados por categorías.
Fuente: captura de pantalla de http://localhost:8003/docs
```

**Qué debe mostrarse:**
- Lista de endpoints colapsados por secciones:
  - Health Check
  - Embeddings
  - Reports
  - Matches
- URL del servidor
- Botón "Try it out"

---

### Imagen 8: Documentación de Endpoint - Búsqueda por Imagen
**Ubicación en el capítulo:** Sección 3.3 - Endpoints Principales → Búsqueda Vectorial

**Descripción para pie de imagen:**
```
Imagen 8: Detalle del endpoint POST /embeddings/search_image mostrando parámetros 
de entrada (query params y form-data), esquema de respuesta y ejemplos de uso.
Fuente: captura de pantalla de la documentación Swagger
```

**Qué debe mostrarse:**
- Endpoint expandido
- Parámetros: file, top_k, min_similarity, lat, lng, max_km
- Schema de Response
- Botón "Try it out"
- Ejemplo de respuesta JSON

---

### Imagen 9: Respuesta de Endpoint - Ejemplo JSON
**Ubicación en el capítulo:** Sección 3.3 - Endpoints Principales → Búsqueda Vectorial

**Descripción para pie de imagen:**
```
Imagen 9: Ejemplo de respuesta JSON del endpoint de búsqueda por similitud, 
mostrando array de resultados con scores, información de mascotas y metadatos.
Fuente: captura de pantalla de respuesta de API
```

**Qué debe mostrarse:**
- JSON formateado con:
  - Array "results" con varios elementos
  - Cada elemento con: report_id, similarity, species, breed, photo_url, etc.
  - search_time_ms
  - query_embedding_dims

---

## 🗄️ BASE DE DATOS

### Imagen 10: Supabase - Table Editor (Tabla Reports)
**Ubicación en el capítulo:** Sección 4.2 - Esquema de Base de Datos → Tabla reports

**Descripción para pie de imagen:**
```
Imagen 10: Vista de la tabla 'reports' en Supabase Table Editor mostrando 
columnas incluyendo la columna 'embedding' de tipo vector(1536) para búsqueda 
por similitud visual.
Fuente: captura de pantalla de Supabase Dashboard
```

**Qué debe mostrarse:**
- Lista de columnas: id, user_id, type, species, breed, color, embedding, location, etc.
- Algunos registros de ejemplo
- Resaltado de la columna "embedding" mostrando tipo vector(1536)

---

### Imagen 11: Supabase - Función RPC
**Ubicación en el capítulo:** Sección 4.4 - Funciones RPC para Búsqueda Vectorial

**Descripción para pie de imagen:**
```
Imagen 11: Función RPC 'search_similar_reports' en el SQL Editor de Supabase. 
Esta función realiza búsqueda vectorial por similitud coseno usando el operador 
<=> de pgvector.
Fuente: captura de pantalla de Supabase SQL Editor
```

**Qué debe mostrarse:**
- SQL Editor con código de la función
- Nombre de la función visible
- Parámetros de entrada
- Query con operador <=>

---

### Imagen 12: Supabase - Storage de Imágenes
**Ubicación en el capítulo:** Sección 4.6 - Supabase Storage

**Descripción para pie de imagen:**
```
Imagen 12: Bucket 'pet-photos' en Supabase Storage mostrando imágenes de mascotas 
almacenadas con URLs públicas y políticas de seguridad configuradas.
Fuente: captura de pantalla de Supabase Storage
```

**Qué debe mostrarse:**
- Lista de buckets
- Contenido del bucket "pet-photos"
- Varias imágenes subidas
- Columnas: name, size, created_at

---

## ☁️ INFRAESTRUCTURA

### Imagen 13: Google Cloud Platform - VM Instances
**Ubicación en el capítulo:** Sección 5.1 - Google Cloud Platform

**Descripción para pie de imagen:**
```
Imagen 13: Instancia de VM 'petalert-backend' ejecutándose en Google Compute Engine 
con configuración e2-medium (2 vCPUs, 4 GB RAM) en la región us-central1.
Fuente: captura de pantalla de Google Cloud Console
```

**Qué debe mostrarse:**
- Lista de VMs
- VM destacada: petalert-backend
- Estado: running (verde)
- IP externa visible
- Tipo de máquina: e2-medium
- Región

---

### Imagen 14: Google Cloud - Reglas de Firewall
**Ubicación en el capítulo:** Sección 5.2 - Configuración de Red y Firewall

**Descripción para pie de imagen:**
```
Imagen 14: Regla de firewall 'allow-petalert-backend' permitiendo tráfico HTTP 
entrante en el puerto 8003 para instancias con el tag 'petalert-backend'.
Fuente: captura de pantalla de Google Cloud VPC Network
```

**Qué debe mostrarse:**
- Lista de reglas de firewall
- Regla destacada: allow-petalert-backend
- Tipo: Ingress
- Puertos: tcp:8003
- Targets: tag petalert-backend
- Source: 0.0.0.0/0

---

### Imagen 15: Docker - Contenedor en Ejecución
**Ubicación en el capítulo:** Sección 5.3 - Containerización con Docker

**Descripción para pie de imagen:**
```
Imagen 15: Salida del comando 'docker-compose ps' mostrando el contenedor 
'petalert-backend' en estado 'running' y escuchando en el puerto 8003.
Fuente: captura de terminal SSH de la VM
```

**Qué debe mostrarse:**
- Terminal con comando docker-compose ps
- Columnas: Name, Command, State, Ports
- Estado: Up (verde)
- Ports: 0.0.0.0:8003->8003/tcp

---

## 📊 DIAGRAMAS

### Imagen 16: Arquitectura del Sistema Completo
**Ubicación en el capítulo:** Sección 1 - MVP → Al inicio

**Descripción para pie de imagen:**
```
Imagen 16: Arquitectura general del sistema PetAlert mostrando la interacción 
entre la aplicación móvil, Supabase (base de datos y storage), y el backend en 
Google Cloud Platform con servicios de inteligencia artificial.
Fuente: elaboración propia
```

**Componentes a incluir:**
```
- Capa de Usuario: Dispositivos iOS/Android
- Capa de Frontend: App React Native (Expo)
- Capa de Backend: Google Cloud VM con FastAPI + Docker
- Capa de Datos: Supabase (PostgreSQL + pgvector + Storage)
- Servicios Externos: Google Cloud Vision API
- Conexiones entre capas con flechas etiquetadas
```

---

### Imagen 17: Diagrama Entidad-Relación
**Ubicación en el capítulo:** Sección 4.2 - Esquema de Base de Datos

**Descripción para pie de imagen:**
```
Imagen 17: Diagrama entidad-relación de la base de datos mostrando las tablas 
principales (users, reports, pets, matches, messages) y sus relaciones.
Fuente: elaboración propia
```

**Tablas a incluir:**
```
users (1) ──< (N) reports
users (1) ──< (N) pets
users (1) ──< (N) messages

reports (1) ──< (N) matches
reports (lost) ──< (1) matches
reports (found) ──< (1) matches

Mostrar:
- Claves primarias (PK)
- Claves foráneas (FK)
- Tipos de datos importantes
- Índices especiales (embedding, location)
```

---

### Imagen 18: Flujo de Búsqueda con IA
**Ubicación en el capítulo:** Sección 6.2 - Proceso de Generación de Embeddings

**Descripción para pie de imagen:**
```
Imagen 18: Flujo completo del proceso de búsqueda por similitud visual, desde 
la captura de la foto hasta la presentación de resultados con scores de similitud.
Fuente: elaboración propia
```

**Pasos del flujo:**
```
1. Usuario toma/selecciona foto → App
2. Redimensionamiento y optimización → Cliente
3. Upload a Supabase Storage → URL pública
4. Backend descarga imagen → Procesamiento
5. Preprocesamiento (384x384, normalización) → Input
6. MegaDescriptor genera embedding → 1536 dims
7. Búsqueda vectorial con pgvector → Similitud coseno
8. Ranking y filtrado → Top K resultados
9. Return a app → Presentación al usuario
```

---

### Imagen 19: Proceso de Detección de Matches
**Ubicación en el capítulo:** Sección 6.4 - Detección Automática de Matches

**Descripción para pie de imagen:**
```
Imagen 19: Algoritmo de detección automática de coincidencias entre reportes 
de mascotas perdidas y encontradas usando múltiples factores de scoring.
Fuente: elaboración propia
```

**Componentes del diagrama:**
```
Input: Nuevo Reporte (con embedding)
     ↓
Tipo = LOST? → Buscar en FOUND
Tipo = FOUND? → Buscar en LOST
     ↓
Búsqueda vectorial (similarity > 0.75)
     ↓
Calcular factores:
- Similitud visual (50%)
- Proximidad geográfica (25%)
- Coincidencia de metadatos (25%)
     ↓
Score >= 80% → Confidence: HIGH
Score >= 60% → Confidence: MEDIUM
Score < 60% → Descartar
     ↓
Guardar matches en BD
     ↓
Notificar a usuarios
```

---

## 💻 CÓDIGO FUENTE

### Imagen 20: Estructura del Proyecto en VS Code
**Ubicación en el capítulo:** Sección 6 - Código Fuente del Proyecto

**Descripción para pie de imagen:**
```
Imagen 20: Estructura de directorios del proyecto PetAlert en Visual Studio Code 
mostrando la organización del código en módulos (app, backend, src, tests).
Fuente: captura de pantalla de Visual Studio Code
```

**Qué debe mostrarse:**
- Explorador de archivos (sidebar izquierdo)
- Carpetas principales expandidas:
  - app/ con subcarpetas (auth), (tabs)
  - backend/ con main.py, routers/, services/
  - src/ con components/, services/, stores/
- Algunos archivos clave visibles

---

### Imagen 21: Código del Servicio de Embeddings
**Ubicación en el capítulo:** Sección 3.4 - Servicio de Embeddings

**Descripción para pie de imagen:**
```
Imagen 21: Implementación del servicio de generación de embeddings usando 
MegaDescriptor-L-384 en Python. La clase EmbeddingService carga el modelo y 
proporciona el método generate_embedding().
Fuente: captura de pantalla del archivo backend/services/embeddings.py
```

**Qué debe mostrarse:**
- Código Python con sintaxis resaltada
- Imports (transformers, torch, PIL)
- Clase EmbeddingService
- Método __init__ con carga del modelo
- Método generate_embedding

---

### Imagen 22: Función RPC de Búsqueda Vectorial (SQL)
**Ubicación en el capítulo:** Sección 4.4 - Funciones RPC

**Descripción para pie de imagen:**
```
Imagen 22: Función PL/pgSQL 'search_similar_reports' que realiza búsqueda vectorial 
usando el operador de distancia coseno (<=>)  de pgvector y retorna reportes 
ordenados por similitud.
Fuente: captura de pantalla del archivo migrations/005_migrate_to_megadescriptor.sql
```

**Qué debe mostrarse:**
- Código SQL formateado
- CREATE FUNCTION
- Parámetros: query_embedding VECTOR(1536)
- RETURN QUERY con operador <=>
- ORDER BY con similitud

---

## 📋 Checklist de Imágenes

Marca cada imagen cuando la hayas capturado e insertado:

### Aplicación Móvil:
- [ ] Imagen 1: Login
- [ ] Imagen 2: Mapa
- [ ] Imagen 3: Crear Reporte
- [ ] Imagen 4: Búsqueda IA
- [ ] Imagen 5: Mensajería
- [ ] Imagen 6: Perfil

### Backend:
- [ ] Imagen 7: Swagger UI General
- [ ] Imagen 8: Endpoint Detallado
- [ ] Imagen 9: Response JSON

### Base de Datos:
- [ ] Imagen 10: Tabla Reports
- [ ] Imagen 11: Función RPC
- [ ] Imagen 12: Storage

### Infraestructura:
- [ ] Imagen 13: VM en GCP
- [ ] Imagen 14: Firewall
- [ ] Imagen 15: Docker

### Diagramas:
- [ ] Imagen 16: Arquitectura
- [ ] Imagen 17: Entidad-Relación
- [ ] Imagen 18: Flujo Búsqueda IA
- [ ] Imagen 19: Detección Matches

### Código:
- [ ] Imagen 20: Estructura VS Code
- [ ] Imagen 21: Código Embeddings
- [ ] Imagen 22: Función SQL

---

## 🎨 Herramientas Recomendadas

### Para diagramas:
- **draw.io** (https://app.diagrams.net/) - Gratuito, exporta PNG/SVG
- **Lucidchart** (https://www.lucidchart.com/) - Profesional
- **dbdiagram.io** (https://dbdiagram.io/) - Específico para ER

### Para capturas de pantalla:
- **Snipping Tool** (Windows) - Win + Shift + S
- **Snagit** - Profesional con anotaciones
- **ShareX** - Gratuito con edición

### Para edición de imágenes:
- **Paint.NET** - Recortar, redimensionar
- **GIMP** - Edición avanzada gratuita
- **Photoshop** - Profesional

### Para formato de código:
- **Carbon** (https://carbon.now.sh/) - Capturas bonitas de código
- **Ray.so** (https://ray.so/) - Alternativa moderna

---

## 💡 Tips para Mejores Capturas

1. **Resolución mínima:** 1920x1080 (Full HD)
2. **Formato:** PNG para pantallas, JPG para fotos reales
3. **Sin información sensible:** Bloquea emails, IPs reales, tokens
4. **Datos realistas:** Usa nombres y descripciones creíbles
5. **Modo claro:** Mejor legibilidad en impresión
6. **Sin barras de sistema:** Oculta notificaciones, hora, batería (si es posible)
7. **Centrado y enfocado:** Encuadra bien lo que quieres mostrar
8. **Consistencia:** Todas las capturas con el mismo estilo/tema

---

¡Con estas 22 imágenes tu Capítulo XIII estará completo y profesional! 📚✨



