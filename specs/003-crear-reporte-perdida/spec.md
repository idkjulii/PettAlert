# Feature Specification: Crear Reporte de Mascota Perdida

**Feature Branch**: `003-crear-reporte-perdida`  
**Created**: 2025-10-05  
**Status**: Implementado (Documentación Retroactiva)  
**Input**: Feature existente - Creación de reportes para mascotas perdidas con información completa, fotos y ubicación

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Crear Reporte Completo de Mascota Perdida (Priority: P1)

Como dueño de una mascota perdida, quiero crear un reporte con toda la información relevante (nombre, especie, descripción, fotos, ubicación) para que la comunidad pueda ayudarme a encontrarla.

**Why this priority**: Es la funcionalidad principal de la aplicación. Sin la capacidad de crear reportes, la aplicación no cumple su propósito principal.

**Independent Test**: Puede ser testeado completamente creando un reporte con todos los campos requeridos y verificando que se guarda correctamente y aparece en el mapa.

**Acceptance Scenarios**:

1. **Given** un usuario autenticado, **When** completa el formulario con nombre, especie, tamaño, descripción, al menos una foto y ubicación, **Then** se crea el reporte exitosamente y se muestra un mensaje de confirmación
2. **Given** un usuario que crea un reporte exitosamente, **When** se completa el proceso, **Then** puede elegir ver el reporte creado o volver a la pantalla anterior
3. **Given** un usuario que crea un reporte, **When** se guarda, **Then** el reporte aparece en el mapa y en la lista de reportes del usuario

---

### User Story 2 - Subida y Gestión de Fotos (Priority: P1)

Como usuario que reporta una mascota perdida, quiero subir múltiples fotos claras de mi mascota (hasta 5) desde mi galería o cámara para ayudar a otros a identificarla.

**Why this priority**: Las fotos son esenciales para la identificación de mascotas. Sin fotos, es muy difícil que otros usuarios reconozcan a la mascota.

**Independent Test**: Puede ser testeado completamente seleccionando fotos desde galería o cámara, verificando que se muestran en el formulario, y que se suben correctamente al servidor.

**Acceptance Scenarios**:

1. **Given** un usuario en el formulario de reporte, **When** toca "Galería" o "Cámara", **Then** puede seleccionar o tomar una foto que se agrega al formulario
2. **Given** un usuario que ha agregado fotos, **When** ve el formulario, **Then** puede ver miniaturas de todas las fotos seleccionadas
3. **Given** un usuario que ha agregado fotos, **When** toca el botón de eliminar en una foto, **Then** esa foto se remueve del formulario
4. **Given** un usuario que intenta agregar más de 5 fotos, **When** intenta seleccionar otra foto, **Then** se muestra un mensaje indicando que el límite es 5 fotos
5. **Given** un usuario que sube fotos, **When** crea el reporte, **Then** las fotos se suben al servidor y se asocian correctamente con el reporte

---

### User Story 3 - Selección de Ubicación (Priority: P1)

Como usuario que reporta una mascota perdida, quiero especificar la ubicación exacta donde se perdió mi mascota usando mi ubicación actual o seleccionando un punto en el mapa para que otros usuarios sepan dónde buscar.

**Why this priority**: La ubicación es crítica para que otros usuarios puedan ayudar a buscar la mascota en el área correcta.

**Independent Test**: Puede ser testeado completamente obteniendo la ubicación GPS, seleccionando un punto en el mapa, y verificando que la ubicación se guarda correctamente con geocodificación inversa.

**Acceptance Scenarios**:

1. **Given** un usuario en el formulario de reporte, **When** el formulario se carga, **Then** se obtiene automáticamente la ubicación GPS actual del usuario
2. **Given** un usuario en el formulario de reporte, **When** toca "Mi ubicación", **Then** se actualiza la ubicación a la posición GPS actual
3. **Given** un usuario en el formulario de reporte, **When** toca "Seleccionar en mapa" y selecciona un punto, **Then** la ubicación se actualiza al punto seleccionado y se muestra la dirección correspondiente
4. **Given** un usuario que selecciona una ubicación, **When** se guarda el reporte, **Then** la ubicación se guarda en formato PostGIS y aparece correctamente en el mapa
5. **Given** un usuario que no puede obtener su ubicación GPS, **When** intenta crear un reporte, **Then** puede seleccionar manualmente una ubicación en el mapa

---

### User Story 4 - Validación de Campos Requeridos (Priority: P2)

Como usuario, quiero recibir retroalimentación clara sobre qué campos son obligatorios y cuáles están incompletos antes de poder crear el reporte.

**Why this priority**: Mejora la experiencia del usuario y asegura que todos los reportes tengan la información mínima necesaria para ser útiles.

**Independent Test**: Puede ser testeado intentando crear un reporte con campos faltantes y verificando que se muestran mensajes de error apropiados.

**Acceptance Scenarios**:

1. **Given** un usuario en el formulario de reporte, **When** intenta crear un reporte sin nombre de mascota, **Then** se muestra un mensaje indicando que el nombre es requerido
2. **Given** un usuario en el formulario de reporte, **When** intenta crear un reporte sin seleccionar especie, **Then** se muestra un mensaje indicando que la especie es requerida
3. **Given** un usuario en el formulario de reporte, **When** intenta crear un reporte sin seleccionar tamaño, **Then** se muestra un mensaje indicando que el tamaño es requerido
4. **Given** un usuario en el formulario de reporte, **When** intenta crear un reporte sin descripción, **Then** se muestra un mensaje indicando que la descripción es requerida
5. **Given** un usuario en el formulario de reporte, **When** intenta crear un reporte sin fotos, **Then** se muestra un mensaje indicando que al menos una foto es requerida
6. **Given** un usuario en el formulario de reporte, **When** intenta crear un reporte sin ubicación, **Then** se muestra un mensaje indicando que la ubicación es requerida

---

### User Story 5 - Edición de Reporte Existente (Priority: P2)

Como usuario que creó un reporte, quiero poder editar la información del reporte para actualizar detalles o corregir errores.

**Why this priority**: Permite a los usuarios mantener la información actualizada, lo cual es crucial para reportes de mascotas perdidas donde los detalles pueden cambiar.

**Independent Test**: Puede ser testeado abriendo un reporte existente en modo edición, modificando campos, y verificando que los cambios se guardan correctamente.

**Acceptance Scenarios**:

1. **Given** un usuario que tiene un reporte creado, **When** accede al modo edición desde "Mis Reportes", **Then** el formulario se carga con todos los datos existentes del reporte
2. **Given** un usuario en modo edición, **When** modifica campos y guarda, **Then** los cambios se actualizan en el reporte existente
3. **Given** un usuario en modo edición, **When** elimina fotos existentes, **Then** esas fotos se remueven del reporte
4. **Given** un usuario en modo edición, **When** agrega nuevas fotos, **Then** las nuevas fotos se agregan a las existentes (hasta el límite de 5)
5. **Given** un usuario que intenta editar un reporte de otro usuario, **When** accede al formulario, **Then** se muestra un error y se previene la edición

---

### Edge Cases

- ¿Qué sucede cuando el usuario no tiene permisos de ubicación habilitados?
- ¿Cómo maneja el sistema cuando falla la geocodificación inversa?
- ¿Qué ocurre si el usuario intenta subir una foto que excede el tamaño máximo permitido?
- ¿Cómo se maneja el caso cuando el usuario pierde conexión a internet durante la subida de fotos?
- ¿Qué sucede si el usuario intenta crear un reporte mientras está en modo avión?
- ¿Cómo se maneja la edición cuando el reporte fue eliminado por otro proceso?
- ¿Qué ocurre si el usuario selecciona una ubicación fuera del área de cobertura del servicio de mapas?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE permitir a usuarios autenticados crear reportes de mascotas perdidas
- **FR-002**: El sistema DEBE requerir los siguientes campos obligatorios para crear un reporte:
  - Nombre de la mascota
  - Especie (perro, gato, ave, conejo, otro)
  - Tamaño (pequeño, mediano, grande)
  - Descripción
  - Al menos una foto
  - Ubicación (coordenadas GPS)
- **FR-003**: El sistema DEBE permitir campos opcionales:
  - Raza
  - Color
  - Señas particulares
  - Recompensa (monto numérico)
- **FR-004**: El sistema DEBE permitir subir hasta 5 fotos por reporte
- **FR-005**: El sistema DEBE permitir seleccionar fotos desde la galería del dispositivo
- **FR-006**: El sistema DEBE permitir tomar fotos con la cámara del dispositivo
- **FR-007**: El sistema DEBE mostrar miniaturas de todas las fotos seleccionadas en el formulario
- **FR-008**: El sistema DEBE permitir eliminar fotos seleccionadas antes de crear el reporte
- **FR-009**: El sistema DEBE obtener automáticamente la ubicación GPS actual del usuario al cargar el formulario
- **FR-010**: El sistema DEBE permitir actualizar la ubicación usando el botón "Mi ubicación"
- **FR-011**: El sistema DEBE permitir seleccionar una ubicación manualmente en un mapa interactivo
- **FR-012**: El sistema DEBE realizar geocodificación inversa para convertir coordenadas en dirección legible
- **FR-013**: El sistema DEBE guardar la ubicación en formato PostGIS (SRID=4326;POINT(lon lat))
- **FR-014**: El sistema DEBE validar todos los campos requeridos antes de permitir crear el reporte
- **FR-015**: El sistema DEBE mostrar mensajes de error específicos para cada campo faltante o inválido
- **FR-016**: El sistema DEBE mostrar un indicador de carga durante la creación del reporte
- **FR-017**: El sistema DEBE subir las fotos a Supabase Storage antes de crear el reporte
- **FR-018**: El sistema DEBE asociar las URLs de las fotos subidas con el reporte
- **FR-019**: El sistema DEBE permitir editar reportes existentes creados por el usuario autenticado
- **FR-020**: El sistema DEBE cargar todos los datos existentes del reporte al entrar en modo edición
- **FR-021**: El sistema DEBE permitir modificar, agregar y eliminar fotos en modo edición
- **FR-022**: El sistema DEBE prevenir que usuarios editen reportes de otros usuarios
- **FR-023**: El sistema DEBE mostrar un mensaje de éxito después de crear o actualizar un reporte exitosamente

### Key Entities *(include if feature involves data)*

- **Reporte**: Representa un reporte de mascota perdida con información básica (nombre, especie, raza, color, tamaño), descripción, señas particulares, fotos (array de URLs), ubicación (PostGIS Point), dirección, recompensa opcional, tipo ("lost"), estado ("active"), y referencia al usuario creador
- **Foto**: Representa una imagen asociada a un reporte, almacenada en Supabase Storage con URL pública
- **Ubicación**: Representa una ubicación geográfica con coordenadas (latitud, longitud) y dirección legible obtenida por geocodificación inversa

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Los usuarios pueden completar la creación de un reporte con todos los campos requeridos en menos de 5 minutos
- **SC-002**: El 90% de los usuarios que inician la creación de un reporte lo completan exitosamente
- **SC-003**: Las fotos se suben al servidor en menos de 10 segundos por foto (para conexiones normales)
- **SC-004**: La geocodificación inversa se completa en menos de 3 segundos en el 95% de los casos
- **SC-005**: El 95% de los reportes creados tienen al menos una foto asociada
- **SC-006**: El 100% de los reportes creados tienen una ubicación válida asociada
- **SC-007**: Los usuarios pueden editar un reporte existente y guardar cambios en menos de 2 minutos
- **SC-008**: El sistema maneja correctamente la creación de al menos 50 reportes concurrentes sin degradación de rendimiento

