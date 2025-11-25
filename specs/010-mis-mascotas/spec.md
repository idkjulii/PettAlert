# Feature Specification: Mis Mascotas - Módulo de Seguimiento Veterinario & Salud

**Feature Branch**: `010-mis-mascotas`  
**Created**: 2025-10-05  
**Updated**: 2025-01-XX  
**Status**: Implementado - Módulo Completo de Salud Veterinaria  
**Input**: Sistema completo de seguimiento de salud de mascotas con historial médico, vacunaciones, medicamentos, indicadores de bienestar y recordatorios

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver Lista de Mis Mascotas (Priority: P1)

Como usuario autenticado, quiero ver una lista de todas las mascotas que he registrado para tener un resumen de mis mascotas en la aplicación.

**Why this priority**: Proporciona una vista centralizada de las mascotas del usuario, facilitando la gestión y referencia rápida.

**Independent Test**: Puede ser testeado completamente cargando la pantalla y verificando que se muestran todas las mascotas del usuario.

**Acceptance Scenarios**:

1. **Given** un usuario autenticado con mascotas registradas, **When** accede a "Mis Mascotas", **Then** ve una lista de todas sus mascotas
2. **Given** un usuario autenticado sin mascotas, **When** accede a "Mis Mascotas", **Then** ve un mensaje indicando que no tiene mascotas registradas aún
3. **Given** un usuario autenticado, **When** ve la lista de mascotas, **Then** cada mascota muestra:
   - Nombre
   - Especie (perro/gato/otro)
   - Raza
   - Tamaño
   - Color
   - Fecha de registro
   - Indicador si está perdida

---

### User Story 2 - Ver Detalles de Mascota con Seguimiento de Salud (Priority: P1)

Como usuario, quiero ver información detallada de cada mascota con su historial de salud completo para llevar un seguimiento veterinario activo.

**Why this priority**: Permite a los usuarios gestionar la salud de sus mascotas de forma integral, no solo ver información básica.

**Independent Test**: Puede ser testeado completamente verificando que cada mascota muestra toda su información y datos de salud.

**Acceptance Scenarios**:

1. **Given** un usuario que ve sus mascotas, **When** toca una mascota en la lista, **Then** navega a la pantalla de detalle con pestañas (Información, Salud, Bienestar, Recordatorios)
2. **Given** un usuario en el detalle de mascota, **When** ve la pestaña "Información", **Then** puede ver todos los datos básicos (nombre, especie, raza, tamaño, color, descripción, señales particulares)
3. **Given** un usuario en el detalle de mascota, **When** ve la pestaña "Salud", **Then** puede ver:
   - Resumen de salud (último peso, próxima vacuna, medicamentos activos, recordatorios pendientes)
   - Lista de vacunaciones y tratamientos con fechas
   - Medicamentos activos con dosis y frecuencia
   - Historial reciente de eventos médicos
4. **Given** un usuario en el detalle de mascota, **When** ve la pestaña "Bienestar", **Then** puede ver indicadores de:
   - Peso a lo largo del tiempo
   - Actividad (minutos/pasos)
   - Horas de descanso
   - Temperatura (si está registrada)
5. **Given** un usuario en el detalle de mascota, **When** ve la pestaña "Recordatorios", **Then** puede ver:
   - Recordatorios pendientes ordenados por fecha
   - Recordatorios completados
   - Opción para marcar recordatorios como completados
6. **Given** un usuario que ve una mascota, **When** la mascota está marcada como perdida, **Then** se muestra un indicador visual destacado "⚠️ MASCOTA PERDIDA"

---

### User Story 3 - Registrar Eventos de Salud (Priority: P1)

Como usuario, quiero registrar eventos médicos de mi mascota (enfermedades, cirugías, alergias, chequeos) para mantener un historial médico completo.

**Why this priority**: Es fundamental para el seguimiento de la salud de la mascota a lo largo del tiempo.

**Acceptance Scenarios**:

1. **Given** un usuario en la pestaña "Salud" de una mascota, **When** presiona el botón para agregar evento, **Then** puede registrar:
   - Tipo de evento (enfermedad, cirugía, alergia, chequeo, otro)
   - Fecha del evento
   - Descripción
   - Veterinario (opcional)
   - Notas adicionales
   - Costo (opcional)
2. **Given** un usuario que registra un evento de salud, **When** guarda el evento, **Then** aparece en el historial reciente
3. **Given** un usuario que ve el historial de salud, **When** hay múltiples eventos, **Then** están ordenados por fecha (más recientes primero)

---

### User Story 4 - Gestionar Vacunaciones y Tratamientos (Priority: P1)

Como usuario, quiero registrar y gestionar las vacunaciones y tratamientos de mi mascota para asegurar que esté al día con su calendario de vacunación.

**Why this priority**: Las vacunaciones son críticas para la salud preventiva de las mascotas.

**Acceptance Scenarios**:

1. **Given** un usuario en la pestaña "Salud", **When** ve la sección de vacunaciones, **Then** puede ver todas las vacunas registradas con:
   - Nombre de la vacuna/tratamiento
   - Tipo (vacuna, tratamiento, desparasitación, antiparasitario)
   - Fecha de inicio
   - Próxima fecha (si aplica)
   - Dosis y frecuencia
   - Observaciones
2. **Given** un usuario que quiere agregar una vacunación, **When** completa el formulario, **Then** puede especificar:
   - Tipo de vacunación/tratamiento
   - Nombre
   - Fecha de inicio
   - Fecha final (opcional)
   - Próxima fecha (para recordatorios automáticos)
   - Dosis y frecuencia
   - Observaciones
3. **Given** un usuario que tiene vacunaciones registradas, **When** hay una próxima vacuna programada, **Then** aparece en el resumen de salud

---

### User Story 5 - Gestionar Medicamentos Activos (Priority: P1)

Como usuario, quiero registrar y gestionar los medicamentos que mi mascota está tomando actualmente para llevar un control de tratamientos activos.

**Why this priority**: Es importante para evitar interacciones medicamentosas y asegurar el cumplimiento del tratamiento.

**Acceptance Scenarios**:

1. **Given** un usuario en la pestaña "Salud", **When** ve la sección de medicamentos activos, **Then** puede ver:
   - Nombre del medicamento
   - Dosis
   - Frecuencia
   - Fecha de inicio
   - Fecha de fin (si aplica)
   - Motivo del tratamiento
   - Veterinario que lo prescribió
2. **Given** un usuario que quiere agregar un medicamento, **When** completa el formulario, **Then** puede especificar todos los datos requeridos
3. **Given** un usuario que tiene medicamentos activos, **When** finaliza un tratamiento, **Then** puede marcar el medicamento como inactivo
4. **Given** un usuario que ve el resumen de salud, **When** hay medicamentos activos, **Then** se muestra el conteo en el resumen

---

### User Story 6 - Registrar Indicadores de Bienestar (Priority: P2)

Como usuario, quiero registrar métricas de bienestar de mi mascota (peso, actividad, horas de descanso) para monitorear su salud a lo largo del tiempo.

**Why this priority**: Permite detectar cambios en la salud de la mascota mediante el seguimiento de métricas clave.

**Acceptance Scenarios**:

1. **Given** un usuario en la pestaña "Bienestar", **When** ve los indicadores, **Then** puede ver un historial de:
   - Peso (en kg)
   - Altura (en cm, opcional)
   - Actividad (minutos o pasos)
   - Horas de descanso
   - Temperatura (opcional)
   - Fecha de registro
   - Notas adicionales
2. **Given** un usuario que quiere agregar un indicador, **When** completa el formulario, **Then** puede registrar al menos el peso y la fecha
3. **Given** un usuario que tiene múltiples registros de peso, **When** ve el historial, **Then** puede identificar tendencias (aumento/disminución de peso)
4. **Given** un usuario que ve el resumen de salud, **When** hay un peso registrado recientemente, **Then** aparece en el resumen con la fecha

---

### User Story 7 - Gestionar Recordatorios (Priority: P1)

Como usuario, quiero crear y gestionar recordatorios para vacunas, chequeos, medicamentos y otros eventos importantes relacionados con la salud de mi mascota.

**Why this priority**: Los recordatorios ayudan a los usuarios a mantener el calendario de salud de sus mascotas al día.

**Acceptance Scenarios**:

1. **Given** un usuario en la pestaña "Recordatorios", **When** ve los recordatorios, **Then** puede ver:
   - Recordatorios pendientes ordenados por fecha
   - Recordatorios completados
   - Tipo de recordatorio (vacuna, chequeo, medicamento, desparasitación, otro)
   - Título y descripción
   - Fecha y hora programada
   - Estado (pendiente/completado)
2. **Given** un usuario que quiere crear un recordatorio, **When** completa el formulario, **Then** puede especificar:
   - Tipo de recordatorio
   - Título
   - Descripción (opcional)
   - Fecha programada
   - Hora programada (opcional)
   - Repetición (una vez, diario, semanal, mensual, anual)
3. **Given** un usuario que tiene recordatorios pendientes, **When** completa un recordatorio, **Then** se marca como completado con fecha y hora
4. **Given** un usuario que ve el resumen de salud, **When** hay recordatorios pendientes, **Then** se muestra el conteo en el resumen

---

### User Story 8 - Gestionar Documentos Médicos (Priority: P2)

Como usuario, quiero subir y gestionar documentos médicos de mi mascota (certificados de vacunación, exámenes, recetas) para tener acceso rápido a esta información.

**Why this priority**: Los documentos médicos son importantes para consultas veterinarias y para mantener un registro completo.

**Acceptance Scenarios**:

1. **Given** un usuario en el detalle de mascota, **When** accede a documentos médicos, **Then** puede ver:
   - Lista de documentos ordenados por fecha
   - Tipo de documento (certificado, examen, receta, radiografía, análisis, otro)
   - Nombre del documento
   - Fecha del documento
   - Veterinario (si está registrado)
   - Descripción
2. **Given** un usuario que quiere agregar un documento, **When** sube un archivo, **Then** puede especificar:
   - Tipo de documento
   - Nombre
   - Archivo (imagen o PDF)
   - Fecha del documento
   - Veterinario (opcional)
   - Descripción (opcional)
3. **Given** un usuario que tiene documentos médicos, **When** toca un documento, **Then** puede verlo o descargarlo

---

### User Story 9 - Planes de Cuidado Personalizados (Priority: P3)

Como usuario, quiero crear y gestionar planes de cuidado personalizados para mi mascota según su edad, especie y raza.

**Why this priority**: Los planes de cuidado ayudan a los usuarios a seguir un programa estructurado de salud preventiva.

**Acceptance Scenarios**:

1. **Given** un usuario que quiere crear un plan de cuidado, **When** completa el formulario, **Then** puede especificar:
   - Nombre del plan
   - Descripción
   - Tipo de plan (preventivo, tratamiento, recuperación, mantenimiento)
   - Fecha de inicio
   - Fecha de fin (opcional)
   - Items del checklist
2. **Given** un usuario que tiene un plan de cuidado activo, **When** ve el plan, **Then** puede ver:
   - Porcentaje de cumplimiento
   - Items del checklist con estado (completado/pendiente)
   - Fechas objetivo para cada item
3. **Given** un usuario que completa un item del checklist, **When** lo marca como completado, **Then** se actualiza el porcentaje de cumplimiento del plan

---

### Edge Cases

- ¿Qué sucede cuando el usuario tiene muchas mascotas registradas (más de 50)?
- ¿Cómo maneja el sistema cuando falla la carga de mascotas?
- ¿Qué ocurre si una mascota fue eliminada mientras el usuario está viendo la lista?
- ¿Cómo se maneja cuando no hay conexión a internet?
- ¿Qué sucede cuando hay muchos eventos de salud registrados (más de 100)?
- ¿Cómo se maneja cuando una fecha de recordatorio es en el pasado?
- ¿Qué ocurre si se intenta registrar un peso negativo o valores inválidos?
- ¿Cómo se valida que las fechas de vacunación sean lógicas (fecha final después de fecha inicial)?
- ¿Qué sucede cuando se intenta subir un documento médico muy grande?
- ¿Cómo se maneja cuando hay múltiples recordatorios para la misma fecha?

## Requirements *(mandatory)*

### Functional Requirements

#### Visualización de Mascotas
- **FR-001**: El sistema DEBE mostrar una lista de todas las mascotas registradas por el usuario autenticado
- **FR-002**: El sistema DEBE mostrar para cada mascota en la lista:
  - Foto principal (si está disponible)
  - Nombre (o "Sin nombre" si no tiene)
  - Especie traducida (Perro/Gato/Otro)
  - Raza (o "Raza no especificada" si no tiene)
  - Tamaño traducido (Pequeño/Mediano/Grande)
  - Color (o "No especificado" si no tiene)
  - Fecha de registro formateada
  - Indicador visual si está perdida
  - Botón para ver detalles y salud
- **FR-003**: El sistema DEBE mostrar un indicador destacado "⚠️ MASCOTA PERDIDA" cuando is_lost es true
- **FR-004**: El sistema DEBE mostrar un estado vacío cuando el usuario no tiene mascotas registradas
- **FR-005**: El sistema DEBE mostrar un mensaje indicando que puede registrar su primera mascota
- **FR-006**: El sistema DEBE mostrar indicadores de carga durante la carga inicial
- **FR-007**: El sistema DEBE manejar errores mostrando mensajes apropiados

#### Detalle de Mascota
- **FR-008**: El sistema DEBE permitir navegar al detalle de una mascota desde la lista
- **FR-009**: El sistema DEBE mostrar el detalle de mascota con pestañas: Información, Salud, Bienestar, Recordatorios
- **FR-010**: El sistema DEBE mostrar en la pestaña "Información":
  - Foto principal de la mascota
  - Todos los datos básicos (nombre, especie, raza, tamaño, color, descripción, señales particulares)
- **FR-011**: El sistema DEBE mostrar en la pestaña "Salud":
  - Resumen de salud con último peso, próxima vacuna, medicamentos activos, recordatorios pendientes
  - Lista de vacunaciones y tratamientos
  - Lista de medicamentos activos
  - Historial reciente de eventos médicos (últimos 5)
- **FR-012**: El sistema DEBE mostrar en la pestaña "Bienestar":
  - Historial de indicadores de bienestar (peso, actividad, descanso, temperatura)
  - Ordenados por fecha (más recientes primero)
- **FR-013**: El sistema DEBE mostrar en la pestaña "Recordatorios":
  - Recordatorios pendientes ordenados por fecha
  - Recordatorios completados
  - Opción para marcar como completado

#### Historial de Salud
- **FR-014**: El sistema DEBE permitir registrar eventos de salud (enfermedad, cirugía, alergia, chequeo, otro)
- **FR-015**: El sistema DEBE almacenar para cada evento: fecha, tipo, descripción, veterinario (opcional), notas, costo (opcional)
- **FR-016**: El sistema DEBE mostrar el historial ordenado por fecha (más recientes primero)
- **FR-017**: El sistema DEBE permitir paginación del historial (límite de 50 por página)

#### Vacunaciones y Tratamientos
- **FR-018**: El sistema DEBE permitir registrar vacunaciones y tratamientos
- **FR-019**: El sistema DEBE almacenar para cada vacunación: tipo, nombre, fecha_inicio, fecha_final (opcional), proxima_fecha, dosis, frecuencia, observaciones, veterinario
- **FR-020**: El sistema DEBE mostrar las vacunaciones ordenadas por fecha de inicio (más recientes primero)
- **FR-021**: El sistema DEBE permitir actualizar vacunaciones existentes
- **FR-022**: El sistema DEBE mostrar en el resumen la próxima vacuna programada

#### Medicamentos
- **FR-023**: El sistema DEBE permitir registrar medicamentos activos
- **FR-024**: El sistema DEBE almacenar para cada medicamento: nombre, dosis, frecuencia, fecha_inicio, fecha_fin (opcional), motivo, veterinario, activo
- **FR-025**: El sistema DEBE permitir filtrar medicamentos activos/inactivos
- **FR-026**: El sistema DEBE permitir actualizar medicamentos (incluyendo desactivarlos)
- **FR-027**: El sistema DEBE mostrar el conteo de medicamentos activos en el resumen

#### Indicadores de Bienestar
- **FR-028**: El sistema DEBE permitir registrar indicadores de bienestar
- **FR-029**: El sistema DEBE almacenar para cada indicador: fecha, peso (opcional), altura (opcional), actividad (opcional), horas_descanso (opcional), temperatura (opcional), notas
- **FR-030**: El sistema DEBE mostrar los indicadores ordenados por fecha (más recientes primero)
- **FR-031**: El sistema DEBE mostrar el último peso registrado en el resumen de salud

#### Recordatorios
- **FR-032**: El sistema DEBE permitir crear recordatorios
- **FR-033**: El sistema DEBE almacenar para cada recordatorio: tipo, titulo, descripcion, fecha_programada, hora_programada (opcional), repeticion, cumplido, fecha_cumplido, activo
- **FR-034**: El sistema DEBE permitir filtrar recordatorios activos/pendientes/próximos
- **FR-035**: El sistema DEBE permitir marcar recordatorios como completados
- **FR-036**: El sistema DEBE mostrar el conteo de recordatorios pendientes en el resumen

#### Documentos Médicos
- **FR-037**: El sistema DEBE permitir subir documentos médicos
- **FR-038**: El sistema DEBE almacenar para cada documento: tipo_documento, nombre, archivo_url, descripcion, fecha_documento, veterinario
- **FR-039**: El sistema DEBE mostrar los documentos ordenados por fecha (más recientes primero)
- **FR-040**: El sistema DEBE permitir ver/descargar documentos médicos

#### Planes de Cuidado
- **FR-041**: El sistema DEBE permitir crear planes de cuidado personalizados
- **FR-042**: El sistema DEBE almacenar para cada plan: nombre, descripcion, tipo_plan, fecha_inicio, fecha_fin (opcional), activo, porcentaje_cumplimiento
- **FR-043**: El sistema DEBE permitir agregar items al checklist del plan
- **FR-044**: El sistema DEBE permitir marcar items del checklist como completados
- **FR-045**: El sistema DEBE calcular automáticamente el porcentaje de cumplimiento del plan

### Key Entities *(include if feature involves data)*

- **Mascota (pets)**: Representa una mascota registrada por el usuario con nombre, especie, raza, tamaño, color, descripción, señales particulares, fotos, fecha de registro y estado (is_lost)
- **Historial de Salud (historial_salud)**: Eventos médicos de la mascota (enfermedad, cirugía, alergia, chequeo, otro) con fecha, descripción, veterinario, notas, costo
- **Vacunación/Tratamiento (vacunacion_tratamiento)**: Vacunas y tratamientos con tipo, nombre, fechas, dosis, frecuencia, observaciones
- **Medicamento Activo (medicamentos_activos)**: Medicamentos que está tomando la mascota con nombre, dosis, frecuencia, fechas, motivo, veterinario, estado activo
- **Indicador de Bienestar (indicador_bienestar)**: Métricas de salud (peso, altura, actividad, descanso, temperatura) con fecha y notas
- **Recordatorio (recordatorio)**: Recordatorios de vacunas, chequeos, medicamentos con tipo, título, descripción, fecha/hora programada, repetición, estado cumplido
- **Documento Médico (documento_medico)**: Documentos médicos (certificados, exámenes, recetas) con tipo, nombre, archivo_url, fecha, veterinario
- **Plan de Cuidado (plan_cuidado)**: Planes personalizados de cuidado con nombre, descripción, tipo, fechas, porcentaje de cumplimiento
- **Checklist de Cuidado (checklist_cuidado)**: Items del plan de cuidado con descripción, fecha objetivo, estado completado

## Success Criteria *(mandatory)*

### Measurable Outcomes

#### Rendimiento
- **SC-001**: La lista de mascotas se carga en menos de 2 segundos después de abrir la pantalla
- **SC-002**: El detalle de mascota con resumen de salud se carga en menos de 3 segundos
- **SC-003**: El sistema maneja correctamente listas de hasta 100 mascotas sin degradación de rendimiento
- **SC-004**: El historial de salud se carga en menos de 2 segundos (paginado a 50 registros)

#### Funcionalidad
- **SC-005**: El 100% de las mascotas registradas del usuario se muestran correctamente en la lista
- **SC-006**: El 100% de los eventos de salud registrados se muestran en el historial
- **SC-007**: El resumen de salud muestra correctamente el último peso, próxima vacuna, medicamentos activos y recordatorios pendientes
- **SC-008**: Los recordatorios pendientes se muestran ordenados por fecha (próximos primero)
- **SC-009**: Los usuarios pueden registrar eventos de salud, vacunaciones, medicamentos e indicadores de bienestar sin errores

#### Usabilidad
- **SC-010**: Los usuarios pueden navegar entre pestañas sin pérdida de datos
- **SC-011**: Los usuarios pueden refrescar los datos con pull-to-refresh
- **SC-012**: Los formularios validan correctamente los datos antes de guardar
- **SC-013**: Los mensajes de error son claros y accionables

#### Integridad de Datos
- **SC-014**: Todos los datos de salud se guardan correctamente en la base de datos
- **SC-015**: Las relaciones entre mascotas y sus datos de salud se mantienen correctamente (CASCADE)
- **SC-016**: Los cálculos de resumen de salud son precisos (último peso, conteos, etc.)

## Arquitectura Técnica

### Backend
- **Router**: `backend/routers/pets.py`
- **Endpoints principales**:
  - `GET /pets/` - Lista de mascotas del usuario
  - `GET /pets/{pet_id}` - Detalle de mascota con resumen de salud
  - `GET /pets/{pet_id}/health-history` - Historial de salud
  - `POST /pets/{pet_id}/health-history` - Agregar evento de salud
  - `GET /pets/{pet_id}/vaccinations` - Vacunaciones
  - `POST /pets/{pet_id}/vaccinations` - Agregar vacunación
  - `GET /pets/{pet_id}/medications` - Medicamentos
  - `POST /pets/{pet_id}/medications` - Agregar medicamento
  - `GET /pets/{pet_id}/wellness` - Indicadores de bienestar
  - `POST /pets/{pet_id}/wellness` - Agregar indicador
  - `GET /pets/{pet_id}/reminders` - Recordatorios
  - `POST /pets/{pet_id}/reminders` - Crear recordatorio
  - `PUT /pets/reminders/{reminder_id}/complete` - Completar recordatorio
  - `GET /pets/{pet_id}/documents` - Documentos médicos
  - `POST /pets/{pet_id}/documents` - Subir documento
  - `GET /pets/{pet_id}/care-plans` - Planes de cuidado
  - `POST /pets/{pet_id}/care-plans` - Crear plan

### Base de Datos
- **Migración**: `backend/migrations/007_pet_health_tracking.sql`
- **Tablas**: historial_salud, vacunacion_tratamiento, medicamentos_activos, indicador_bienestar, recordatorio, documento_medico, plan_cuidado, checklist_cuidado
- **Función SQL**: `obtener_resumen_salud_mascota(pet_id)` - Calcula resumen de salud
- **Políticas RLS**: Todas las tablas tienen RLS habilitado con políticas para que los usuarios solo vean/gestionen sus propias mascotas

### Frontend
- **Componente principal**: `app/(tabs)/pets.jsx` - Lista de mascotas
- **Componente detalle**: `app/pets/[petId].jsx` - Detalle con pestañas
- **Servicios**: `src/services/supabase.js` - Funciones del petService extendidas
- **Navegación**: Expo Router con rutas dinámicas

## Notas de Implementación

- El sistema usa el backend API para todas las operaciones de salud (no Supabase directo)
- Los datos básicos de mascotas siguen usando Supabase directo para mantener compatibilidad
- El resumen de salud se calcula usando una función SQL para mejor rendimiento
- Los formularios de entrada de datos están referenciados pero pueden ser implementados como pantallas separadas o modales
- El sistema está preparado para notificaciones push de recordatorios (pendiente de implementar)

