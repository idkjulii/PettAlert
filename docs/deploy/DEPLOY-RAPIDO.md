# 🚀 Deploy Rápido - Resumen

Esta es una guía resumida para hostear el backend en Google Cloud VM.

## ✅ Checklist Pre-Deploy

- [ ] Cuenta de Google Cloud Platform
- [ ] Archivo `backend/.env` configurado con credenciales de Supabase
- [ ] Archivo `backend/google-vision-key.json` con credenciales de Google Vision

---

## 🎯 Pasos Rápidos

### 1️⃣ Crear VM en Google Cloud

```yaml
Console: https://console.cloud.google.com
Ir a: Compute Engine → VM instances → CREATE INSTANCE

Configuración:
- Nombre: petalert-backend
- Región: us-central1
- Máquina: e2-medium (2 vCPU, 4 GB RAM)
- Boot disk: Ubuntu 22.04 LTS, 50 GB
- Firewall: ✅ Allow HTTP/HTTPS
```

### 2️⃣ Configurar Firewall

```yaml
VPC network → Firewall → CREATE FIREWALL RULE

- Nombre: allow-petalert-backend
- Dirección: Ingress
- Action: Allow
- Targets: Specified target tags
- Target tags: petalert-backend
- Source IP ranges: 0.0.0.0/0
- Protocols and ports: tcp:8003
```

### 3️⃣ Conectar y Configurar

```bash
# Click en SSH en la VM

# Ejecutar setup automático
sudo apt-get update && sudo apt-get install -y curl
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo apt-get install -y docker-compose-plugin git

# Agregar usuario a grupo docker
sudo usermod -aG docker $USER
newgrp docker
```

### 4️⃣ Subir Proyecto

**Opción A - Con Git:**
```bash
git clone https://github.com/TU_USUARIO/petFindnoborres.git
cd petFindnoborres
```

**Opción B - Sin Git (desde tu PC):**
```bash
# En tu PC (PowerShell):
# Comprimir proyecto
tar -czf petalert.tar.gz backend docker-compose.yml deploy-vm.sh scripts

# Subir a VM
gcloud compute scp petalert.tar.gz petalert-backend:~/ --zone=us-central1-a

# En la VM:
tar -xzf petalert.tar.gz
cd petFindnoborres
```

### 5️⃣ Configurar Credenciales

```bash
cd ~/petFindnoborres/backend

# Copiar y editar .env
cp env.example .env
nano .env  # Edita con tus credenciales

# Subir google-vision-key.json
# (desde tu PC con gcloud compute scp)
```

### 6️⃣ Deploy

```bash
cd ~/petFindnoborres
chmod +x deploy-vm.sh scripts/*.sh
./deploy-vm.sh
```

### 7️⃣ Obtener IP y Probar

```bash
# Obtener IP pública
curl -H "Metadata-Flavor: Google" http://metadata.google.internal/computeMetadata/v1/instance/network-interfaces/0/access-configs/0/external-ip

# Probar (reemplaza TU_IP)
curl http://TU_IP:8003/health
```

### 8️⃣ Configurar App

En tu app React Native, actualiza la URL del backend:

```javascript
// .env o config
EXPO_PUBLIC_BACKEND_URL=http://TU_IP:8003
```

---

## 📋 Comandos Útiles

```bash
# Ver logs
docker-compose logs -f backend

# Reiniciar
docker-compose restart backend

# Ver estado
docker-compose ps

# Monitor
./scripts/monitor.sh
```

---

## 🐛 Problemas Comunes

**No puedo acceder desde internet:**
- Verifica firewall en GCP (puerto 8003)
- Verifica que la VM tenga el tag `petalert-backend`

**El servicio no inicia:**
```bash
docker-compose logs backend
```

**Falta memoria:**
```bash
# Cambiar a VM con más RAM (e2-standard-2)
# O agregar swap:
sudo fallocate -l 2G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

---

## 📚 Ver Guía Completa

Para más detalles, consulta: `GUIA-DEPLOY-GOOGLE-CLOUD.md`

---

💡 **Costo estimado:** ~$35-50/mes con e2-medium





