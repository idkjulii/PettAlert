# Feature Specification: Mapa Interactivo con Reportes

**Feature Branch**: `006-mapa-interactivo`  
**Created**: 2025-10-05  
**Status**: Implementado (Documentación Retroactiva)  
**Input**: Feature existente - Visualización de reportes en mapa interactivo con marcadores y filtros

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver Reportes en el Mapa (Priority: P1)

Como usuario, quiero ver todos los reportes de mascotas perdidas y encontradas en un mapa interactivo para identificar reportes cercanos a mi ubicación.

**Why this priority**: Es la funcionalidad principal de visualización. El mapa es la forma más intuitiva de ver reportes geográficamente distribuidos.

**Independent Test**: Puede ser testeado completamente abriendo la pantalla principal y verificando que se cargan reportes y se muestran marcadores en el mapa.

**Acceptance Scenarios**:

1. **Given** un usuario que abre la aplicación, **When** accede a la pantalla principal, **Then** ve un mapa con marcadores de reportes cercanos
2. **Given** un usuario en el mapa, **When** el mapa se carga, **Then** se muestra su ubicación actual y reportes en un radio determinado
3. **Given** un usuario en el mapa, **When** ve los marcadores, **Then** los marcadores muestran diferentes colores o iconos para reportes perdidas (rojo) y encontradas (verde)
4. **Given** un usuario en el mapa, **When** toca un marcador, **Then** se abre un modal con información básica del reporte

---

### User Story 2 - Ver Detalles de Reporte desde el Mapa (Priority: P1)

Como usuario, quiero ver detalles completos de un reporte cuando toco su marcador en el mapa para decidir si es relevante para mí.

**Why this priority**: Permite a los usuarios obtener información suficiente del reporte sin salir del mapa, mejorando la experiencia de navegación.

**Independent Test**: Puede ser testeado completamente tocando un marcador y verificando que se muestra el modal con información y opción de ver detalles completos.

**Acceptance Scenarios**:

1. **Given** un usuario en el mapa, **When** toca un marcador de reporte, **Then** se abre un modal mostrando:
   - Tipo de reporte (perdida/encontrada)
   - Nombre de la mascota (si aplica)
   - Foto principal
   - Descripción breve
   - Ubicación aproximada
2. **Given** un usuario que ve el modal de reporte, **When** toca "Ver detalles" o el modal, **Then** navega a la pantalla de detalles completos del reporte
3. **Given** un usuario que ve el modal de reporte, **When** toca fuera del modal o el botón cerrar, **Then** el modal se cierra y vuelve al mapa

---

### User Story 3 - Actualizar Ubicación y Refrescar Reportes (Priority: P2)

Como usuario, quiero poder actualizar mi ubicación y refrescar los reportes para ver los más recientes y cercanos.

**Why this priority**: Permite a los usuarios mantener la información actualizada cuando se mueven o cuando se crean nuevos reportes.

**Independent Test**: Puede ser testeado completamente usando pull-to-refresh y verificando que se actualizan la ubicación y los reportes.

**Acceptance Scenarios**:

1. **Given** un usuario en el mapa, **When** realiza pull-to-refresh, **Then** se actualiza la ubicación del usuario y se recargan los reportes cercanos
2. **Given** un usuario que se ha movido, **When** actualiza el mapa, **Then** el mapa se centra en la nueva ubicación y muestra reportes del nuevo radio
3. **Given** un usuario que actualiza el mapa, **When** hay nuevos reportes, **Then** aparecen nuevos marcadores en el mapa
4. **Given** un usuario que actualiza el mapa, **When** se están cargando datos, **Then** se muestra un indicador de carga

---

### User Story 4 - Crear Nuevo Reporte desde el Mapa (Priority: P2)

Como usuario, quiero poder crear un nuevo reporte directamente desde el mapa para reportar rápidamente una mascota perdida o encontrada.

**Why this priority**: Facilita la creación rápida de reportes desde la pantalla principal, mejorando la accesibilidad de la funcionalidad.

**Independent Test**: Puede ser testeado completamente tocando el botón flotante y verificando que se abre el formulario de creación de reporte.

**Acceptance Scenarios**:

1. **Given** un usuario autenticado en el mapa, **When** toca el botón flotante de crear reporte, **Then** se abre un menú o diálogo para elegir tipo de reporte (perdida/encontrada)
2. **Given** un usuario que elige crear reporte, **When** selecciona el tipo, **Then** navega al formulario correspondiente con la ubicación actual pre-cargada
3. **Given** un usuario no autenticado, **When** intenta crear un reporte, **Then** es redirigido a la pantalla de login

---

### Edge Cases

- ¿Qué sucede cuando el usuario no tiene permisos de ubicación habilitados?
- ¿Cómo maneja el sistema cuando no hay reportes cercanos en el área?
- ¿Qué ocurre si el usuario está en un área sin cobertura de mapas?
- ¿Cómo se maneja cuando hay muchos reportes en un área pequeña (marcadores superpuestos)?
- ¿Qué sucede si el usuario se mueve muy rápido y el mapa no puede seguir su ubicación?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE mostrar un mapa interactivo con marcadores de reportes cercanos
- **FR-002**: El sistema DEBE mostrar la ubicación actual del usuario en el mapa
- **FR-003**: El sistema DEBE mostrar marcadores diferenciados visualmente para reportes perdidas y encontradas
- **FR-004**: El sistema DEBE cargar reportes dentro de un radio determinado desde la ubicación del usuario
- **FR-005**: El sistema DEBE permitir tocar marcadores para ver información del reporte
- **FR-006**: El sistema DEBE mostrar un modal con información básica del reporte al tocar un marcador
- **FR-007**: El sistema DEBE permitir navegar a detalles completos del reporte desde el modal
- **FR-008**: El sistema DEBE permitir cerrar el modal y volver al mapa
- **FR-009**: El sistema DEBE soportar pull-to-refresh para actualizar ubicación y reportes
- **FR-010**: El sistema DEBE actualizar el centro del mapa cuando se actualiza la ubicación del usuario
- **FR-011**: El sistema DEBE mostrar un botón flotante para crear nuevo reporte
- **FR-012**: El sistema DEBE permitir a usuarios autenticados crear reportes desde el mapa
- **FR-013**: El sistema DEBE redirigir usuarios no autenticados a login cuando intentan crear reporte
- **FR-014**: El sistema DEBE pre-cargar la ubicación actual en el formulario de creación de reporte
- **FR-015**: El sistema DEBE mostrar indicadores de carga durante la carga inicial y actualizaciones
- **FR-016**: El sistema DEBE manejar errores de ubicación mostrando mensajes apropiados
- **FR-017**: El sistema DEBE manejar casos cuando no hay reportes cercanos mostrando el mapa vacío

### Key Entities *(include if feature involves data)*

- **Mapa**: Representa la visualización geográfica con centro en ubicación del usuario y marcadores de reportes
- **Marcador**: Representa un punto en el mapa asociado a un reporte, con coordenadas, tipo (perdida/encontrada) y datos básicos
- **Modal de Reporte**: Representa una vista emergente con información resumida de un reporte para preview rápido

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: El mapa se carga y muestra reportes en menos de 3 segundos después de abrir la pantalla
- **SC-002**: Los usuarios pueden ver al menos los 20 reportes más cercanos en el mapa
- **SC-003**: El 95% de los toques en marcadores abren el modal correctamente
- **SC-004**: El pull-to-refresh actualiza reportes en menos de 2 segundos
- **SC-005**: Los usuarios pueden crear un nuevo reporte desde el mapa en menos de 3 toques
- **SC-006**: El sistema maneja correctamente actualizaciones de ubicación cuando el usuario se mueve
- **SC-007**: El mapa mantiene buen rendimiento con hasta 100 marcadores visibles simultáneamente

