---
description: Crear o actualizar la especificación de feature desde una descripción en lenguaje natural.
handoffs: 
  - label: Build Technical Plan
    agent: speckit.plan
    prompt: Create a plan for the spec. I am building with...
  - label: Clarify Spec Requirements
    agent: speckit.clarify
    prompt: Clarify specification requirements
    send: true
---

## Entrada del Usuario

```text
$ARGUMENTS
```

**DEBES** considerar la entrada del usuario antes de proceder (si no está vacía).

## Esquema

El texto que el usuario escribió después de `/speckit.specify` en el mensaje que activó el comando **es** la descripción de la feature. Asume que siempre la tienes disponible en esta conversación incluso si `$ARGUMENTS` aparece literalmente abajo. No pidas al usuario que la repita a menos que haya proporcionado un comando vacío.

Dada esa descripción de feature, haz lo siguiente:

1. **Generar un nombre corto conciso** (2-4 palabras) para la rama:
   - Analiza la descripción de la feature y extrae las palabras clave más significativas
   - Crea un nombre corto de 2-4 palabras que capture la esencia de la feature
   - Usa formato acción-sustantivo cuando sea posible (ej: "add-user-auth", "fix-payment-bug")
   - Preserva términos técnicos y acrónimos (OAuth2, API, JWT, etc.)
   - Manténlo conciso pero lo suficientemente descriptivo para entender la feature de un vistazo
   - Ejemplos:
     - "Quiero agregar autenticación de usuario" → "user-auth"
     - "Implementar integración OAuth2 para la API" → "oauth2-api-integration"
     - "Crear un dashboard para analytics" → "analytics-dashboard"
     - "Corregir bug de timeout en procesamiento de pagos" → "fix-payment-timeout"

2. **Verificar ramas existentes antes de crear una nueva**:
   
   a. Primero, obtén todas las ramas remotas para asegurar que tenemos la información más reciente:
      ```bash
      git fetch --all --prune
      ```
   
   b. Encuentra el número de feature más alto en todas las fuentes para el nombre corto:
      - Ramas remotas: `git ls-remote --heads origin | grep -E 'refs/heads/[0-9]+-<short-name>$'`
      - Ramas locales: `git branch | grep -E '^[* ]*[0-9]+-<short-name>$'`
      - Directorios de specs: Verifica directorios que coincidan con `specs/[0-9]+-<short-name>`
   
   c. Determina el siguiente número disponible:
      - Extrae todos los números de las tres fuentes
      - Encuentra el número más alto N
      - Usa N+1 para el número de la nueva rama
   
   d. Ejecuta el script `.specify/scripts/powershell/create-new-feature.ps1 -Json "$ARGUMENTS"` con el número calculado y el nombre corto:
      - Pasa `--number N+1` y `--short-name "your-short-name"` junto con la descripción de la feature
      - Ejemplo Bash: `.specify/scripts/powershell/create-new-feature.ps1 -Json "$ARGUMENTS" --json --number 5 --short-name "user-auth" "Add user authentication"`
      - Ejemplo PowerShell: `.specify/scripts/powershell/create-new-feature.ps1 -Json "$ARGUMENTS" -Json -Number 5 -ShortName "user-auth" "Add user authentication"`
   
   **IMPORTANTE**:
   - Verifica las tres fuentes (ramas remotas, ramas locales, directorios de specs) para encontrar el número más alto
   - Solo coincide con ramas/directorios con el patrón exacto del nombre corto
   - Si no se encuentran ramas/directorios existentes con este nombre corto, comienza con el número 1
   - Solo debes ejecutar este script una vez por feature
   - El JSON se proporciona en la terminal como salida - siempre refiérete a él para obtener el contenido real que buscas
   - La salida JSON contendrá BRANCH_NAME y rutas SPEC_FILE
   - Para comillas simples en args como "I'm Groot", usa sintaxis de escape: ej. 'I'\''m Groot' (o comillas dobles si es posible: "I'm Groot")

3. Cargar `.specify/templates/spec-template.md` para entender las secciones requeridas.

4. Seguir este flujo de ejecución:

    1. Analizar la descripción del usuario desde la Entrada
       Si está vacía: ERROR "No se proporcionó descripción de feature"
    2. Extraer conceptos clave de la descripción
       Identificar: actores, acciones, datos, restricciones
    3. Para aspectos poco claros:
       - Haz suposiciones informadas basadas en contexto y estándares de la industria
       - Solo marca con [NEEDS CLARIFICATION: pregunta específica] si:
         - La elección impacta significativamente el alcance de la feature o la experiencia del usuario
         - Existen múltiples interpretaciones razonables con diferentes implicaciones
         - No existe un valor por defecto razonable
       - **LÍMITE: Máximo 3 marcadores [NEEDS CLARIFICATION] en total**
       - Prioriza clarificaciones por impacto: alcance > seguridad/privacidad > experiencia de usuario > detalles técnicos
    4. Llenar la sección User Scenarios & Testing
       Si no hay flujo de usuario claro: ERROR "No se pueden determinar escenarios de usuario"
    5. Generar Requisitos Funcionales
       Cada requisito debe ser testeable
       Usa valores por defecto razonables para detalles no especificados (documenta suposiciones en la sección Assumptions)
    6. Definir Criterios de Éxito
       Crea resultados medibles y agnósticos a la tecnología
       Incluye métricas cuantitativas (tiempo, rendimiento, volumen) y medidas cualitativas (satisfacción del usuario, completitud de tareas)
       Cada criterio debe ser verificable sin detalles de implementación
    7. Identificar Entidades Clave (si hay datos involucrados)
    8. Retornar: ÉXITO (spec lista para planificación)

5. Escribir la especificación en SPEC_FILE usando la estructura del template, reemplazando placeholders con detalles concretos derivados de la descripción de la feature (argumentos) mientras preservas el orden de secciones y encabezados.

6. **Validación de Calidad de Especificación**: Después de escribir la spec inicial, valídala contra criterios de calidad:

   a. **Crear Checklist de Calidad de Spec**: Genera un archivo de checklist en `FEATURE_DIR/checklists/requirements.md` usando la estructura del template de checklist con estos elementos de validación:

      ```markdown
      # Checklist de Calidad de Especificación: [NOMBRE DE FEATURE]
      
      **Propósito**: Validar completitud y calidad de la especificación antes de proceder a la planificación
      **Creado**: [FECHA]
      **Feature**: [Enlace a spec.md]
      
      ## Calidad de Contenido
      
      - [ ] Sin detalles de implementación (lenguajes, frameworks, APIs)
      - [ ] Enfocado en valor de usuario y necesidades de negocio
      - [ ] Escrito para stakeholders no técnicos
      - [ ] Todas las secciones obligatorias completadas
      
      ## Completitud de Requisitos
      
      - [ ] No quedan marcadores [NEEDS CLARIFICATION]
      - [ ] Los requisitos son testeables y no ambiguos
      - [ ] Los criterios de éxito son medibles
      - [ ] Los criterios de éxito son agnósticos a la tecnología (sin detalles de implementación)
      - [ ] Todos los escenarios de aceptación están definidos
      - [ ] Los casos límite están identificados
      - [ ] El alcance está claramente delimitado
      - [ ] Dependencias y suposiciones identificadas
      
      ## Preparación de Feature
      
      - [ ] Todos los requisitos funcionales tienen criterios de aceptación claros
      - [ ] Los escenarios de usuario cubren flujos principales
      - [ ] La feature cumple con resultados medibles definidos en Criterios de Éxito
      - [ ] No hay filtraciones de detalles de implementación en la especificación
      
      ## Notas
      
      - Los elementos marcados como incompletos requieren actualizaciones de spec antes de `/speckit.clarify` o `/speckit.plan`
      ```

   b. **Ejecutar Verificación de Validación**: Revisa la spec contra cada elemento del checklist:
      - Para cada elemento, determina si pasa o falla
      - Documenta problemas específicos encontrados (cita secciones relevantes de la spec)

   c. **Manejar Resultados de Validación**:

      - **Si todos los elementos pasan**: Marca el checklist como completo y procede al paso 6

      - **Si elementos fallan (excluyendo [NEEDS CLARIFICATION])**:
        1. Lista los elementos que fallan y problemas específicos
        2. Actualiza la spec para abordar cada problema
        3. Re-ejecuta la validación hasta que todos los elementos pasen (máximo 3 iteraciones)
        4. Si aún falla después de 3 iteraciones, documenta problemas restantes en notas del checklist y advierte al usuario

      - **Si quedan marcadores [NEEDS CLARIFICATION]**:
        1. Extrae todos los marcadores [NEEDS CLARIFICATION: ...] de la spec
        2. **VERIFICACIÓN DE LÍMITE**: Si existen más de 3 marcadores, mantén solo los 3 más críticos (por impacto de alcance/seguridad/UX) y haz suposiciones informadas para el resto
        3. Para cada clarificación necesaria (máx 3), presenta opciones al usuario en este formato:

           ```markdown
           ## Pregunta [N]: [Tema]
           
           **Contexto**: [Cita sección relevante de la spec]
           
           **Lo que necesitamos saber**: [Pregunta específica del marcador NEEDS CLARIFICATION]
           
           **Respuestas Sugeridas**:
           
           | Opción | Respuesta | Implicaciones |
           |--------|-----------|---------------|
           | A      | [Primera respuesta sugerida] | [Qué significa esto para la feature] |
           | B      | [Segunda respuesta sugerida] | [Qué significa esto para la feature] |
           | C      | [Tercera respuesta sugerida] | [Qué significa esto para la feature] |
           | Custom | Proporciona tu propia respuesta | [Explica cómo proporcionar entrada personalizada] |
           
           **Tu elección**: _[Esperar respuesta del usuario]_
           ```

        4. **CRÍTICO - Formato de Tabla**: Asegúrate de que las tablas markdown estén correctamente formateadas:
           - Usa espaciado consistente con pipes alineados
           - Cada celda debe tener espacios alrededor del contenido: `| Contenido |` no `|Contenido|`
           - El separador de encabezado debe tener al menos 3 guiones: `|--------|`
           - Verifica que la tabla se renderice correctamente en la vista previa de markdown
        5. Numera las preguntas secuencialmente (P1, P2, P3 - máx 3 en total)
        6. Presenta todas las preguntas juntas antes de esperar respuestas
        7. Espera a que el usuario responda con sus elecciones para todas las preguntas (ej: "P1: A, P2: Custom - [detalles], P3: B")
        8. Actualiza la spec reemplazando cada marcador [NEEDS CLARIFICATION] con la respuesta seleccionada o proporcionada por el usuario
        9. Re-ejecuta la validación después de que todas las clarificaciones se resuelvan

   d. **Actualizar Checklist**: Después de cada iteración de validación, actualiza el archivo del checklist con el estado actual de pasar/fallar

7. Reportar completitud con nombre de rama, ruta del archivo spec, resultados del checklist, y preparación para la siguiente fase (`/speckit.clarify` o `/speckit.plan`).

**NOTA:** El script crea y hace checkout de la nueva rama e inicializa el archivo spec antes de escribir.

## Guías Generales

## Guías Rápidas

- Enfócate en **QUÉ** necesitan los usuarios y **POR QUÉ**.
- Evita CÓMO implementar (sin stack tecnológico, APIs, estructura de código).
- Escrito para stakeholders de negocio, no desarrolladores.
- NO crees ningún checklist que esté embebido en la spec. Eso será un comando separado.

### Requisitos de Sección

- **Secciones obligatorias**: Deben completarse para cada feature
- **Secciones opcionales**: Incluir solo cuando sean relevantes para la feature
- Cuando una sección no aplica, elimínala completamente (no la dejes como "N/A")

### Para Generación por IA

Cuando crees esta spec desde un prompt del usuario:

1. **Haz suposiciones informadas**: Usa contexto, estándares de la industria y patrones comunes para llenar vacíos
2. **Documenta suposiciones**: Registra valores por defecto razonables en la sección Assumptions
3. **Limita clarificaciones**: Máximo 3 marcadores [NEEDS CLARIFICATION] - usa solo para decisiones críticas que:
   - Impacten significativamente el alcance de la feature o la experiencia del usuario
   - Tengan múltiples interpretaciones razonables con diferentes implicaciones
   - Carezcan de cualquier valor por defecto razonable
4. **Prioriza clarificaciones**: alcance > seguridad/privacidad > experiencia de usuario > detalles técnicos
5. **Piensa como un tester**: Cada requisito vago debe fallar el elemento del checklist "testeable y no ambiguo"
6. **Áreas comunes que necesitan clarificación** (solo si no existe un valor por defecto razonable):
   - Alcance de la feature y límites (incluir/excluir casos de uso específicos)
   - Tipos de usuario y permisos (si múltiples interpretaciones conflictivas son posibles)
   - Requisitos de seguridad/cumplimiento (cuando sean legal o financieramente significativos)

**Ejemplos de valores por defecto razonables** (no preguntes sobre estos):

- Retención de datos: Prácticas estándar de la industria para el dominio
- Objetivos de rendimiento: Expectativas estándar de apps web/móviles a menos que se especifique
- Manejo de errores: Mensajes amigables al usuario con fallbacks apropiados
- Método de autenticación: Basado en sesión estándar u OAuth2 para apps web
- Patrones de integración: APIs RESTful a menos que se especifique lo contrario

### Guías de Criterios de Éxito

Los criterios de éxito deben ser:

1. **Medibles**: Incluir métricas específicas (tiempo, porcentaje, conteo, tasa)
2. **Agnósticos a la tecnología**: Sin mención de frameworks, lenguajes, bases de datos o herramientas
3. **Enfocados en el usuario**: Describir resultados desde la perspectiva del usuario/negocio, no internos del sistema
4. **Verificables**: Pueden ser probados/validados sin conocer detalles de implementación

**Buenos ejemplos**:

- "Los usuarios pueden completar el checkout en menos de 3 minutos"
- "El sistema soporta 10,000 usuarios concurrentes"
- "95% de las búsquedas retornan resultados en menos de 1 segundo"
- "La tasa de completitud de tareas mejora en 40%"

**Malos ejemplos** (enfocados en implementación):

- "El tiempo de respuesta de la API es menor a 200ms" (demasiado técnico, usa "Los usuarios ven resultados instantáneamente")
- "La base de datos puede manejar 1000 TPS" (detalle de implementación, usa métrica orientada al usuario)
- "Los componentes React renderizan eficientemente" (específico del framework)
- "La tasa de aciertos de caché Redis por encima del 80%" (específico de tecnología)
