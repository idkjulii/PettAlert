# 🐳🚀 Guía Completa: Deploy en Docker y Google Compute Engine

Esta guía te llevará paso a paso para desplegar tu aplicación PetAlert en Docker y Google Compute Engine.

---

## 📋 ÍNDICE

1. [Prerequisitos](#prerequisitos)
2. [PASO 1: Preparar el Proyecto Localmente](#paso-1-preparar-el-proyecto-localmente)
3. [PASO 2: Crear la VM en Google Cloud](#paso-2-crear-la-vm-en-google-cloud)
4. [PASO 3: Configurar la VM](#paso-3-configurar-la-vm)
5. [PASO 4: Subir el Proyecto a la VM](#paso-4-subir-el-proyecto-a-la-vm)
6. [PASO 5: Configurar Variables de Entorno](#paso-5-configurar-variables-de-entorno)
7. [PASO 6: Desplegar con Docker](#paso-6-desplegar-con-docker)
8. [PASO 7: Configurar Firewall y Acceso](#paso-7-configurar-firewall-y-acceso)
9. [PASO 8: Verificar el Deploy](#paso-8-verificar-el-deploy)
10. [PASO 9: Configurar IP Estática](#paso-9-configurar-ip-estática)
11. [Comandos Útiles](#comandos-útiles)
12. [Troubleshooting](#troubleshooting)

---

## 📦 PREREQUISITOS

Antes de comenzar, asegúrate de tener:

- ✅ Cuenta de Google Cloud Platform (GCP)
- ✅ Proyecto creado en GCP
- ✅ Google Cloud SDK instalado (opcional, pero recomendado)
- ✅ Credenciales de Supabase (URL y Service Key)
- ✅ Archivo de credenciales de Google Vision API (si lo usas)
- ✅ Git instalado en tu máquina local
- ✅ Acceso SSH a la VM

---

## 🏠 PASO 1: Preparar el Proyecto Localmente

### 1.1. Verificar que tienes todos los archivos necesarios

Asegúrate de tener estos archivos en tu proyecto:

```
petFindnoborres/
├── backend/
│   ├── Dockerfile          ✅ (ya existe)
│   ├── requirements.txt    ✅ (ya existe)
│   ├── main.py            ✅
│   ├── env.example        ✅
│   └── ... (resto de archivos)
├── docker-compose.yml     ✅ (ya existe)
└── deploy-vm.sh           ✅ (ya existe)
```

### 1.2. Verificar el Dockerfile

El Dockerfile en `backend/Dockerfile` debe estar correcto. Ya lo tienes configurado.

### 1.3. Preparar variables de entorno

Crea un archivo `.env` en `backend/` basándote en `env.example`:

```bash
# En tu máquina local (PowerShell)
cd backend
copy env.example .env
# Edita .env con tus credenciales reales
```

**Contenido mínimo del `.env`:**

```env
SUPABASE_URL=https://tu-proyecto-id.supabase.co
SUPABASE_SERVICE_KEY=tu-clave-service-role-aqui
ALLOWED_ORIGINS=*
GENERATE_EMBEDDINGS_LOCALLY=true
```

### 1.4. (Opcional) Subir a un repositorio Git

Si quieres usar Git para subir el código:

```bash
# Inicializar repositorio (si no lo tienes)
git init
git add .
git commit -m "Preparado para deploy"

# Subir a GitHub/GitLab
git remote add origin https://github.com/TU_USUARIO/petFindnoborres.git
git push -u origin main
```

---

## ☁️ PASO 2: Crear la VM en Google Cloud

### 2.1. Acceder a Google Cloud Console

1. Ve a: https://console.cloud.google.com
2. Selecciona tu proyecto (o crea uno nuevo)

### 2.2. Habilitar APIs necesarias

1. Ve a **APIs & Services** → **Library**
2. Busca y habilita:
   - ✅ **Compute Engine API**
   - ✅ **Cloud Resource Manager API**

### 2.3. Crear la instancia VM

1. Ve a **Compute Engine** → **VM instances**
2. Click en **CREATE INSTANCE**

#### Configuración recomendada:

```
Nombre: petalert-backend
Región: us-central1 (o la más cercana a tus usuarios)
Zona: us-central1-a

Configuración de máquina:
  Serie: E2
  Tipo: e2-medium
    - 2 vCPU
    - 4 GB RAM
  (Para modelos ML grandes, usa: e2-standard-2 o e2-standard-4)

Disco de arranque:
  Sistema operativo: Ubuntu
  Versión: Ubuntu 22.04 LTS
  Tipo de disco: Balanced persistent disk
  Tamaño: 50 GB (mínimo recomendado)

Firewall:
  ✅ Permitir tráfico HTTP
  ✅ Permitir tráfico HTTPS
```

3. Click en **CREATE**

### 2.4. Anotar la IP externa

Después de crear la VM, anota la **IP externa** que aparece en la lista de instancias. La necesitarás más adelante.

---

## 🔧 PASO 3: Configurar la VM

### 3.1. Conectarse a la VM

**Opción A: Desde Google Cloud Console**
1. Ve a **Compute Engine** → **VM instances**
2. Click en **SSH** junto a tu VM
3. Se abrirá una ventana de terminal en el navegador

**Opción B: Desde tu terminal local (con gcloud CLI)**
```bash
gcloud compute ssh petalert-backend --zone=us-central1-a
```

### 3.2. Actualizar el sistema

```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 3.3. Instalar Docker

```bash
# Instalar dependencias
sudo apt-get install -y \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg \
    lsb-release

# Agregar la clave GPG oficial de Docker
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# Configurar el repositorio
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# Instalar Docker Engine
sudo apt-get update
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# Instalar Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Agregar tu usuario al grupo docker (para no usar sudo)
sudo usermod -aG docker $USER

# Aplicar cambios (o cierra sesión y vuelve a entrar)
newgrp docker

# Verificar instalación
docker --version
docker-compose --version
```

Deberías ver algo como:
```
Docker version 24.x.x
Docker Compose version v2.x.x
```

### 3.4. Instalar Git

```bash
sudo apt-get install -y git
```

---

## 📤 PASO 4: Subir el Proyecto a la VM

Tienes dos opciones:

### Opción A: Usando Git (Recomendado)

Si subiste tu proyecto a GitHub/GitLab:

```bash
# En la VM
cd ~
git clone https://github.com/TU_USUARIO/petFindnoborres.git
cd petFindnoborres
```

### Opción B: Usando SCP (Subir archivos directamente)

**Desde tu máquina local (PowerShell):**

```bash
# Instalar gcloud CLI si no lo tienes
# Descarga desde: https://cloud.google.com/sdk/docs/install

# Autenticarse
gcloud auth login

# Subir archivos
gcloud compute scp --recurse backend petalert-backend:~/petFindnoborres/ --zone=us-central1-a
gcloud compute scp docker-compose.yml petalert-backend:~/petFindnoborres/ --zone=us-central1-a
gcloud compute scp deploy-vm.sh petalert-backend:~/petFindnoborres/ --zone=us-central1-a
```

**O empaquetar todo y subir:**

```bash
# En tu máquina local (PowerShell)
# Crear un archivo comprimido
tar -czf petalert-backend.tar.gz backend docker-compose.yml deploy-vm.sh

# Subir a la VM
gcloud compute scp petalert-backend.tar.gz petalert-backend:~/ --zone=us-central1-a

# En la VM, descomprimir:
cd ~
tar -xzf petalert-backend.tar.gz
mkdir -p petFindnoborres
mv backend docker-compose.yml deploy-vm.sh petFindnoborres/
cd petFindnoborres
```

---

## ⚙️ PASO 5: Configurar Variables de Entorno

### 5.1. Crear el archivo .env

```bash
# En la VM
cd ~/petFindnoborres/backend
cp env.example .env
nano .env  # o usa 'vim .env'
```

### 5.2. Editar el archivo .env

Edita el archivo con tus credenciales reales:

```env
# Supabase Configuration
SUPABASE_URL=https://tu-proyecto-id.supabase.co
SUPABASE_SERVICE_KEY=tu-clave-service-role-aqui

# Backend Configuration
ALLOWED_ORIGINS=*

# Embeddings locales
GENERATE_EMBEDDINGS_LOCALLY=true
```

**Para guardar en nano:**
- `Ctrl + X` para salir
- `Y` para confirmar
- `Enter` para guardar

**Para guardar en vim:**
- `Esc` para salir del modo inserción
- `:wq` y `Enter` para guardar y salir

### 5.3. (Opcional) Subir credenciales de Google Vision

Si usas Google Vision API:

**Desde tu máquina local:**
```bash
gcloud compute scp backend/google-vision-key.json petalert-backend:~/petFindnoborres/backend/ --zone=us-central1-a
```

**O copiar y pegar en la VM:**
```bash
cd ~/petFindnoborres/backend
nano google-vision-key.json
# Pega el contenido de tu archivo JSON
# Guarda con Ctrl+X, Y, Enter
```

---

## 🐳 PASO 6: Desplegar con Docker

### 6.1. Hacer el script ejecutable

```bash
cd ~/petFindnoborres
chmod +x deploy-vm.sh
```

### 6.2. Ejecutar el deploy

```bash
./deploy-vm.sh
```

Este script:
- ✅ Verifica los archivos de configuración
- ✅ Construye la imagen Docker
- ✅ Inicia el contenedor
- ✅ Verifica que el servicio esté funcionando

**Nota:** La primera vez puede tardar varios minutos porque descarga e instala todas las dependencias (incluyendo PyTorch).

### 6.3. Verificar que el contenedor está corriendo

```bash
docker-compose ps
```

Deberías ver algo como:
```
NAME                STATUS          PORTS
petalert-backend-1  Up X minutes    0.0.0.0:8003->8003/tcp
```

### 6.4. Ver los logs

```bash
# Ver logs en tiempo real
docker-compose logs -f backend

# Ver últimas 50 líneas
docker-compose logs --tail=50 backend
```

---

## 🔥 PASO 7: Configurar Firewall y Acceso

### 7.1. Crear regla de firewall en Google Cloud

1. Ve a **VPC network** → **Firewall** → **CREATE FIREWALL RULE**

2. Configura la regla:

```
Nombre: allow-petalert-backend
Descripción: Permitir tráfico al backend de PetAlert
Logs: Off
Red: default
Prioridad: 1000
Dirección: Ingress
Acción: Allow
Destinos: Specified target tags
Tags: petalert-backend
Filtros de origen: IP ranges
Rangos IPv4: 0.0.0.0/0
Protocolos y puertos:
  ✅ tcp: 8003
```

3. Click en **CREATE**

### 7.2. Agregar tag a la VM

1. Ve a **Compute Engine** → **VM instances**
2. Click en el nombre de tu VM (`petalert-backend`)
3. Click en **EDIT**
4. En la sección **Network tags**, agrega: `petalert-backend`
5. Click en **SAVE**

### 7.3. Verificar que el servicio escucha en todas las interfaces

```bash
# En la VM
sudo netstat -tlnp | grep 8003
```

Deberías ver:
```
tcp  0  0  0.0.0.0:8003  0.0.0.0:*  LISTEN  ...
```

Si ves `127.0.0.1:8003`, el servicio solo escucha localmente. Verifica que en `docker-compose.yml` el puerto esté mapeado correctamente.

---

## ✅ PASO 8: Verificar el Deploy

### 8.1. Probar localmente en la VM

```bash
# En la VM
curl http://localhost:8003/health
```

Deberías ver algo como:
```json
{
  "status": "ok",
  "message": "PetAlert Vision API activa",
  "supabase": "conectado",
  "google_vision": "configurado"
}
```

### 8.2. Obtener la IP externa

**Opción A: Desde Google Cloud Console**
- Ve a **Compute Engine** → **VM instances**
- Busca tu VM, la IP externa está en la columna "External IP"

**Opción B: Desde la VM**
```bash
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip
```

### 8.3. Probar desde tu navegador

Abre en tu navegador:
```
http://TU_IP_EXTERNA:8003/health
http://TU_IP_EXTERNA:8003/docs
```

Si puedes acceder, ¡el deploy fue exitoso! 🎉

---

## 🌐 PASO 9: Configurar IP Estática

Por defecto, la IP externa es **efímera** (cambia si reinicias la VM). Para hacerla estática:

### 9.1. Reservar la IP

1. Ve a **VPC network** → **IP addresses**
2. Click en **RESERVE STATIC ADDRESS**
3. Configura:
   ```
   Nombre: petalert-backend-ip
   Tipo: Regional (o Global si usas load balancer)
   Región: us-central1 (la misma que tu VM)
   ```
4. Click en **RESERVE**

### 9.2. Asignar la IP a la VM

1. Ve a **Compute Engine** → **VM instances**
2. Click en el nombre de tu VM
3. Click en **EDIT**
4. En **Network interfaces**, click en el lápiz (✏️)
5. En **External IP**, selecciona la IP estática que acabas de reservar
6. Click en **DONE** y luego **SAVE**

### 9.3. Actualizar tu aplicación

Actualiza la URL del backend en tu aplicación React Native:

```javascript
// src/config/api.js o donde esté tu configuración
const BACKEND_URL = 'http://TU_IP_ESTATICA:8003';

export default BACKEND_URL;
```

---

## 🛠️ COMANDOS ÚTILES

### Gestión del servicio Docker

```bash
# Ver logs en tiempo real
docker-compose logs -f backend

# Ver últimas 100 líneas
docker-compose logs --tail=100 backend

# Reiniciar el servicio
docker-compose restart backend

# Detener el servicio
docker-compose down

# Iniciar el servicio
docker-compose up -d

# Ver estado
docker-compose ps

# Reconstruir y reiniciar (después de cambios)
docker-compose up -d --build

# Ver uso de recursos
docker stats
```

### Actualizar el código

```bash
cd ~/petFindnoborres

# Si usas Git:
git pull origin main

# Reconstruir y reiniciar
./deploy-vm.sh
```

### Monitoreo del sistema

```bash
# Ver uso de CPU y memoria
top

# Ver espacio en disco
df -h

# Ver memoria disponible
free -h

# Ver procesos de Docker
docker ps
docker stats
```

### Limpieza de Docker

```bash
# Limpiar imágenes no usadas
docker image prune -a

# Limpiar todo (con cuidado)
docker system prune -a

# Ver espacio usado por Docker
docker system df
```

---

## 🐛 TROUBLESHOOTING

### Problema: El servicio no inicia

**Solución:**
```bash
# Ver logs detallados
docker-compose logs backend

# Verificar que el puerto 8003 no está en uso
sudo lsof -i :8003

# Reiniciar Docker
sudo systemctl restart docker
docker-compose up -d
```

### Problema: No puedo acceder desde internet

**Solución:**
1. Verifica que el firewall de GCP permite el puerto 8003
   - Ve a **VPC network** → **Firewall** y verifica la regla
2. Verifica que la VM tiene el tag correcto
   - Ve a tu VM → **EDIT** → Verifica que tiene el tag `petalert-backend`
3. Verifica que el servicio escucha en todas las interfaces:
   ```bash
   sudo netstat -tlnp | grep 8003
   # Debe mostrar 0.0.0.0:8003, no 127.0.0.1:8003
   ```

### Problema: Error con variables de entorno

**Solución:**
```bash
# Verificar que el archivo .env existe
ls -la ~/petFindnoborres/backend/.env

# Verificar el contenido (sin mostrar valores sensibles)
cat ~/petFindnoborres/backend/.env | grep -v "KEY\|PASSWORD"

# Verificar que Docker está leyendo las variables
docker-compose config
```

### Problema: Error con Google Vision

**Solución:**
```bash
# Verificar que el archivo de credenciales existe
ls -la ~/petFindnoborres/backend/google-vision-key.json

# Verificar permisos
chmod 600 ~/petFindnoborres/backend/google-vision-key.json

# Ver logs específicos
docker-compose logs backend | grep -i "vision"
```

### Problema: Falta memoria

**Solución:**
```bash
# Ver uso de memoria
free -h

# Si necesitas más memoria:
# 1. Cambiar el tipo de VM a uno con más RAM (e2-standard-2)
# 2. O agregar swap:
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

### Problema: El contenedor se reinicia constantemente

**Solución:**
```bash
# Ver logs para identificar el error
docker-compose logs --tail=100 backend

# Verificar el estado del contenedor
docker-compose ps

# Intentar iniciar manualmente para ver el error
docker-compose up backend
```

### Problema: No puedo conectarme por SSH

**Solución:**
1. Verifica que la VM está corriendo en Google Cloud Console
2. Intenta conectarte desde la consola web de Google Cloud
3. Verifica las reglas de firewall para SSH (puerto 22)

---

## 💰 COSTOS ESTIMADOS

Con la configuración recomendada (e2-medium):

- **Instancia e2-medium**: ~$24/mes (uso 24/7)
- **Almacenamiento (50GB)**: ~$8/mes
- **Transferencia de datos**: Variable según uso
- **IP estática**: Gratis (si está en uso)
- **Total estimado**: ~$35-50/mes

**Tip:** Puedes usar créditos gratuitos de Google Cloud para nuevos usuarios ($300 USD).

---

## 🎯 PRÓXIMOS PASOS

1. ✅ **Configurar backups** de la VM
2. ✅ **Monitoreo**: Configura Cloud Monitoring
3. ✅ **Logs**: Usa Cloud Logging para logs centralizados
4. ✅ **Dominio personalizado**: Registra un dominio
5. ✅ **HTTPS**: Configura certificado SSL con Let's Encrypt
6. ✅ **CI/CD**: Automatiza deploys con GitHub Actions
7. ✅ **Load Balancer**: Para alta disponibilidad

---

## 📚 RECURSOS ADICIONALES

- [Documentación de Google Cloud Compute Engine](https://cloud.google.com/compute/docs)
- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de Docker Compose](https://docs.docker.com/compose/)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Supabase Docs](https://supabase.com/docs)

---

## 🆘 SOPORTE

Si tienes problemas:

1. Revisa los logs: `docker-compose logs -f backend`
2. Verifica la configuración en `.env`
3. Asegúrate de que todas las credenciales están correctas
4. Verifica las reglas de firewall en GCP
5. Consulta la sección de Troubleshooting arriba

---

¡Éxito con tu deploy! 🚀🐕

