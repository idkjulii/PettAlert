# Instrucciones para Agregar Imágenes al Capítulo XIII

Este documento contiene las instrucciones para capturar y agregar las imágenes necesarias al Capítulo XIII de tu tesis, siguiendo el formato de los ejemplos de Eagle Vision y Mascoteando.

---

## Imágenes Requeridas

### 1. Imagen 1: Arquitectura del Sistema ✅
**Ya incluida en el documento**
- Diagrama ASCII de la arquitectura
- Muestra la relación entre App, Supabase y Google Cloud

---

### 2. Imagen 2: Prototipo - Pantalla de Login
**Ubicación**: Sección "Prototipo"

**Qué capturar**:
- Pantalla de inicio de sesión de la aplicación
- Debe mostrar campos de email y contraseña
- Botón de "Iniciar Sesión"
- Opción de registro

**Pie de imagen sugerido**:
```
Imagen 2: Pantalla de inicio de sesión

Fuente: captura de pantalla de la aplicación PetAlert
```

---

### 3. Imagen 3: Prototipo - Mapa con Reportes
**Ubicación**: Sección "Código Fuente del Proyecto"

**Qué capturar**:
- Pantalla principal con el mapa interactivo
- Marcadores de mascotas perdidas (rojos) y encontradas (verdes)
- Botón flotante para crear reporte

**Pie de imagen sugerido**:
```
Imagen 3: Mapa interactivo con reportes geolocalizados

Fuente: captura de pantalla de la aplicación PetAlert
```

---

### 4. Imagen 4: Creación de Reporte
**Ubicación**: Sección "Código Fuente del Proyecto"

**Qué capturar**:
- Formulario de creación de reporte
- Campos de especie, raza, color, etc.
- Botón de captura/selección de foto
- Mapa de ubicación

**Pie de imagen sugerido**:
```
Imagen 4: Formulario de creación de reporte de mascota perdida

Fuente: captura de pantalla de la aplicación PetAlert
```

---

### 5. Imagen 5: Búsqueda con IA
**Ubicación**: Sección "Documentación" - Sistema de IA

**Qué capturar**:
- Pantalla de búsqueda por imagen
- Resultados de similitud con porcentajes
- Fotos de mascotas encontradas similares

**Pie de imagen sugerido**:
```
Imagen 5: Resultados de búsqueda por inteligencia artificial

Fuente: captura de pantalla de la aplicación PetAlert
```

---

### 6. Imagen 6: Chat entre Usuarios
**Ubicación**: Sección "Código Fuente del Proyecto"

**Qué capturar**:
- Pantalla de conversación individual
- Mensajes entre dos usuarios
- Información del reporte relacionado

**Pie de imagen sugerido**:
```
Imagen 6: Sistema de mensajería en tiempo real

Fuente: captura de pantalla de la aplicación PetAlert
```

---

### 7. Imagen 7: Documentación API (Swagger)
**Ubicación**: Sección "Documentación"

**Qué capturar**:
- Abrir http://[tu-backend-ip]:8003/docs
- Capturar la interfaz de Swagger UI
- Mostrar lista de endpoints expandida

**Pie de imagen sugerido**:
```
Imagen 7: Documentación interactiva de la API con Swagger

Fuente: captura de documentación generada automáticamente por FastAPI
```

---

### 8. Imagen 8: Dashboard de Supabase
**Ubicación**: Sección "Base de Datos y Storage"

**Qué capturar**:
- Panel de Supabase mostrando la tabla `reports`
- Debe verse la columna `embedding` con tipo VECTOR(1536)
- Algunos registros de ejemplo

**Pie de imagen sugerido**:
```
Imagen 8: Base de datos con embeddings vectoriales en Supabase

Fuente: captura del panel de administración de Supabase
```

---

### 9. Imagen 9: Google Cloud Platform
**Ubicación**: Sección "Infraestructura de Despliegue"

**Qué capturar**:
- Panel de Google Cloud Console
- VM petalert-backend en ejecución
- Estado, CPU, memoria

**Pie de imagen sugerido**:
```
Imagen 9: Máquina virtual en Google Cloud Platform

Fuente: captura del panel de Google Cloud Console
```

---

### 10. Imagen 10: Repositorio GitHub - Vista General
**Ubicación**: Sección "Repositorio del Proyecto en GitHub"

**Qué capturar**:
- Página principal del repositorio en GitHub
- Estructura de carpetas visible
- README, cantidad de commits, branches

**Pie de imagen sugerido**:
```
Imagen 10: Repositorio del proyecto en GitHub

Fuente: captura del repositorio en GitHub
```

---

### 11. Imagen 11: Repositorio GitHub - Commits
**Ubicación**: Sección "Repositorio del Proyecto en GitHub"

**Qué capturar**:
- Historial de commits del proyecto
- Mensajes descriptivos
- Fechas de commits

**Pie de imagen sugerido**:
```
Imagen 11: Historial de commits del repositorio

Fuente: captura del repositorio en GitHub
```

---

### 12. Imagen 12: Código - Servicio de Embeddings
**Ubicación**: Sección "Código Fuente del Proyecto"

**Qué capturar**:
- Archivo `backend/services/embeddings.py` en VS Code
- Resaltar la clase `EmbeddingService`
- Método `generate_embedding`

**Pie de imagen sugerido**:
```
Imagen 12: Código del servicio de generación de embeddings

Fuente: captura del código en Visual Studio Code
```

---

## Instrucciones de Formato

### Para todas las imágenes:

1. **Resolución**: Mínimo 1920x1080 para capturas de pantalla de escritorio
2. **Formato**: PNG o JPG
3. **Tamaño**: Máximo 2 MB por imagen
4. **Nombre de archivo**: `capitulo-xiii-imagen-XX.png` (donde XX es el número)

### Cómo insertarlas en el documento:

Reemplaza los textos de referencia con:

```markdown
![Descripción](./assets/capitulo-xiii-imagen-XX.png)

**Imagen XX**: Título descriptivo

*Fuente: origen de la imagen*
```

O en formato académico:

```markdown
**Imagen XX**: Título descriptivo

[Insertar imagen aquí]

*Fuente: origen de la imagen*
```

---

## Ubicaciones Específicas en el Documento

### Sección MVP
- Imagen 1: Arquitectura (ya incluida)

### Sección Prototipo
- Imagen 2: Login
- Agregar después de "Ambas versiones permiten experimentar..."

### Sección Código Fuente - Frontend
- Imagen 3: Mapa con reportes
- Imagen 4: Creación de reporte
- Imagen 6: Chat
- Agregar en subsección "Funcionalidades Principales"

### Sección Código Fuente - Backend
- Imagen 7: Swagger UI
- Imagen 12: Código de embeddings
- Agregar en subsección "Documentación Automática"

### Sección Base de Datos
- Imagen 8: Dashboard Supabase
- Agregar después de "Esquema de Base de Datos"

### Sección Infraestructura
- Imagen 9: Google Cloud
- Agregar después de "Google Cloud Platform - Compute Engine"

### Sección Documentación - Sistema de IA
- Imagen 5: Búsqueda con IA
- Agregar después de "Búsqueda por Similitud Vectorial"

### Sección Repositorio GitHub
- Imagen 10: Vista general del repositorio
- Imagen 11: Historial de commits
- Agregar después de "Repositorio en GitHub"

---

## Checklist de Completitud

- [ ] Imagen 1: Arquitectura del sistema ✅ (Ya incluida)
- [ ] Imagen 2: Pantalla de login
- [ ] Imagen 3: Mapa con reportes
- [ ] Imagen 4: Creación de reporte
- [ ] Imagen 5: Búsqueda con IA
- [ ] Imagen 6: Chat entre usuarios
- [ ] Imagen 7: Swagger UI
- [ ] Imagen 8: Dashboard Supabase
- [ ] Imagen 9: Google Cloud Platform
- [ ] Imagen 10: Repositorio GitHub - Vista general
- [ ] Imagen 11: Repositorio GitHub - Commits
- [ ] Imagen 12: Código servicio embeddings

---

## Notas Adicionales

### Para capturas de móvil:
- Usa el emulador de iOS/Android o la app Expo Go
- Asegúrate de que no haya información personal visible
- Preferiblemente usa datos de prueba

### Para capturas de código:
- Usa un tema de VS Code profesional (ej: Dark+ o Material Theme)
- Ajusta el zoom para que el código sea legible
- Resalta las secciones más importantes

### Para capturas de servicios cloud:
- Difumina o censura cualquier credencial visible
- Difumina project IDs si son sensibles
- Asegúrate de que se vea el nombre del proyecto "PetAlert"

---

## Orden de Prioridad

### Alta prioridad (esenciales):
1. Imagen 2: Login
2. Imagen 3: Mapa
3. Imagen 5: Búsqueda IA
4. Imagen 7: Swagger
5. Imagen 10: GitHub

### Media prioridad (recomendadas):
6. Imagen 4: Creación reporte
7. Imagen 8: Supabase
8. Imagen 9: Google Cloud

### Baja prioridad (opcionales):
9. Imagen 6: Chat
10. Imagen 11: Commits
11. Imagen 12: Código

---

## Contacto

Si tienes dudas sobre qué capturar o cómo formatear las imágenes, consulta los PDFs de ejemplo de Eagle Vision y Mascoteando para referencia visual del estilo esperado.


