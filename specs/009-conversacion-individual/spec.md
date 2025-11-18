# Feature Specification: Conversación Individual

**Feature Branch**: `009-conversacion-individual`  
**Created**: 2025-10-05  
**Status**: Implementado (Documentación Retroactiva)  
**Input**: Feature existente - Mensajería en tiempo real entre usuarios sobre reportes de mascotas

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Ver Mensajes de la Conversación (Priority: P1)

Como usuario, quiero ver todos los mensajes de una conversación en orden cronológico para seguir el hilo de la conversación sobre un reporte de mascota.

**Why this priority**: Es la funcionalidad principal de la conversación. Sin ver mensajes, no hay comunicación posible.

**Independent Test**: Puede ser testeado completamente abriendo una conversación y verificando que se muestran todos los mensajes correctamente.

**Acceptance Scenarios**:

1. **Given** un usuario que abre una conversación, **When** se carga la pantalla, **Then** ve todos los mensajes de la conversación en orden cronológico (más antiguos arriba, más recientes abajo)
2. **Given** un usuario que ve una conversación, **When** hay mensajes, **Then** cada mensaje muestra:
   - Contenido del mensaje o indicador de imagen
   - Timestamp
   - Indicador visual de si es propio o del otro usuario
3. **Given** un usuario que ve una conversación, **When** se carga, **Then** el scroll se posiciona en el último mensaje (más reciente)

---

### User Story 2 - Enviar Mensajes de Texto (Priority: P1)

Como usuario, quiero poder enviar mensajes de texto al otro usuario para comunicarme sobre el reporte de mascota.

**Why this priority**: Es la forma principal de comunicación. Sin poder enviar mensajes, no hay funcionalidad de chat.

**Independent Test**: Puede ser testeado completamente escribiendo un mensaje, enviándolo y verificando que aparece en la conversación.

**Acceptance Scenarios**:

1. **Given** un usuario en una conversación, **When** escribe un mensaje y presiona enviar, **Then** el mensaje se envía y aparece en la conversación
2. **Given** un usuario que envía un mensaje, **When** se envía exitosamente, **Then** el mensaje aparece marcado como enviado
3. **Given** un usuario que envía un mensaje, **When** el otro usuario lo lee, **Then** el mensaje se marca como leído (si está implementado)
4. **Given** un usuario que intenta enviar un mensaje vacío, **When** presiona enviar, **Then** no se envía el mensaje

---

### User Story 3 - Enviar Imágenes (Priority: P2)

Como usuario, quiero poder enviar fotos en la conversación para compartir imágenes adicionales de la mascota o evidencia.

**Why this priority**: Las imágenes son importantes para identificar mascotas y proporcionar evidencia visual en las conversaciones.

**Independent Test**: Puede ser testeado completamente seleccionando una imagen y verificando que se envía y aparece en la conversación.

**Acceptance Scenarios**:

1. **Given** un usuario en una conversación, **When** selecciona enviar imagen desde galería o cámara, **Then** la imagen se envía y aparece en la conversación
2. **Given** un usuario que envía una imagen, **When** se envía exitosamente, **Then** se muestra una miniatura o indicador de imagen en la conversación
3. **Given** un usuario que ve una imagen recibida, **When** toca la imagen, **Then** puede verla en tamaño completo (si está implementado)

---

### User Story 4 - Actualización en Tiempo Real (Priority: P2)

Como usuario, quiero recibir nuevos mensajes automáticamente sin tener que refrescar la pantalla para tener conversaciones fluidas.

**Why this priority**: Mejora significativamente la experiencia de usuario al hacer las conversaciones más naturales y fluidas.

**Independent Test**: Puede ser testeado completamente enviando un mensaje desde otro dispositivo y verificando que aparece automáticamente.

**Acceptance Scenarios**:

1. **Given** un usuario en una conversación, **When** el otro usuario envía un mensaje, **Then** el mensaje aparece automáticamente en la conversación
2. **Given** un usuario que recibe un nuevo mensaje, **When** está viendo la conversación, **Then** el scroll se ajusta para mostrar el nuevo mensaje
3. **Given** un usuario que recibe un nuevo mensaje, **When** no está en la conversación, **Then** se actualiza el badge de no leídos en la lista (si está implementado)

---

### Edge Cases

- ¿Qué sucede cuando el usuario pierde conexión mientras envía un mensaje?
- ¿Cómo maneja el sistema cuando falla el envío de un mensaje?
- ¿Qué ocurre si el otro usuario elimina su cuenta durante la conversación?
- ¿Cómo se maneja cuando hay muchos mensajes (más de 1000)?
- ¿Qué sucede si el usuario cierra la aplicación mientras está en una conversación?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: El sistema DEBE mostrar todos los mensajes de una conversación en orden cronológico
- **FR-002**: El sistema DEBE diferenciar visualmente mensajes propios de mensajes del otro usuario
- **FR-003**: El sistema DEBE mostrar timestamps para cada mensaje
- **FR-004**: El sistema DEBE posicionar el scroll en el último mensaje al cargar la conversación
- **FR-005**: El sistema DEBE permitir enviar mensajes de texto
- **FR-006**: El sistema DEBE validar que los mensajes no estén vacíos antes de enviar
- **FR-007**: El sistema DEBE mostrar indicadores de estado para mensajes enviados (enviado, leído)
- **FR-008**: El sistema DEBE permitir enviar imágenes desde galería o cámara
- **FR-009**: El sistema DEBE mostrar imágenes enviadas/recibidas en la conversación
- **FR-010**: El sistema DEBE actualizar la conversación cuando se reciben nuevos mensajes (si está implementado)
- **FR-011**: El sistema DEBE manejar errores de envío mostrando mensajes apropiados
- **FR-012**: El sistema DEBE mostrar indicadores de carga durante el envío de mensajes
- **FR-013**: El sistema DEBE permitir scroll para ver mensajes anteriores
- **FR-014**: El sistema DEBE manejar casos cuando no hay mensajes mostrando un estado vacío apropiado

### Key Entities *(include if feature involves data)*

- **Mensaje**: Representa un mensaje individual en una conversación con contenido (texto o imagen), timestamp, remitente, y estado (enviado, leído)
- **Conversación Individual**: Representa el hilo completo de mensajes entre dos usuarios específicos

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Los mensajes se cargan y muestran en menos de 2 segundos después de abrir la conversación
- **SC-002**: Los usuarios pueden enviar un mensaje de texto en menos de 3 segundos desde que escriben hasta que se envía
- **SC-003**: Las imágenes se envían y aparecen en la conversación en menos de 5 segundos (para conexiones normales)
- **SC-004**: El sistema maneja correctamente conversaciones con hasta 500 mensajes sin degradación de rendimiento
- **SC-005**: Los nuevos mensajes aparecen automáticamente en menos de 2 segundos después de ser enviados (si está implementado)
- **SC-006**: El 95% de los mensajes se envían exitosamente en el primer intento
- **SC-007**: Los usuarios pueden seguir una conversación completa sin necesidad de refrescar manualmente

