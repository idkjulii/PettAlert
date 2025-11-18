# Feature Specification: Visualizar Mis Reportes

**Feature Branch**: `005-ver-mis-reportes`  
**Created**: 2025-10-05  
**Status**: Implementado (Documentación Retroactiva)  
**Input**: Feature existente - Visualización y gestión de reportes creados por el usuario autenticado

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver Lista de Mis Reportes (Priority: P1)

Como usuario autenticado, quiero ver una lista de todos los reportes que he creado para poder revisarlos, editarlos o eliminarlos.

**Why this priority**: Es esencial para que los usuarios puedan gestionar sus propios reportes. Sin esta funcionalidad, no pueden acceder a reportes creados previamente.

**Independent Test**: Puede ser testeado completamente cargando la pantalla y verificando que se muestran todos los reportes del usuario autenticado.

**Acceptance Scenarios**:

1. **Given** un usuario autenticado con reportes creados, **When** accede a "Mis Reportes", **Then** ve una lista de todos sus reportes activos
2. **Given** un usuario autenticado sin reportes, **When** accede a "Mis Reportes", **Then** ve un mensaje indicando que no tiene reportes creados aún
3. **Given** un usuario autenticado, **When** ve la lista de reportes, **Then** cada reporte muestra tipo (perdida/encontrada), nombre (si aplica), descripción, fecha y estado
4. **Given** un usuario autenticado, **When** ve la lista de reportes, **Then** no se muestran reportes con estado "cancelled"

---

### User Story 2 - Editar Reporte Existente (Priority: P1)

Como usuario que creó un reporte, quiero poder editarlo para actualizar información, agregar fotos o corregir errores.

**Why this priority**: Permite a los usuarios mantener la información actualizada, lo cual es crucial especialmente para reportes de mascotas perdidas donde los detalles pueden cambiar.

**Independent Test**: Puede ser testeado completamente tocando el botón de editar en un reporte y verificando que se abre el formulario con los datos existentes.

**Acceptance Scenarios**:

1. **Given** un usuario que ve sus reportes, **When** toca el botón de editar en un reporte, **Then** se abre el formulario correspondiente (perdida o encontrada) con todos los datos cargados
2. **Given** un usuario en modo edición, **When** modifica campos y guarda, **Then** los cambios se actualizan en el reporte
3. **Given** un usuario en modo edición, **When** agrega nuevas fotos, **Then** las nuevas fotos se combinan con las existentes
4. **Given** un usuario en modo edición, **When** elimina fotos existentes, **Then** esas fotos se remueven del reporte
5. **Given** un usuario que intenta editar un reporte de otro usuario, **When** accede al formulario, **Then** se muestra un error y se previene la edición

---

### User Story 3 - Eliminar Reporte (Priority: P2)

Como usuario que creó un reporte, quiero poder eliminarlo cuando ya no sea necesario (mascota encontrada, reporte duplicado, etc.).

**Why this priority**: Permite a los usuarios limpiar reportes obsoletos y mantener su lista organizada.

**Independent Test**: Puede ser testeado completamente tocando el botón de eliminar, confirmando la acción, y verificando que el reporte se elimina.

**Acceptance Scenarios**:

1. **Given** un usuario que ve sus reportes, **When** toca el botón de eliminar en un reporte, **Then** se muestra un diálogo de confirmación con el nombre de la mascota
2. **Given** un usuario en el diálogo de confirmación, **When** confirma la eliminación, **Then** el reporte se elimina y desaparece de la lista
3. **Given** un usuario en el diálogo de confirmación, **When** cancela la eliminación, **Then** el diálogo se cierra y el reporte permanece en la lista
4. **Given** un usuario que elimina un reporte, **When** se completa la eliminación, **Then** se muestra un mensaje de éxito y la lista se actualiza

---

### User Story 4 - Buscar Coincidencias para Mis Reportes (Priority: P2)

Como usuario con un reporte de mascota perdida, quiero poder buscar coincidencias con reportes de mascotas encontradas para encontrar a mi mascota.

**Why this priority**: Es la funcionalidad que conecta reportes perdidas con encontradas, el propósito principal de la aplicación.

**Independent Test**: Puede ser testeado completamente tocando "Buscar coincidencias" en un reporte y verificando que se muestran resultados con scores de similitud.

**Acceptance Scenarios**:

1. **Given** un usuario que ve sus reportes, **When** toca "Buscar coincidencias" en un reporte perdida, **Then** se inicia el proceso de búsqueda y se muestra un indicador de carga
2. **Given** un usuario que busca coincidencias, **When** se encuentran resultados, **Then** se muestran los reportes coincidentes con score de similitud, foto y botón para ver detalles
3. **Given** un usuario que busca coincidencias, **When** no se encuentran resultados, **Then** se muestra un mensaje indicando que no hay coincidencias por ahora
4. **Given** un usuario que ve coincidencias, **When** toca "Ver reporte" en una coincidencia, **Then** navega a los detalles completos de ese reporte
5. **Given** un usuario que busca coincidencias, **When** ocurre un error, **Then** se muestra un mensaje de error apropiado

---

### Edge Cases

- ¿Qué sucede cuando el usuario tiene muchos reportes (más de 50)?
- ¿Cómo maneja el sistema cuando falla la carga de reportes?
- ¿Qué ocurre si el usuario intenta editar un reporte que fue eliminado por otro proceso?
- ¿Cómo se maneja cuando la búsqueda de coincidencias tarda mucho tiempo?
- ¿Qué sucede si el usuario elimina un reporte mientras está buscando coincidencias?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE mostrar una lista de todos los reportes activos creados por el usuario autenticado
- **FR-002**: El sistema DEBE filtrar y no mostrar reportes con estado "cancelled"
- **FR-003**: El sistema DEBE mostrar para cada reporte:
  - Tipo (perdida/encontrada) con indicador visual
  - Nombre de la mascota (si aplica)
  - Descripción (truncada si es muy larga)
  - Fecha de creación
  - Estado (activo/resuelto)
- **FR-004**: El sistema DEBE mostrar un estado vacío cuando el usuario no tiene reportes
- **FR-005**: El sistema DEBE permitir editar reportes existentes del usuario autenticado
- **FR-006**: El sistema DEBE cargar todos los datos del reporte al entrar en modo edición
- **FR-007**: El sistema DEBE prevenir que usuarios editen reportes de otros usuarios
- **FR-008**: El sistema DEBE permitir eliminar reportes del usuario autenticado
- **FR-009**: El sistema DEBE mostrar un diálogo de confirmación antes de eliminar un reporte
- **FR-010**: El sistema DEBE mostrar el nombre de la mascota en el diálogo de confirmación
- **FR-011**: El sistema DEBE actualizar la lista después de eliminar un reporte
- **FR-012**: El sistema DEBE permitir buscar coincidencias para cada reporte del usuario
- **FR-013**: El sistema DEBE mostrar un indicador de carga durante la búsqueda de coincidencias
- **FR-014**: El sistema DEBE mostrar resultados de coincidencias con:
  - Score de similitud (porcentaje)
  - Foto de la mascota encontrada
  - Información básica del reporte
  - Botón para ver detalles completos
- **FR-015**: El sistema DEBE mostrar un mensaje cuando no se encuentran coincidencias
- **FR-016**: El sistema DEBE manejar errores durante la búsqueda de coincidencias mostrando mensajes apropiados
- **FR-017**: El sistema DEBE permitir navegar a detalles de reportes coincidentes
- **FR-018**: El sistema DEBE mostrar estados de carga apropiados durante todas las operaciones

### Key Entities *(include if feature involves data)*

- **Lista de Reportes**: Representa una colección de reportes del usuario autenticado, filtrada por estado activo
- **Coincidencia**: Representa un match entre un reporte perdida y un reporte encontrada, incluyendo score de similitud y referencias a ambos reportes

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Los usuarios pueden ver su lista de reportes en menos de 2 segundos después de abrir la pantalla
- **SC-002**: El 100% de los reportes activos del usuario se muestran correctamente en la lista
- **SC-003**: Los usuarios pueden editar un reporte existente y guardar cambios en menos de 2 minutos
- **SC-004**: Los usuarios pueden eliminar un reporte en menos de 5 segundos desde que confirman la acción
- **SC-005**: La búsqueda de coincidencias se completa en menos de 10 segundos en el 90% de los casos
- **SC-006**: El 95% de las búsquedas de coincidencias muestran resultados relevantes cuando existen reportes compatibles
- **SC-007**: El sistema maneja correctamente listas de hasta 100 reportes por usuario sin degradación de rendimiento

