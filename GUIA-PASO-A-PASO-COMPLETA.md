# 🐳🚀 Guía Paso a Paso Completa: Docker + Google Cloud

Te guiaré paso a paso para desplegar tu aplicación en Docker y Google Compute Engine.

---

## 📋 FASE 1: PREPARACIÓN LOCAL

### ✅ PASO 1.1: Verificar que tienes todo

Verifica que tienes estos archivos en tu proyecto:

```
petFindnoborres/
├── backend/
│   ├── Dockerfile          ✅
│   ├── requirements.txt    ✅
│   ├── main.py            ✅
│   ├── env.example        ✅
│   └── .env               ⚠️ (debes crearlo)
├── docker-compose.yml     ✅
└── deploy-vm.sh           ✅
```

**¿Tienes todos estos archivos?** Si falta alguno, avísame.

---

### 📝 PASO 1.2: Crear archivo .env

**IMPORTANTE:** Necesitas tus credenciales de Supabase antes de continuar.

#### 1.2.1. Obtener credenciales de Supabase

1. Ve a tu proyecto en Supabase: https://app.supabase.com
2. Ve a **Settings** → **API**
3. Copia:
   - **Project URL** (ejemplo: `https://xxxxx.supabase.co`)
   - **service_role key** (la clave secreta, NO la anon key)

#### 1.2.2. Crear el archivo .env

**En PowerShell (Windows):**

```powershell
# Navegar a la carpeta backend
cd backend

# Copiar el archivo de ejemplo
copy env.example .env

# Abrir en el editor
notepad .env
```

#### 1.2.3. Editar el archivo .env

Reemplaza los valores con tus credenciales reales:

```env
SUPABASE_URL=https://TU-PROYECTO-ID.supabase.co
SUPABASE_SERVICE_KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InR1LXByb3llY3RvLWlkIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTY0NjE2MjAwMCwiZXhwIjoxOTYxNzM4MDAwfQ.tu-clave-aqui
ALLOWED_ORIGINS=*
GENERATE_EMBEDDINGS_LOCALLY=true
```

**Guarda el archivo** (Ctrl+S en Notepad).

#### 1.2.4. Verificar que se creó correctamente

```powershell
# Verificar que existe
Test-Path .env

# Ver el contenido (sin mostrar la clave completa)
Get-Content .env | Select-String "SUPABASE"
```

**✅ Si el archivo existe y tiene tus credenciales, continúa al siguiente paso.**

---

## ☁️ FASE 2: GOOGLE CLOUD - CREAR VM

### 🌐 PASO 2.1: Acceder a Google Cloud Console

1. Abre tu navegador
2. Ve a: https://console.cloud.google.com
3. Inicia sesión con tu cuenta de Google
4. **Selecciona o crea un proyecto:**
   - Si ya tienes un proyecto: selecciónalo del menú desplegable arriba
   - Si no tienes: click en "Select a project" → "NEW PROJECT"
     - Nombre: `petalert-backend` (o el que prefieras)
     - Click en "CREATE"

**¿Ya estás en Google Cloud Console con un proyecto seleccionado?** ✅

---

### 🔌 PASO 2.2: Habilitar APIs necesarias

1. En el menú de la izquierda (☰), busca **"APIs & Services"** → **"Library"**
2. Busca y habilita estas APIs (una por una):
   - **Compute Engine API**
     - Busca "Compute Engine API"
     - Click en el resultado
     - Click en **"ENABLE"**
   - **Cloud Resource Manager API**
     - Busca "Cloud Resource Manager API"
     - Click en **"ENABLE"**

**Espera a que se habiliten** (puede tardar unos segundos cada una).

**✅ ¿Ya habilitaste ambas APIs?** Continúa.

---

### 🖥️ PASO 2.3: Crear la VM (Máquina Virtual)

1. En el menú de la izquierda, ve a **"Compute Engine"** → **"VM instances"**
2. Si es la primera vez, puede pedirte habilitar Compute Engine API (ya lo hiciste)
3. Click en el botón **"CREATE INSTANCE"** (arriba)

#### Configuración detallada:

**1. Nombre y región:**
```
Name: petalert-backend
Region: us-central1 (o la más cercana a ti)
Zone: us-central1-a
```

**2. Configuración de máquina:**
- Click en "Machine type"
- Selecciona: **e2-medium**
  - 2 vCPU
  - 4 GB memoria
- Click en "SELECT"

**3. Disco de arranque:**
- Click en "Boot disk" → "CHANGE"
- Sistema operativo: **Ubuntu**
- Versión: **Ubuntu 22.04 LTS**
- Tipo de disco: **Balanced persistent disk**
- Tamaño: **50 GB** (cambia el valor si está en 10)
- Click en "SELECT"

**4. Firewall:**
- Marca las casillas:
  - ✅ **Allow HTTP traffic**
  - ✅ **Allow HTTPS traffic**

**5. Crear:**
- Click en el botón **"CREATE"** (abajo)

**⏳ Espera 1-2 minutos** mientras se crea la VM.

**✅ ¿Ya se creó la VM?** Deberías verla en la lista con un estado "Running" (verde).

---

### 🔥 PASO 2.4: Anotar la IP Externa

1. En la lista de VMs, busca tu VM `petalert-backend`
2. En la columna **"External IP"**, verás una IP (ejemplo: `34.123.45.67`)
3. **ANÓTALA** - la necesitarás más adelante

**Ejemplo:** `34.123.45.67`

**✅ ¿Ya anotaste la IP externa?** Continúa.

---

## 🔧 FASE 3: CONFIGURAR LA VM

### 🔐 PASO 3.1: Conectarse a la VM por SSH

Tienes dos opciones:

**Opción A: Desde Google Cloud Console (Más fácil)**
1. En la lista de VMs, encuentra `petalert-backend`
2. Click en el botón **"SSH"** (a la derecha)
3. Se abrirá una ventana de terminal en el navegador
4. **¡Listo!** Ya estás conectado a la VM

**Opción B: Desde tu terminal local (si tienes gcloud CLI)**
```powershell
gcloud compute ssh petalert-backend --zone=us-central1-a
```

**✅ ¿Ya estás conectado a la VM?** Continúa con el siguiente paso.

---

### 📦 PASO 3.2: Actualizar el sistema

En la terminal de la VM, ejecuta:

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

**⏳ Esto puede tardar 2-5 minutos.** Espera a que termine.

**✅ ¿Terminó sin errores?** Continúa.

---

### 🐳 PASO 3.3: Instalar Docker

Ejecuta estos comandos **uno por uno** en la terminal de la VM:

```bash
# 1. Instalar dependencias
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release
```

```bash
# 2. Agregar la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg
```

```bash
# 3. Configurar el repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

```bash
# 4. Actualizar e instalar Docker
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io
```

**⏳ Esto puede tardar 3-5 minutos.** Espera a que termine.

---

### 🐙 PASO 3.4: Instalar Docker Compose

```bash
# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose
```

---

### 👤 PASO 3.5: Configurar usuario para Docker

```bash
# Agregar tu usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER

# Aplicar cambios
newgrp docker
```

---

### ✅ PASO 3.6: Verificar instalación

```bash
# Verificar Docker
docker --version

# Verificar Docker Compose
docker-compose --version
```

**Deberías ver algo como:**
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

**✅ ¿Ves las versiones?** ¡Perfecto! Continúa.

---

### 📥 PASO 3.7: Instalar Git

```bash
sudo apt-get install -y git
```

```bash
# Verificar
git --version
```

**✅ ¿Git está instalado?** Continúa.

---

## 📤 FASE 4: SUBIR EL CÓDIGO A LA VM

Tienes dos opciones para subir tu código:

### 📋 Opción A: Usando Git (Recomendado si tu proyecto está en GitHub/GitLab)

**Si tu proyecto NO está en Git, ve a la Opción B.**

#### 4A.1: Subir tu proyecto a GitHub (si no lo has hecho)

1. Ve a https://github.com
2. Crea un nuevo repositorio
3. Sube tu código

#### 4A.2: Clonar en la VM

En la terminal de la VM:

```bash
cd ~
git clone https://github.com/TU_USUARIO/petFindnoborres.git
cd petFindnoborres
```

**✅ ¿Ya clonaste el repositorio?** Continúa al PASO 5.

---

### 📋 Opción B: Subir archivos directamente con SCP

**Si tu proyecto NO está en Git, usa esta opción.**

#### 4B.1: Instalar Google Cloud SDK en tu máquina local (si no lo tienes)

1. Descarga desde: https://cloud.google.com/sdk/docs/install
2. Instala siguiendo las instrucciones
3. Abre PowerShell y ejecuta:

```powershell
gcloud auth login
```

#### 4B.2: Empaquetar el proyecto

En PowerShell (en tu máquina local, en la carpeta del proyecto):

```powershell
# Crear archivo comprimido con los archivos necesarios
tar -czf petalert-backend.tar.gz backend docker-compose.yml deploy-vm.sh
```

#### 4B.3: Subir a la VM

```powershell
# Subir el archivo comprimido
gcloud compute scp petalert-backend.tar.gz petalert-backend:~/ --zone=us-central1-a
```

**⏳ Espera a que termine la subida.**

#### 4B.4: Descomprimir en la VM

En la terminal de la VM:

```bash
cd ~
tar -xzf petalert-backend.tar.gz
mkdir -p petFindnoborres
mv backend docker-compose.yml deploy-vm.sh petFindnoborres/
cd petFindnoborres
```

**✅ ¿Ya tienes los archivos en la VM?** Verifica:

```bash
ls -la
```

Deberías ver: `backend`, `docker-compose.yml`, `deploy-vm.sh`

---

## ⚙️ FASE 5: CONFIGURAR VARIABLES DE ENTORNO EN LA VM

### 📝 PASO 5.1: Crear archivo .env en la VM

En la terminal de la VM:

```bash
cd ~/petFindnoborres/backend
cp env.example .env
nano .env
```

### 📝 PASO 5.2: Editar el archivo .env

En el editor nano:

1. **Navega con las flechas** hasta cada línea
2. **Reemplaza los valores** con tus credenciales reales:

```env
SUPABASE_URL=https://TU-PROYECTO-ID.supabase.co
SUPABASE_SERVICE_KEY=tu-clave-service-role-completa-aqui
ALLOWED_ORIGINS=*
GENERATE_EMBEDDINGS_LOCALLY=true
```

3. **Para guardar:**
   - Presiona `Ctrl + X`
   - Presiona `Y` (para confirmar)
   - Presiona `Enter`

**✅ ¿Ya guardaste el archivo .env?** Continúa.

---

### ✅ PASO 5.3: Verificar el archivo .env

```bash
# Verificar que existe
ls -la .env

# Ver el contenido (sin mostrar valores sensibles)
cat .env | grep SUPABASE_URL
```

**✅ ¿Ves tu URL de Supabase?** Perfecto, continúa.

---

## 🐳 FASE 6: DESPLEGAR CON DOCKER

### 🔧 PASO 6.1: Hacer el script ejecutable

En la terminal de la VM:

```bash
cd ~/petFindnoborres
chmod +x deploy-vm.sh
```

---

### 🚀 PASO 6.2: Ejecutar el deploy

```bash
./deploy-vm.sh
```

**⏳ ESTO PUEDE TARDAR 10-15 MINUTOS** la primera vez porque:
- Descarga la imagen de Python
- Instala todas las dependencias (incluyendo PyTorch que es grande)
- Construye la imagen Docker

**Espera pacientemente.** Verás muchos mensajes en la pantalla.

**✅ ¿Terminó el script sin errores?** Deberías ver un mensaje como:
```
✅ Backend deployado exitosamente!
🌐 API disponible en: http://localhost:8003
```

---

### 🔍 PASO 6.3: Verificar que el contenedor está corriendo

```bash
docker-compose ps
```

**Deberías ver algo como:**
```
NAME                STATUS          PORTS
petalert-backend-1  Up X minutes    0.0.0.0:8003->8003/tcp
```

**✅ ¿Ves el contenedor corriendo?** Continúa.

---

### 📋 PASO 6.4: Ver los logs

```bash
# Ver últimas 50 líneas
docker-compose logs --tail=50 backend
```

**Busca mensajes de error.** Si todo está bien, deberías ver que el servidor está corriendo.

**✅ ¿Los logs se ven bien?** Continúa.

---

### 🧪 PASO 6.5: Probar localmente en la VM

```bash
curl http://localhost:8003/health
```

**Deberías ver algo como:**
```json
{
  "status": "ok",
  "message": "PetAlert Vision API activa",
  "supabase": "conectado"
}
```

**✅ ¿Funciona el health check?** ¡Excelente! Continúa.

---

## 🔥 FASE 7: CONFIGURAR FIREWALL Y ACCESO EXTERNO

### 🔥 PASO 7.1: Crear regla de firewall en Google Cloud

1. Ve a Google Cloud Console
2. En el menú, ve a **"VPC network"** → **"Firewall"**
3. Click en **"CREATE FIREWALL RULE"** (arriba)

#### Configuración:

```
Name: allow-petalert-backend
Description: Permitir tráfico al backend de PetAlert
Network: default
Priority: 1000
Direction of traffic: Ingress
Action on match: Allow
Targets: Specified target tags
Target tags: petalert-backend
Source IP ranges: 0.0.0.0/0
Protocols and ports:
  ✅ tcp
  Ports: 8003
```

4. Click en **"CREATE"**

**✅ ¿Ya creaste la regla de firewall?** Continúa.

---

### 🏷️ PASO 7.2: Agregar tag a la VM

1. Ve a **"Compute Engine"** → **"VM instances"**
2. Click en el nombre de tu VM (`petalert-backend`)
3. Click en **"EDIT"** (arriba)
4. Busca la sección **"Network tags"**
5. En el campo, escribe: `petalert-backend`
6. Click en **"SAVE"**

**✅ ¿Ya agregaste el tag?** Continúa.

---

### 🌐 PASO 7.3: Obtener la IP Externa

1. En la lista de VMs, busca tu VM
2. Anota la **"External IP"** (debería ser la misma que antes)

**Ejemplo:** `34.123.45.67`

**✅ ¿Tienes la IP externa?** Continúa.

---

### 🧪 PASO 7.4: Probar desde tu navegador

Abre en tu navegador:

```
http://TU_IP_EXTERNA:8003/health
```

**Ejemplo:** `http://34.123.45.67:8003/health`

**✅ ¿Puedes acceder y ver el JSON de respuesta?** ¡Felicidades! El deploy funcionó.

También prueba:
```
http://TU_IP_EXTERNA:8003/docs
```

Deberías ver la documentación interactiva de la API.

---

## 🌐 FASE 8: CONFIGURAR IP ESTÁTICA (OPCIONAL PERO RECOMENDADO)

### 📌 PASO 8.1: Reservar IP estática

1. Ve a **"VPC network"** → **"IP addresses"**
2. Click en **"RESERVE STATIC ADDRESS"** (arriba)
3. Configura:
   ```
   Name: petalert-backend-ip
   IP version: IPv4
   Type: Regional
   Region: us-central1 (la misma que tu VM)
   ```
4. Click en **"RESERVE"**

**✅ ¿Ya reservaste la IP?** Continúa.

---

### 🔗 PASO 8.2: Asignar IP a la VM

1. Ve a **"Compute Engine"** → **"VM instances"**
2. Click en el nombre de tu VM
3. Click en **"EDIT"**
4. En **"Network interfaces"**, click en el lápiz (✏️)
5. En **"External IP"**, cambia de "Ephemeral" a la IP estática que acabas de reservar
6. Click en **"DONE"**
7. Click en **"SAVE"**

**⏳ Espera 1-2 minutos** mientras se reinicia la interfaz de red.

**✅ ¿Ya asignaste la IP estática?** Continúa.

---

### 📱 PASO 8.3: Actualizar tu aplicación móvil

En tu proyecto React Native, actualiza la URL del backend:

```javascript
// src/config/api.js o donde esté tu configuración
const BACKEND_URL = 'http://TU_IP_ESTATICA:8003';

export default BACKEND_URL;
```

O si usas variables de entorno en Expo:

```env
# .env en tu proyecto frontend
EXPO_PUBLIC_BACKEND_URL=http://TU_IP_ESTATICA:8003
```

**✅ ¿Ya actualizaste la URL en tu app?** ¡Listo!

---

## ✅ VERIFICACIÓN FINAL

### Checklist de verificación:

- [ ] VM creada y corriendo en Google Cloud
- [ ] Docker y Docker Compose instalados en la VM
- [ ] Código subido a la VM
- [ ] Archivo `.env` configurado con credenciales reales
- [ ] Contenedor Docker corriendo (`docker-compose ps`)
- [ ] Health check funciona localmente en la VM (`curl http://localhost:8003/health`)
- [ ] Firewall configurado en Google Cloud
- [ ] Tag `petalert-backend` agregado a la VM
- [ ] Puedo acceder desde internet (`http://TU_IP:8003/health`)
- [ ] IP estática reservada y asignada (opcional)

**✅ ¿Tienes todo marcado?** ¡Felicidades! Tu aplicación está desplegada. 🎉

---

## 🛠️ COMANDOS ÚTILES

### Ver logs en tiempo real
```bash
docker-compose logs -f backend
```

### Reiniciar el servicio
```bash
docker-compose restart backend
```

### Detener el servicio
```bash
docker-compose down
```

### Iniciar el servicio
```bash
docker-compose up -d
```

### Reconstruir después de cambios
```bash
docker-compose up -d --build
```

### Ver estado
```bash
docker-compose ps
```

---

## 🐛 TROUBLESHOOTING

### El servicio no inicia
```bash
# Ver logs
docker-compose logs backend

# Verificar puerto
sudo netstat -tlnp | grep 8003
```

### No puedo acceder desde internet
1. Verifica el firewall en Google Cloud
2. Verifica que la VM tiene el tag `petalert-backend`
3. Verifica que el servicio escucha en `0.0.0.0:8003`

### Error con variables de entorno
```bash
# Verificar archivo .env
cat backend/.env
```

---

¡Éxito con tu deploy! 🚀🐕


