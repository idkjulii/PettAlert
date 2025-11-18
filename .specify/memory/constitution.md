<!--
Sync Impact Report:
Version change: (none) → 1.0.0
Modified principles: N/A (initial version)
Added sections: Core Principles (10 principles), Development Workflow, Governance
Removed sections: N/A
Templates requiring updates:
  ✅ plan-template.md - Constitution Check section aligns with principles
  ✅ spec-template.md - User stories and testable requirements align with principles
  ✅ tasks-template.md - Feature isolation and testing tasks align with principles
  ✅ checklist-template.md - No changes needed (generic template)
  ✅ agent-file-template.md - No changes needed (generic template)
Follow-up TODOs: None
-->

# PetAlert Constitution

## Core Principles

### I. Respeto al Sistema Existente

El sistema actual (Expo/React Native, FastAPI, Supabase, n8n, IA para embeddings/matches) 
es la base operativa. NO se renombrarán ni romperán endpoints, tablas, flujos ni 
contratos que ya funcionan. Las nuevas features deben integrarse sin modificar 
comportamientos existentes, salvo que sea explícitamente requerido y documentado 
como breaking change con migración planificada.

**Rationale**: Mantener estabilidad operativa y evitar regresiones en funcionalidades 
ya desplegadas y utilizadas por usuarios.

### II. Especificaciones Funcionales, No Técnicas

Las especificaciones describen QUÉ debe hacer la feature, no CÓMO implementarla. 
Se evita imponer tecnologías, patrones de diseño o arquitecturas específicas. 
Los equipos de implementación deciden la solución técnica más adecuada dentro 
de las restricciones del sistema existente.

**Rationale**: Permitir flexibilidad técnica mientras se mantiene claridad sobre 
los objetivos funcionales y de negocio.

### III. Claridad y Cero Ambigüedad

Cada requisito dudoso o ambiguo DEBE ser detectado y aclarado ANTES de planear 
o implementar. Las especificaciones deben usar lenguaje declarativo y evitar 
términos vagos. Si un requisito no puede expresarse de forma clara y medible, 
requiere refinamiento antes de proceder.

**Rationale**: Reducir retrabajo, malentendidos y errores de implementación 
causados por interpretaciones incorrectas.

### IV. Compatibilidad de Datos

El modelo actual de Supabase (tablas, relaciones, constraints) y los contratos 
de FastAPI (endpoints, schemas, respuestas) son la fuente de verdad. Las nuevas 
features deben respetar estos modelos. Cualquier extensión del esquema debe 
ser compatible hacia atrás y documentada como migración.

**Rationale**: Garantizar integridad de datos y evitar inconsistencias entre 
componentes del sistema.

### V. Desarrollo por Feature Aislada

Cada nueva funcionalidad se desarrolla en su propia especificación, plan y branch. 
Las features son independientes y pueden implementarse, probarse y desplegarse 
por separado. Las dependencias entre features deben ser explícitas y mínimas.

**Rationale**: Facilitar desarrollo paralelo, testing independiente y despliegues 
incrementales sin bloquear otras features.

### VI. Requisitos Testables

Cada requisito DEBE tener criterios de aceptación claros y medibles. Los criterios 
deben ser verificables mediante pruebas automatizadas o validación manual con 
procedimientos definidos. Los requisitos sin criterios de aceptación no son 
completos y requieren refinamiento.

**Rationale**: Asegurar que las features cumplan expectativas y permitir validación 
objetiva del cumplimiento de requisitos.

### VII. Seguridad y Privacidad

Manejo responsable de datos sensibles: fotos de mascotas, ubicación geográfica, 
datos de contacto y mensajes entre usuarios. Debe cumplirse con principios de 
privacidad por diseño, minimización de datos, consentimiento explícito y protección 
de información personal. Las vulnerabilidades de seguridad deben ser priorizadas 
y resueltas antes del despliegue.

**Rationale**: Proteger la privacidad de usuarios y cumplir con expectativas 
regulatorias y éticas sobre manejo de datos personales.

### VIII. Gobernanza por Versión

Los cambios en principios o reglas de esta Constitución implican incremento de 
versión siguiendo semantic versioning (MAJOR.MINOR.PATCH). MAJOR para cambios 
incompatibles, MINOR para nuevas reglas o principios, PATCH para clarificaciones. 
Cada cambio debe documentarse con fecha y justificación.

**Rationale**: Mantener trazabilidad de evolución de principios y permitir 
adaptación controlada de las reglas de desarrollo.

### IX. Historias de Usuario para Todas las Features

Todas las features existentes y nuevas DEBEN tener historias de usuario documentadas. 
Las historias deben seguir formato estándar (Como [rol], quiero [acción], para 
[beneficio]) y estar priorizadas. Las features sin historias de usuario no están 
completamente especificadas.

**Rationale**: Asegurar que todas las funcionalidades estén alineadas con necesidades 
de usuarios y permitir trazabilidad desde requerimientos hasta implementación.

### X. Pruebas Unitarias para Cada Funcionalidad

Cada funcionalidad existente y nueva DEBE tener pruebas unitarias correspondientes. 
Las pruebas deben cubrir casos de éxito, casos de error y casos límite. La cobertura 
de pruebas debe mantenerse y mejorarse con cada nueva feature. Las funcionalidades 
sin pruebas unitarias requieren creación de pruebas como parte del trabajo de 
extensión del sistema.

**Rationale**: Garantizar calidad del código, facilitar refactorización segura y 
detectar regresiones tempranamente.

## Development Workflow

### Feature Development Process

1. **Especificación**: Crear especificación funcional con historias de usuario, 
   requisitos testables y criterios de aceptación claros.

2. **Planificación**: Desarrollar plan técnico que respete el sistema existente 
   y modele de datos actual.

3. **Branch Aislado**: Crear branch dedicado para la feature siguiendo convención 
   de nombres establecida.

4. **Implementación**: Desarrollar feature con pruebas unitarias desde el inicio, 
   respetando endpoints y esquemas existentes.

5. **Validación**: Verificar cumplimiento de criterios de aceptación y ejecutar 
   suite de pruebas completa.

6. **Integración**: Integrar feature sin romper funcionalidades existentes, 
   validando compatibilidad hacia atrás.

### Code Review Requirements

- Verificar cumplimiento con principios de la Constitución
- Validar que no se rompen contratos existentes (endpoints, tablas, flujos)
- Confirmar presencia de pruebas unitarias para nueva funcionalidad
- Revisar manejo de seguridad y privacidad de datos
- Validar claridad y ausencia de ambigüedades en código y documentación

### Testing Gates

- Pruebas unitarias deben pasar antes de merge
- Pruebas de integración deben validar compatibilidad con sistema existente
- Validación manual de criterios de aceptación para historias de usuario
- Verificación de seguridad para features que manejan datos sensibles

## Governance

Esta Constitución rige todos los procesos de desarrollo y extensión del sistema 
PetAlert. Supersede prácticas ad-hoc y debe ser consultada antes de tomar decisiones 
arquitectónicas o de diseño que afecten múltiples features.

**Amendment Procedure**: 
- Cambios a principios requieren actualización de versión según semantic versioning
- Cambios MAJOR requieren revisión y aprobación explícita
- Cambios MINOR y PATCH pueden proceder con documentación adecuada
- Todos los cambios deben reflejarse en este documento y en templates relacionados

**Compliance Review**: 
- Cada PR debe verificar cumplimiento con principios relevantes
- Features sin historias de usuario o pruebas unitarias no están completas
- Violaciones a principios de compatibilidad o seguridad bloquean merge

**Version**: 1.0.0 | **Ratified**: 2025-10-05 | **Last Amended**: 2025-10-05
