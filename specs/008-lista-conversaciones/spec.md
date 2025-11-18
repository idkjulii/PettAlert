# Feature Specification: Lista de Conversaciones

**Feature Branch**: `008-lista-conversaciones`  
**Created**: 2025-10-05  
**Status**: Implementado (Documentación Retroactiva)  
**Input**: Feature existente - Visualización de conversaciones de mensajería del usuario autenticado

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver Lista de Conversaciones (Priority: P1)

Como usuario autenticado, quiero ver una lista de todas mis conversaciones para acceder rápidamente a los chats sobre reportes de mascotas.

**Why this priority**: Es la entrada principal al sistema de mensajería. Sin esta funcionalidad, los usuarios no pueden acceder a sus conversaciones.

**Independent Test**: Puede ser testeado completamente cargando la pantalla y verificando que se muestran todas las conversaciones del usuario.

**Acceptance Scenarios**:

1. **Given** un usuario autenticado con conversaciones existentes, **When** accede a "Mensajes", **Then** ve una lista de todas sus conversaciones
2. **Given** un usuario autenticado sin conversaciones, **When** accede a "Mensajes", **Then** ve un mensaje indicando que no tiene conversaciones todavía
3. **Given** un usuario autenticado, **When** ve la lista de conversaciones, **Then** cada conversación muestra:
   - Nombre del otro usuario
   - Último mensaje o preview
   - Timestamp del último mensaje
   - Indicador de mensajes no leídos (si aplica)
   - Avatar del otro usuario o iniciales

---

### User Story 2 - Ver Preview de Último Mensaje (Priority: P1)

Como usuario, quiero ver un preview del último mensaje en cada conversación para decidir rápidamente cuál abrir.

**Why this priority**: Mejora la experiencia de usuario al permitir identificar conversaciones relevantes sin abrirlas.

**Independent Test**: Puede ser testeado completamente verificando que cada conversación muestra el último mensaje o indicador apropiado.

**Acceptance Scenarios**:

1. **Given** un usuario que ve sus conversaciones, **When** hay un último mensaje de texto, **Then** se muestra el contenido del mensaje (truncado si es muy largo)
2. **Given** un usuario que ve sus conversaciones, **When** el último mensaje es una imagen, **Then** se muestra "📷 Foto" como preview
3. **Given** un usuario que ve sus conversaciones, **When** el último mensaje es del usuario actual, **Then** se muestra "Tú: " antes del preview
4. **Given** un usuario que ve sus conversaciones, **When** no hay mensajes, **Then** se muestra "Toca para comenzar a chatear"

---

### User Story 3 - Indicadores de Mensajes No Leídos (Priority: P2)

Como usuario, quiero ver cuántos mensajes no he leído en cada conversación para priorizar cuáles revisar primero.

**Why this priority**: Ayuda a los usuarios a gestionar sus conversaciones y no perder mensajes importantes.

**Independent Test**: Puede ser testeado completamente verificando que se muestran badges con el conteo de mensajes no leídos.

**Acceptance Scenarios**:

1. **Given** un usuario que ve sus conversaciones, **When** una conversación tiene mensajes no leídos, **Then** se muestra un badge con el número de mensajes no leídos
2. **Given** un usuario que ve sus conversaciones, **When** una conversación no tiene mensajes no leídos, **Then** no se muestra badge
3. **Given** un usuario que lee mensajes en una conversación, **When** vuelve a la lista, **Then** el badge de mensajes no leídos se actualiza o desaparece

---

### User Story 4 - Actualizar Lista de Conversaciones (Priority: P2)

Como usuario, quiero poder actualizar la lista de conversaciones para ver conversaciones nuevas o actualizadas.

**Why this priority**: Permite a los usuarios mantener su lista actualizada cuando reciben nuevos mensajes o se crean nuevas conversaciones.

**Independent Test**: Puede ser testeado completamente usando pull-to-refresh y verificando que se actualizan las conversaciones.

**Acceptance Scenarios**:

1. **Given** un usuario en la lista de conversaciones, **When** realiza pull-to-refresh, **Then** se recargan las conversaciones y se actualiza la lista
2. **Given** un usuario que actualiza la lista, **When** hay nuevas conversaciones, **Then** aparecen en la lista
3. **Given** un usuario que actualiza la lista, **When** hay mensajes nuevos, **Then** se actualizan los previews y timestamps
4. **Given** un usuario que actualiza la lista, **When** se están cargando datos, **Then** se muestra un indicador de carga

---

### User Story 5 - Navegar a Conversación Individual (Priority: P1)

Como usuario, quiero poder tocar una conversación para abrirla y ver todos los mensajes.

**Why this priority**: Es la acción principal de la lista. Sin esta funcionalidad, la lista no tiene propósito.

**Independent Test**: Puede ser testeado completamente tocando una conversación y verificando que navega a la pantalla de conversación individual.

**Acceptance Scenarios**:

1. **Given** un usuario en la lista de conversaciones, **When** toca una conversación, **Then** navega a la pantalla de conversación individual con ese usuario
2. **Given** un usuario que navega a una conversación, **When** se abre, **Then** ve todos los mensajes de esa conversación
3. **Given** un usuario no autenticado, **When** intenta acceder a mensajes, **Then** ve un mensaje pidiendo iniciar sesión con botón para ir a login

---

### Edge Cases

- ¿Qué sucede cuando el usuario tiene muchas conversaciones (más de 100)?
- ¿Cómo maneja el sistema cuando falla la carga de conversaciones?
- ¿Qué ocurre si una conversación se elimina mientras el usuario está viendo la lista?
- ¿Cómo se maneja cuando el otro usuario elimina su cuenta?
- ¿Qué sucede si hay problemas de conexión durante la actualización?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE mostrar una lista de todas las conversaciones del usuario autenticado
- **FR-002**: El sistema DEBE mostrar para cada conversación:
  - Nombre del otro usuario
  - Avatar del otro usuario o iniciales si no hay avatar
  - Preview del último mensaje
  - Timestamp del último mensaje formateado (hoy: hora, otros días: fecha)
  - Badge con conteo de mensajes no leídos (si aplica)
- **FR-003**: El sistema DEBE mostrar "Tú: " antes del preview cuando el último mensaje es del usuario actual
- **FR-004**: El sistema DEBE mostrar "📷 Foto" cuando el último mensaje es una imagen
- **FR-005**: El sistema DEBE mostrar "Toca para comenzar a chatear" cuando no hay mensajes en la conversación
- **FR-006**: El sistema DEBE formatear timestamps:
  - Mensajes de hoy: solo hora (HH:MM)
  - Mensajes anteriores: fecha (DD MMM)
- **FR-007**: El sistema DEBE mostrar un badge rojo con el número de mensajes no leídos cuando hay mensajes sin leer
- **FR-008**: El sistema DEBE permitir pull-to-refresh para actualizar la lista
- **FR-009**: El sistema DEBE permitir tocar una conversación para navegar a la conversación individual
- **FR-010**: El sistema DEBE mostrar un estado vacío cuando el usuario no tiene conversaciones
- **FR-011**: El sistema DEBE mostrar un mensaje para usuarios no autenticados pidiendo iniciar sesión
- **FR-012**: El sistema DEBE proporcionar un botón para ir a login desde el estado no autenticado
- **FR-013**: El sistema DEBE mostrar indicadores de carga durante la carga inicial
- **FR-014**: El sistema DEBE manejar errores mostrando mensajes apropiados con opción de reintentar
- **FR-015**: El sistema DEBE actualizar automáticamente la lista cuando el usuario vuelve a la pantalla (focus)

### Key Entities *(include if feature involves data)*

- **Conversación**: Representa un hilo de mensajería entre dos usuarios, incluyendo metadatos (último mensaje, timestamp, conteo de no leídos, información del otro usuario)
- **Preview de Mensaje**: Representa una vista resumida del último mensaje en una conversación para mostrar en la lista

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: La lista de conversaciones se carga en menos de 2 segundos después de abrir la pantalla
- **SC-002**: Los usuarios pueden ver todas sus conversaciones ordenadas por último mensaje
- **SC-003**: El pull-to-refresh actualiza la lista en menos de 1 segundo
- **SC-004**: Los usuarios pueden navegar a una conversación individual en un solo toque
- **SC-005**: El sistema maneja correctamente listas de hasta 200 conversaciones sin degradación de rendimiento
- **SC-006**: Los indicadores de mensajes no leídos se actualizan correctamente en el 100% de los casos
- **SC-007**: Los timestamps se formatean correctamente según la fecha del mensaje

