# 🚀 Guía de Deploy en Google Cloud VM

Esta guía te ayudará a hostear el backend de PetAlert en una VM (máquina virtual) de Google Cloud Platform (GCP).

## 📋 Prerequisitos

1. Una cuenta de Google Cloud Platform
2. Proyecto creado en GCP
3. Credenciales de Supabase configuradas
4. Archivo de credenciales de Google Vision API (`google-vision-key.json`)

---

## 🖥️ PASO 1: Crear la VM en Google Cloud

### 1.1. Accede a Google Cloud Console
```
https://console.cloud.google.com
```

### 1.2. Navega a Compute Engine
- Ve a **Menú ☰** → **Compute Engine** → **VM instances**
- Si es la primera vez, habilita la API de Compute Engine

### 1.3. Crear una nueva instancia
Click en **"CREATE INSTANCE"** y configura:

#### Configuración recomendada:
```yaml
Nombre: petalert-backend
Región: us-central1 (o la más cercana a tus usuarios)
Zona: us-central1-a

Configuración de máquina:
  Serie: E2
  Tipo: e2-medium (2 vCPU, 4 GB memoria)
  # Para modelos ML grandes, considera: e2-standard-2 o e2-standard-4

Disco de arranque:
  Sistema operativo: Ubuntu
  Versión: Ubuntu 22.04 LTS
  Tipo de disco: Balanced persistent disk
  Tamaño: 30 GB (mínimo recomendado: 50 GB para modelos ML)

Firewall:
  ✅ Permitir tráfico HTTP
  ✅ Permitir tráfico HTTPS
```

### 1.4. Configurar reglas de firewall
Después de crear la VM, configura el firewall:

1. Ve a **VPC network** → **Firewall** → **CREATE FIREWALL RULE**

```yaml
Nombre: allow-petalert-backend
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

2. Vuelve a tu VM y edítala para agregar el tag:
   - Click en el nombre de tu VM
   - Click en **EDIT**
   - En "Network tags" agrega: `petalert-backend`
   - Click **SAVE**

---

## 🔧 PASO 2: Configurar la VM

### 2.1. Conectarse a la VM
Desde Google Cloud Console, click en **SSH** junto a tu VM.

### 2.2. Actualizar el sistema
```bash
sudo apt-get update
sudo apt-get upgrade -y
```

### 2.3. Instalar Docker
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

### 2.4. Instalar Git
```bash
sudo apt-get install -y git
```

---

## 📦 PASO 3: Clonar y Configurar el Proyecto

### 3.1. Clonar el repositorio
Si tienes el proyecto en GitHub:
```bash
cd ~
git clone https://github.com/TU_USUARIO/petFindnoborres.git
cd petFindnoborres
```

Si NO tienes el proyecto en un repositorio, sube los archivos:
```bash
# En tu máquina local (PowerShell/CMD):
# Primero, empaqueta el proyecto
tar -czf petalert-backend.tar.gz backend docker-compose.yml deploy-vm.sh

# Luego sube a la VM usando gcloud (instala gcloud SDK si no lo tienes)
gcloud compute scp petalert-backend.tar.gz petalert-backend:~/ --zone=us-central1-a

# En la VM, descomprime:
cd ~
tar -xzf petalert-backend.tar.gz
```

### 3.2. Configurar variables de entorno
```bash
cd ~/petFindnoborres/backend
cp env.example .env
nano .env  # o usa 'vim .env'
```

Edita el archivo `.env` con tus credenciales reales:
```bash
# Supabase Configuration (Backend)
SUPABASE_URL=https://tu-proyecto-id.supabase.co
SUPABASE_SERVICE_KEY=tu-clave-service-role-aqui

# Backend Configuration
ALLOWED_ORIGINS=*
# En producción, especifica tu dominio: https://tuapp.com

# Embeddings locales
GENERATE_EMBEDDINGS_LOCALLY=true
```

Guarda el archivo:
- Si usas nano: `Ctrl+X`, luego `Y`, luego `Enter`
- Si usas vim: `Esc`, luego `:wq`, luego `Enter`

### 3.3. Subir credenciales de Google Cloud Vision
**OPCIÓN A: Desde tu máquina local**
```bash
# En tu máquina local (PowerShell/CMD):
gcloud compute scp backend/google-vision-key.json petalert-backend:~/petFindnoborres/backend/ --zone=us-central1-a
```

**OPCIÓN B: Copiar y pegar**
```bash
# En la VM:
cd ~/petFindnoborres/backend
nano google-vision-key.json
# Pega el contenido de tu archivo JSON
# Guarda con Ctrl+X, Y, Enter
```

---

## 🚀 PASO 4: Deploy del Backend

### 4.1. Hacer el script ejecutable
```bash
cd ~/petFindnoborres
chmod +x deploy-vm.sh
```

### 4.2. Ejecutar el deploy
```bash
./deploy-vm.sh
```

Este script:
- ✅ Verifica los archivos de configuración
- ✅ Construye la imagen Docker
- ✅ Inicia el contenedor
- ✅ Verifica que el servicio esté funcionando

### 4.3. Verificar que funciona
```bash
# Verificar el estado del contenedor
docker-compose ps

# Ver logs
docker-compose logs -f backend

# Probar el endpoint de health
curl http://localhost:8003/health

# Deberías ver algo como:
# {"status":"ok","message":"PetAlert Vision API activa","supabase":"conectado","google_vision":"configurado"}
```

---

## 🌐 PASO 5: Obtener la IP Pública

### 5.1. Obtener la IP externa
```bash
# En la VM:
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip
```

O desde Google Cloud Console:
- Ve a **Compute Engine** → **VM instances**
- Busca tu VM, la IP externa está en la columna "External IP"

### 5.2. Reservar la IP (recomendado)
Por defecto, la IP es efímera (cambia si reinicias la VM). Para hacerla estática:

1. Ve a **VPC network** → **IP addresses**
2. Encuentra tu IP externa
3. Click en **RESERVE**
4. Dale un nombre (ej: `petalert-backend-ip`)

### 5.3. Probar desde tu navegador
```
http://TU_IP_EXTERNA:8003/health
http://TU_IP_EXTERNA:8003/docs
```

---

## 📱 PASO 6: Configurar tu App React Native

### 6.1. Editar la configuración del backend
En tu proyecto React Native, actualiza la URL del backend:

```javascript
// src/config/api.js o donde esté tu configuración
const BACKEND_URL = 'http://TU_IP_EXTERNA:8003';

export default BACKEND_URL;
```

### 6.2. Si usas variables de entorno en Expo:
```bash
# En el archivo .env de tu frontend:
EXPO_PUBLIC_BACKEND_URL=http://TU_IP_EXTERNA:8003
```

---

## 🔒 PASO 7: Configurar HTTPS (Opcional pero Recomendado)

Para producción, deberías usar HTTPS con un dominio y certificado SSL.

### 7.1. Opción A: Usar Nginx como proxy reverso

**Instalar Nginx:**
```bash
sudo apt-get install -y nginx certbot python3-certbot-nginx
```

**Configurar Nginx:**
```bash
sudo nano /etc/nginx/sites-available/petalert
```

Contenido:
```nginx
server {
    listen 80;
    server_name tudominio.com;

    location / {
        proxy_pass http://localhost:8003;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**Activar configuración:**
```bash
sudo ln -s /etc/nginx/sites-available/petalert /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

**Obtener certificado SSL con Let's Encrypt:**
```bash
sudo certbot --nginx -d tudominio.com
```

### 7.2. Opción B: Usar Cloudflare (más fácil)

1. Registra un dominio (o usa uno existente)
2. Configura Cloudflare para tu dominio
3. Agrega un registro A apuntando a tu IP de GCP
4. Cloudflare proporciona SSL automático

---

## 🔄 COMANDOS ÚTILES

### Gestión del servicio
```bash
# Ver logs en tiempo real
docker-compose logs -f backend

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
```

### Actualizar el código
```bash
cd ~/petFindnoborres

# Si usas Git:
git pull origin main

# Reconstruir y reiniciar
./deploy-vm.sh
```

### Monitoreo
```bash
# Ver uso de recursos
docker stats

# Espacio en disco
df -h

# Memoria
free -h

# Procesos
top
```

### Limpieza
```bash
# Limpiar imágenes antiguas
docker system prune -a

# Ver espacio usado por Docker
docker system df
```

---

## 🐛 TROUBLESHOOTING

### Problema: El servicio no inicia
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
```bash
# Verificar que el firewall de GCP permite el puerto 8003
# Ve a VPC network → Firewall y verifica la regla

# Verificar que el servicio escucha en todas las interfaces
sudo netstat -tlnp | grep 8003
# Debe mostrar 0.0.0.0:8003, no 127.0.0.1:8003
```

### Problema: Error con Google Vision
```bash
# Verificar que el archivo de credenciales existe
ls -la ~/petFindnoborres/backend/google-vision-key.json

# Verificar permisos
chmod 600 ~/petFindnoborres/backend/google-vision-key.json

# Ver logs específicos
docker-compose logs backend | grep -i "vision"
```

### Problema: Falta memoria
```bash
# Ver uso de memoria
free -h

# Si necesitas más memoria, puedes:
# 1. Cambiar el tipo de VM a uno con más RAM (e2-standard-2)
# 2. Agregar swap:
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
echo '/swapfile none swap sw 0 0' | sudo tee -a /etc/fstab
```

---

## 💰 COSTOS ESTIMADOS

Con la configuración recomendada (e2-medium):
- **Instancia e2-medium**: ~$24/mes (uso 24/7)
- **Almacenamiento (50GB)**: ~$8/mes
- **Transferencia de datos**: Variable según uso
- **Total estimado**: ~$35-50/mes

**Tip**: Puedes usar créditos gratuitos de Google Cloud para nuevos usuarios ($300 USD).

---

## 🎯 PRÓXIMOS PASOS

1. ✅ **Configurar backups** de la VM
2. ✅ **Monitoreo**: Configura Cloud Monitoring
3. ✅ **Logs**: Usa Cloud Logging para logs centralizados
4. ✅ **Dominio personalizado**: Registra un dominio
5. ✅ **HTTPS**: Configura certificado SSL
6. ✅ **CI/CD**: Automatiza deploys con GitHub Actions

---

## 📚 RECURSOS ADICIONALES

- [Documentación de Google Cloud Compute Engine](https://cloud.google.com/compute/docs)
- [Documentación de Docker](https://docs.docker.com/)
- [Documentación de FastAPI](https://fastapi.tiangolo.com/)
- [Supabase Docs](https://supabase.com/docs)

---

## 🆘 SOPORTE

Si tienes problemas:
1. Revisa los logs: `docker-compose logs -f backend`
2. Verifica la configuración en `.env`
3. Asegúrate de que todas las credenciales están correctas
4. Verifica las reglas de firewall en GCP

---

¡Éxito con tu deploy! 🚀🐕




