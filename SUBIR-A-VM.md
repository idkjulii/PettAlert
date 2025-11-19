# 📤 Cómo Subir el Proyecto a la VM

## Opción 1: Con `gcloud` (desde tu PC Windows)

### 1. Instalar Google Cloud SDK (si no lo tienes)
Descarga e instala desde: https://cloud.google.com/sdk/docs/install

### 2. Autenticarte
```powershell
gcloud auth login
gcloud config set project TU_PROJECT_ID
```

### 3. Subir el proyecto completo
```powershell
# Desde el directorio del proyecto en Windows (PowerShell):
cd C:\Users\maria\OneDrive\Escritorio\lpm\petFindnoborres

# Subir carpeta backend y archivos necesarios
gcloud compute scp --recurse backend petalert-backend-20251119-062307:~/ --zone=us-central1-a
gcloud compute scp docker-compose.yml petalert-backend-20251119-062307:~/ --zone=us-central1-a
gcloud compute scp deploy-vm.sh petalert-backend-20251119-062307:~/ --zone=us-central1-a
gcloud compute scp --recurse scripts petalert-backend-20251119-062307:~/ --zone=us-central1-a
```

---

## Opción 2: Con Git (si tienes el proyecto en GitHub)

### En la VM (donde ya estás conectado):
```bash
cd ~
git clone https://github.com/TU_USUARIO/TU_REPO.git petFindnoborres
cd petFindnoborres
```

---

## Opción 3: Manual con el Editor de SSH de Google Cloud

1. En Google Cloud Console, ve a tu VM
2. Click en "SSH" → "View gcloud command"
3. Usa el botón "Upload file" en la ventana SSH
4. Sube los archivos uno por uno

---

## Después de Subir

```bash
# En la VM:
cd ~/backend  # o ~/petFindnoborres/backend si subiste todo
ls -la  # Verificar que están los archivos

# Hacer scripts ejecutables
chmod +x ../deploy-vm.sh ../scripts/*.sh

# Configurar .env
nano .env  # Edita con tus credenciales

# Ejecutar deploy
cd ..
./deploy-vm.sh
```


