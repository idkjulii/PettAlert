# Feature Specification: Crear Reporte de Mascota Encontrada

**Feature Branch**: `004-crear-reporte-encontrada`  
**Created**: 2025-10-05  
**Status**: Implementado (Documentación Retroactiva)  
**Input**: Feature existente - Creación de reportes para mascotas encontradas con información completa, fotos y ubicación

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Crear Reporte de Mascota Encontrada (Priority: P1)

Como persona que encontró una mascota, quiero crear un reporte con información sobre la mascota encontrada (especie, descripción, fotos, ubicación, dónde y cuándo la encontré) para ayudar a reunirla con su familia.

**Why this priority**: Es una funcionalidad core complementaria a los reportes de mascotas perdidas. Permite que la comunidad complete el ciclo de búsqueda y reunión.

**Independent Test**: Puede ser testeado completamente creando un reporte con todos los campos requeridos y verificando que se guarda correctamente y aparece en el mapa.

**Acceptance Scenarios**:

1. **Given** un usuario autenticado, **When** completa el formulario con especie, tamaño, descripción, información del encuentro, al menos una foto y ubicación, **Then** se crea el reporte exitosamente y se muestra un mensaje de confirmación
2. **Given** un usuario que crea un reporte de mascota encontrada exitosamente, **When** se completa el proceso, **Then** puede elegir ver el reporte creado o volver a la pantalla anterior
3. **Given** un usuario que crea un reporte de mascota encontrada, **When** se guarda, **Then** el reporte aparece en el mapa y puede ser encontrado por usuarios que buscan su mascota perdida

---

### User Story 2 - Información del Encuentro (Priority: P1)

Como persona que encontró una mascota, quiero especificar dónde y cuándo la encontré para proporcionar información precisa que ayude a identificar a la mascota.

**Why this priority**: La información del encuentro es crucial para que los dueños puedan verificar si coincide con el lugar y tiempo donde perdieron a su mascota.

**Independent Test**: Puede ser testeado ingresando información del encuentro (dónde y cuándo) y verificando que se guarda correctamente con el reporte.

**Acceptance Scenarios**:

1. **Given** un usuario en el formulario de reporte encontrada, **When** ingresa dónde encontró la mascota (dirección o lugar), **Then** ese campo se guarda con el reporte
2. **Given** un usuario en el formulario de reporte encontrada, **When** ingresa cuándo encontró la mascota (fecha), **Then** esa fecha se guarda con el reporte
3. **Given** un usuario que no completa el campo "dónde la encontraste", **When** intenta crear el reporte, **Then** se muestra un mensaje indicando que este campo es requerido
4. **Given** un usuario que no completa el campo "cuándo la encontraste", **When** intenta crear el reporte, **Then** se muestra un mensaje indicando que este campo es requerido

---

### User Story 3 - Diferencia con Reporte Perdida (Priority: P2)

Como usuario, quiero entender que los reportes de mascotas encontradas no requieren nombre de mascota (porque no lo conozco) pero sí requieren información del encuentro.

**Why this priority**: Clarifica las diferencias entre los dos tipos de reportes y asegura que los usuarios proporcionen la información correcta para cada tipo.

**Independent Test**: Puede ser testeado verificando que el formulario de encontrada no tiene campo de nombre pero sí tiene campos de encuentro que el de perdida no tiene.

**Acceptance Scenarios**:

1. **Given** un usuario en el formulario de reporte encontrada, **When** ve el formulario, **Then** no hay campo para nombre de mascota
2. **Given** un usuario en el formulario de reporte encontrada, **When** ve el formulario, **Then** hay campos específicos para "dónde la encontraste" y "cuándo la encontraste" que no están en reportes de perdida
3. **Given** un usuario que crea un reporte encontrada, **When** se guarda, **Then** el campo pet_name se guarda como null en la base de datos

---

### Edge Cases

- ¿Qué sucede cuando el usuario no recuerda exactamente dónde encontró la mascota?
- ¿Cómo maneja el sistema cuando la fecha del encuentro es en el futuro?
- ¿Qué ocurre si el usuario intenta crear un reporte encontrada sin haber encontrado realmente una mascota?
- ¿Cómo se maneja cuando la ubicación del encuentro es muy diferente de la ubicación del reporte (usuario se movió)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE permitir a usuarios autenticados crear reportes de mascotas encontradas
- **FR-002**: El sistema DEBE requerir los siguientes campos obligatorios para crear un reporte encontrada:
  - Especie (perro, gato, ave, conejo, otro)
  - Tamaño (pequeño, mediano, grande)
  - Descripción
  - Dónde se encontró (texto descriptivo)
  - Cuándo se encontró (fecha)
  - Al menos una foto
  - Ubicación (coordenadas GPS)
- **FR-003**: El sistema NO DEBE requerir nombre de mascota para reportes encontradas (se guarda como null)
- **FR-004**: El sistema DEBE permitir campos opcionales:
  - Raza
  - Color
  - Señas particulares
- **FR-005**: El sistema DEBE validar que el campo "dónde la encontraste" no esté vacío
- **FR-006**: El sistema DEBE validar que el campo "cuándo la encontraste" contenga una fecha válida
- **FR-007**: El sistema DEBE establecer la fecha actual como valor por defecto para "cuándo la encontraste" si el usuario no la modifica
- **FR-008**: El sistema DEBE permitir todas las funcionalidades de fotos, ubicación y validación igual que en reportes de perdida
- **FR-009**: El sistema DEBE guardar el tipo de reporte como "found" en la base de datos
- **FR-010**: El sistema DEBE permitir editar reportes encontradas existentes con las mismas restricciones que reportes perdidas

### Key Entities *(include if feature involves data)*

- **Reporte Encontrada**: Representa un reporte de mascota encontrada con información básica (especie, raza, color, tamaño), descripción, señas particulares, fotos, ubicación, información del encuentro (dónde, cuándo), tipo ("found"), estado ("active"), y referencia al usuario creador. El campo pet_name es null.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Los usuarios pueden completar la creación de un reporte encontrada con todos los campos requeridos en menos de 5 minutos
- **SC-002**: El 90% de los usuarios que inician la creación de un reporte encontrada lo completan exitosamente
- **SC-003**: El 100% de los reportes encontradas tienen información del encuentro (dónde y cuándo) completada
- **SC-004**: El 95% de los reportes encontradas tienen al menos una foto asociada
- **SC-005**: El sistema diferencia correctamente entre reportes perdidas y encontradas en el 100% de los casos

