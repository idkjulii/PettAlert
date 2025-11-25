# 📋 Instrucciones para Finalizar el Capítulo XIII

## ✅ Lo que YA está hecho

- ✅ Estructura completa del capítulo
- ✅ Contenido técnico detallado
- ✅ Explicación de todas las tecnologías
- ✅ Descripción de componentes
- ✅ Documentación del código
- ✅ Secciones de conclusiones

---

## 📸 Paso 1: Capturar Imágenes

### App Móvil (usar simulador o dispositivo real)

**Pantallas a capturar:**

1. **Login y Registro** (`app/(auth)/login.jsx`)
   - Ejecuta: `npm start` y abre en Expo Go
   - Navega a la pantalla de login
   - Captura: pantalla completa del login
   - Navega a registro
   - Captura: pantalla completa del registro

2. **Mapa Principal** (`app/(tabs)/index.jsx`)
   - Captura del mapa con varios reportes (marcadores rojos y verdes)
   - Asegúrate de que se vean bien los marcadores

3. **Crear Reporte** (`app/report/lost.jsx`)
   - Captura del formulario vacío
   - Captura con datos llenos
   - Captura de selección de foto

4. **Búsqueda con IA** (`app/ai-search.jsx`)
   - Captura de la pantalla inicial
   - Captura de resultados de búsqueda con scores de similitud

5. **Mensajería** (`app/messages/[conversationId].jsx`)
   - Captura de lista de conversaciones
   - Captura de chat individual con mensajes

6. **Perfil** (`app/(tabs)/profile.jsx`)
   - Captura de pantalla de perfil
   - Captura de "Mis mascotas"

**Tips para buenas capturas:**
- Usa datos de prueba realistas
- Asegúrate de que el texto sea legible
- Captura en modo light (mejor para impresión)
- Resolución mínima: 1080x1920 (Full HD)

### Backend y Documentación

7. **Swagger UI**
   - Abre: `http://localhost:8003/docs` o `http://tu-ip-gcp:8003/docs`
   - Captura de la lista de endpoints
   - Captura de un endpoint expandido (ej: `/embeddings/search_image`)
   - Captura de un schema de response

8. **Supabase Dashboard**
   - Abre: https://supabase.com/dashboard/project/tu-proyecto
   - Captura de Table Editor mostrando tabla `reports`
   - Captura mostrando la columna `embedding` (vector)
   - Captura de Storage con imágenes
   - Captura de SQL Editor con una función RPC

9. **Google Cloud Platform**
   - Abre: https://console.cloud.google.com
   - Captura de VM Instances mostrando tu VM
   - Captura de Firewall rules
   - Captura de logs (opcional)

### Diagramas

10. **Arquitectura del Sistema**
    - Usa draw.io o Lucidchart
    - Crea diagrama con:
      - App Móvil
      - Backend (FastAPI)
      - Supabase
      - Google Cloud
      - Conexiones entre ellos

11. **Diagrama Entidad-Relación**
    - Usa dbdiagram.io o draw.io
    - Incluye tablas: users, reports, pets, matches, messages
    - Muestra relaciones (FK)

---

## 📝 Paso 2: Insertar Imágenes en el Documento

### Opción A: Markdown (para visualización web)

Reemplaza la sección "Anexo: Capturas de Pantalla" con:

```markdown
## Anexo: Capturas de Pantalla

### Aplicación Móvil

#### Figura 1: Pantalla de Login
![Login](./imagenes/01-login.png)
*Pantalla de inicio de sesión con autenticación de Supabase*

#### Figura 2: Mapa Interactivo
![Mapa](./imagenes/02-mapa.png)
*Mapa principal mostrando reportes de mascotas perdidas (rojo) y encontradas (verde)*

#### Figura 3: Crear Reporte
![Crear Reporte](./imagenes/03-crear-reporte.png)
*Formulario para reportar mascota perdida con selección de foto y ubicación*

[... continuar con todas las imágenes ...]
```

### Opción B: Word/PDF (para tesis impresa)

1. Convierte el Markdown a Word:
   ```bash
   # Si tienes pandoc instalado
   pandoc CAPITULO-XIII-ENTREGABLES.md -o CAPITULO-XIII.docx
   ```

2. En Word, inserta imágenes:
   - Ve a cada sección de "Imagen X"
   - Inserta → Imagen → Desde archivo
   - Agrega pie de imagen: "Figura X: Descripción"
   - Centra la imagen
   - Ajusta tamaño (no más de 15cm de ancho)

---

## 🎨 Paso 3: Formato para la Tesis

### Ajustes de formato (si usas Word):

1. **Portada del capítulo:**
   ```
   CAPÍTULO XIII
   ENTREGABLES
   ```

2. **Estilos de títulos:**
   - Título 1: 16pt, negrita, centrado
   - Título 2: 14pt, negrita, izquierda
   - Título 3: 12pt, negrita, izquierda
   - Texto: 12pt, justificado, interlineado 1.5

3. **Numeración de figuras:**
   - Figura 13.1, Figura 13.2, etc.
   - Todas centradas con pie de imagen

4. **Bloques de código:**
   - Fuente: Courier New o Consolas
   - Tamaño: 10pt
   - Fondo gris claro (#F5F5F5)
   - Borde fino

5. **Tablas:**
   - Bordes simples
   - Encabezado en negrita
   - Alternancia de colores en filas (opcional)

---

## 📊 Paso 4: Crear Diagramas Adicionales

### Diagrama de Arquitectura

Usa **draw.io** (https://app.diagrams.net/):

```
┌─────────────────┐
│   Usuarios      │
│ (iOS/Android)   │
└────────┬────────┘
         │
         ├──────────────────┬─────────────────┐
         │                  │                 │
┌────────▼────────┐  ┌──────▼─────────┐ ┌────▼──────────┐
│ React Native App│  │  Supabase      │ │ Google Cloud  │
│  - Expo Router  │◄─┤  - PostgreSQL  │ │  - FastAPI    │
│  - Maps         │  │  - Auth        │ │  - Docker     │
│  - Zustand      │  │  - Storage     │ │  - MegaDesc   │
└─────────────────┘  └────────────────┘ └───────────────┘
```

### Diagrama Entidad-Relación

Usa **dbdiagram.io** (https://dbdiagram.io/):

```sql
Table users {
  id uuid [pk]
  email varchar
  full_name varchar
  created_at timestamp
}

Table reports {
  id uuid [pk]
  user_id uuid [ref: > users.id]
  type varchar
  species varchar
  photo_url text
  embedding vector(1536)
  location geography
  created_at timestamp
}

Table matches {
  id uuid [pk]
  report_lost_id uuid [ref: > reports.id]
  report_found_id uuid [ref: > reports.id]
  similarity_score float
  confidence varchar
}
```

### Diagrama de Flujo - Búsqueda con IA

```
Usuario sube foto
       ↓
App redimensiona imagen
       ↓
Sube a Supabase Storage
       ↓
Backend descarga imagen
       ↓
MegaDescriptor genera embedding (1536 dims)
       ↓
Búsqueda vectorial con pgvector
       ↓
Retorna top 10 similares
       ↓
App muestra resultados con scores
```

---

## 🔍 Paso 5: Revisión Final

### Checklist antes de entregar:

- [ ] Todas las capturas de pantalla insertadas y numeradas
- [ ] Todos los diagramas creados y con buena resolución
- [ ] Pies de imagen descriptivos en todas las figuras
- [ ] Código formateado correctamente (sintaxis resaltada si es posible)
- [ ] URLs y credenciales reemplazadas con placeholders (no expongas datos reales)
- [x] Nombres consistentes (PetAlert)
- [ ] Fechas actualizadas
- [ ] Estadísticas verificadas
- [ ] Referencias cruzadas entre secciones
- [ ] Ortografía y gramática revisadas
- [ ] Formato consistente con otros capítulos de la tesis
- [ ] Numeración de páginas
- [ ] Índice de figuras y tablas (si aplica)

---

## 💡 Tips Adicionales

### Para mejorar la presentación:

1. **Agrega color estratégicamente:**
   - Verde para éxitos/completados
   - Rojo para errores/alertas
   - Azul para información
   - Amarillo para warnings

2. **Usa íconos en títulos (si tu formato lo permite):**
   - 🚀 Deploy
   - 🤖 Inteligencia Artificial
   - 📱 App Móvil
   - 🗄️ Base de Datos

3. **Resalta números importantes:**
   - **1536** dimensiones del embedding
   - **85-95%** de precisión
   - **10-50ms** tiempo de búsqueda
   - **$40/mes** costo de hosting

4. **Agrega notas al pie para términos técnicos** (primera aparición):
   - embedding¹
   - pgvector²
   - cosine similarity³
   
   ¹ Representación vectorial numérica de una imagen

---

## 🚀 Comandos Útiles para Capturas

### Capturar pantallas de la app:

```bash
# Iniciar app
npm start

# Abrir en simulador iOS
i

# Abrir en simulador Android
a

# Abrir en navegador (útil para capturas)
w
```

### Verificar backend para capturas:

```bash
# Local
cd backend
uvicorn main:app --reload --port 8003

# En VM (SSH)
ssh tu-vm
cd petFindnoborres
docker-compose logs -f backend
```

### Acceder a servicios:

- App: Expo Go en tu celular
- Backend Docs: http://localhost:8003/docs
- Supabase: https://supabase.com/dashboard
- GCP: https://console.cloud.google.com

---

## 📧 Soporte

Si tienes dudas sobre:
- Formato específico de tu universidad
- Normas APA/IEEE para referencias
- Estructura particular requerida

Consulta el manual de tesis de tu institución o pregunta a tu asesor.

---

**¡Tu capítulo está casi listo! Solo faltan las imágenes y el formato final.** 🎓

¿Necesitas ayuda con alguna parte específica?



