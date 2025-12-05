# Feature Specification: Búsqueda por Imagen con IA

**Feature Branch**: `007-busqueda-ia`  
**Created**: 2025-10-05  
**Status**: Implementado (Documentación Retroactiva)  
**Input**: Feature existente - Búsqueda de coincidencias usando análisis de imágenes mediante MegaDescriptor (procesamiento local)

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Analizar Imagen con IA (Priority: P1)

Como usuario que encontró una mascota o perdió una, quiero subir una foto y analizarla con IA para obtener características visuales (etiquetas y colores) que ayuden a buscar coincidencias.

**Why this priority**: Es el primer paso del proceso de búsqueda con IA. Sin análisis de imagen, no se pueden buscar coincidencias basadas en características visuales.

**Independent Test**: Puede ser testeado completamente subiendo una imagen y verificando que se obtienen etiquetas y colores del análisis.

**Acceptance Scenarios**:

1. **Given** un usuario en la pantalla de búsqueda IA, **When** selecciona una imagen desde galería o cámara, **Then** la imagen se muestra en el formulario
2. **Given** un usuario con imagen seleccionada, **When** toca "Analizar con IA", **Then** se inicia el análisis y se muestra un indicador de carga
3. **Given** un usuario que completa el análisis, **When** se obtienen resultados, **Then** se muestran las etiquetas detectadas con sus scores y los colores dominantes
4. **Given** un usuario que completa el análisis, **When** ve los resultados, **Then** puede usar esa información para buscar coincidencias

---

### User Story 2 - Buscar Coincidencias con Análisis de IA (Priority: P1)

Como usuario con una foto de mascota, quiero buscar coincidencias usando el análisis de IA para encontrar reportes similares basados en características visuales y colores.

**Why this priority**: Es la funcionalidad principal que diferencia esta búsqueda. Conecta el análisis visual con reportes existentes.

**Independent Test**: Puede ser testeado completamente analizando una imagen y luego buscando coincidencias, verificando que se muestran resultados con scores de similitud.

**Acceptance Scenarios**:

1. **Given** un usuario que ha analizado una imagen, **When** toca "Buscar Coincidencias (IA)", **Then** se inicia la búsqueda usando el análisis realizado
2. **Given** un usuario que busca coincidencias, **When** se encuentran resultados, **Then** se muestran reportes con:
   - Score de similitud total (porcentaje)
   - Similitud visual (porcentaje)
   - Similitud de colores (porcentaje)
   - Distancia geográfica (kilómetros)
   - Información básica del reporte
3. **Given** un usuario que busca coincidencias, **When** no se encuentran resultados, **Then** se muestra un mensaje indicando que no hay coincidencias
4. **Given** un usuario que ve resultados, **When** toca un resultado, **Then** navega a los detalles completos de ese reporte

---

### User Story 3 - Buscar Coincidencias por Similitud Visual (Priority: P1)

Como usuario con una foto de mascota, quiero buscar coincidencias usando embeddings de MegaDescriptor para encontrar reportes visualmente similares basados en similitud semántica de imágenes.

**Why this priority**: Proporciona un método avanzado de búsqueda visual que puede encontrar coincidencias que el análisis de etiquetas podría pasar por alto.

**Independent Test**: Puede ser testeado completamente subiendo una imagen y buscando por similitud visual, verificando que se muestran resultados con scores de similitud.

**Acceptance Scenarios**:

1. **Given** un usuario con imagen seleccionada, **When** toca "Buscar por Similitud Visual", **Then** se inicia la búsqueda por similitud visual usando embeddings
2. **Given** un usuario que busca por similitud visual, **When** se encuentran resultados, **Then** se muestran reportes con:
   - Score de similitud (porcentaje)
   - Foto del reporte candidato
   - Información básica (especie, color)
   - Etiquetas si están disponibles
3. **Given** un usuario que busca por similitud visual, **When** se configuran filtros (radio, tipo), **Then** la búsqueda respeta esos filtros
4. **Given** un usuario que ve resultados de similitud visual, **When** toca un resultado, **Then** navega a los detalles completos de ese reporte

---

### User Story 4 - Configurar Filtros de Búsqueda (Priority: P2)

Como usuario, quiero configurar el tipo de búsqueda (perdidas/encontradas/ambas) y el radio geográfico para refinar mis resultados.

**Why this priority**: Permite a los usuarios personalizar la búsqueda según sus necesidades específicas, mejorando la relevancia de los resultados.

**Independent Test**: Puede ser testeado completamente cambiando los filtros y verificando que los resultados se actualizan según la configuración.

**Acceptance Scenarios**:

1. **Given** un usuario en la pantalla de búsqueda IA, **When** selecciona tipo de búsqueda (perdidas/encontradas/ambas), **Then** esa configuración se aplica a búsquedas posteriores
2. **Given** un usuario en la pantalla de búsqueda IA, **When** selecciona radio de búsqueda (5/10/25/50 km), **Then** esa configuración limita los resultados al radio seleccionado
3. **Given** un usuario que busca con filtros configurados, **When** se muestran resultados, **Then** todos los resultados respetan los filtros aplicados
4. **Given** un usuario que cambia los filtros, **When** busca nuevamente, **Then** los nuevos resultados reflejan los filtros actualizados

---

### Edge Cases

- ¿Qué sucede cuando la imagen subida no contiene una mascota?
- ¿Cómo maneja el sistema cuando el análisis de IA falla (servicio externo no disponible)?
- ¿Qué ocurre si el servicio de embeddings no está disponible?
- ¿Qué ocurre si no hay reportes con embeddings en la base de datos?
- ¿Cómo se maneja cuando la búsqueda por similitud visual tarda mucho tiempo?
- ¿Qué sucede cuando el servicio de IA externo está temporalmente no disponible?
- ¿Qué sucede si el usuario no tiene ubicación GPS para el filtro geográfico?
- ¿Cómo se maneja cuando hay muchos resultados (más de 50)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE permitir seleccionar imágenes desde la galería del dispositivo
- **FR-002**: El sistema DEBE permitir tomar fotos con la cámara del dispositivo
- **FR-003**: El sistema DEBE mostrar la imagen seleccionada en el formulario
- **FR-004**: El sistema DEBE permitir analizar imágenes mediante MegaDescriptor (procesamiento local)
- **FR-005**: El sistema DEBE mostrar etiquetas detectadas con sus scores de confianza
- **FR-006**: El sistema DEBE mostrar colores dominantes detectados en la imagen
- **FR-007**: El sistema DEBE permitir buscar coincidencias usando el análisis de IA (etiquetas y colores) obtenido del servicio externo
- **FR-008**: El sistema DEBE permitir buscar coincidencias usando embeddings de MegaDescriptor (similitud visual)
- **FR-009**: El sistema DEBE mostrar resultados de búsqueda con scores de similitud
- **FR-010**: El sistema DEBE mostrar para cada resultado:
  - Score de similitud (porcentaje)
  - Información básica del reporte
  - Foto si está disponible
  - Distancia geográfica si aplica
- **FR-011**: El sistema DEBE permitir configurar tipo de búsqueda (perdidas/encontradas/ambas)
- **FR-012**: El sistema DEBE permitir configurar radio de búsqueda (5, 10, 25, 50 km)
- **FR-013**: El sistema DEBE aplicar filtros geográficos basados en la ubicación del usuario
- **FR-014**: El sistema DEBE permitir navegar a detalles completos de reportes encontrados
- **FR-015**: El sistema DEBE mostrar indicadores de carga durante análisis y búsquedas
- **FR-016**: El sistema DEBE manejar la generación de embeddings con MegaDescriptor
- **FR-017**: El sistema DEBE manejar errores de procesamiento de embeddings mostrando mensajes apropiados
- **FR-018**: El sistema DEBE manejar errores del servidor mostrando mensajes específicos
- **FR-019**: El sistema DEBE mostrar mensajes cuando no se encuentran resultados
- **FR-020**: El sistema DEBE manejar casos cuando el servicio de embeddings no está disponible

### Key Entities *(include if feature involves data)*

- **Análisis de Imagen**: Representa el resultado del análisis de una imagen realizado por MegaDescriptor, incluyendo embeddings vectoriales y metadatos
- **Resultado de Búsqueda IA**: Representa un reporte candidato encontrado usando análisis de etiquetas y colores obtenidos del servicio de IA externo, con scores de similitud visual, similitud de colores, distancia y confianza total
- **Resultado de Búsqueda por Similitud Visual**: Representa un reporte candidato encontrado usando embeddings de MegaDescriptor, con score de similitud visual y metadatos del reporte
- **Sistema de Embeddings**: Representa el procesamiento local de imágenes usando MegaDescriptor para generar embeddings vectoriales

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El análisis de imagen se completa en menos de 10 segundos en el 90% de los casos (generación de embedding con MegaDescriptor)
- **SC-002**: La búsqueda con IA se completa en menos de 15 segundos en el 90% de los casos (búsqueda vectorial en Supabase)
- **SC-003**: La búsqueda por similitud visual se completa en menos de 20 segundos en el 90% de los casos (incluyendo generación de embeddings con MegaDescriptor)
- **SC-004**: El 80% de las búsquedas con imágenes válidas de mascotas retornan al menos un resultado relevante cuando existen reportes compatibles
- **SC-005**: Los usuarios pueden completar todo el flujo (seleccionar imagen, analizar, buscar) en menos de 2 minutos
- **SC-006**: El sistema maneja correctamente errores de procesamiento de embeddings mostrando mensajes útiles en el 100% de los casos
- **SC-007**: Los resultados de búsqueda muestran scores de similitud con precisión suficiente para que usuarios identifiquen coincidencias relevantes
- **SC-008**: El sistema maneja correctamente casos cuando el servicio de IA externo está temporalmente no disponible, informando al usuario apropiadamente

