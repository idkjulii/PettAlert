# 🐳🚀 Guía Paso a Paso: Deploy en Docker y Google Cloud

## 📋 CHECKLIST INICIAL

Antes de comenzar, verifica que tienes:

- [ ] Cuenta de Google Cloud Platform activa
- [ ] Proyecto creado en GCP
- [ ] Credenciales de Supabase (URL y Service Key)
- [ ] Archivo `backend/.env` configurado (o `env.example` listo)
- [ ] Acceso a tu proyecto local

---

## 🏠 FASE 1: PREPARACIÓN LOCAL

### PASO 1.1: Verificar archivos necesarios

Verifica que tienes estos archivos:
- ✅ `backend/Dockerfile` 
- ✅ `backend/requirements.txt`
- ✅ `docker-compose.yml`
- ✅ `deploy-vm.sh`
- ✅ `backend/env.example`

### PASO 1.2: Crear archivo .env

Crea el archivo `backend/.env` con tus credenciales reales.

---

## ☁️ FASE 2: GOOGLE CLOUD - CREAR VM

### PASO 2.1: Acceder a Google Cloud Console
### PASO 2.2: Habilitar APIs
### PASO 2.3: Crear la VM
### PASO 2.4: Configurar Firewall

---

## 🔧 FASE 3: CONFIGURAR LA VM

### PASO 3.1: Conectarse por SSH
### PASO 3.2: Instalar Docker
### PASO 3.3: Instalar Docker Compose
### PASO 3.4: Verificar instalación

---

## 📤 FASE 4: SUBIR CÓDIGO

### PASO 4.1: Elegir método (Git o SCP)
### PASO 4.2: Subir archivos
### PASO 4.3: Verificar archivos en la VM

---

## ⚙️ FASE 5: CONFIGURAR EN LA VM

### PASO 5.1: Crear .env en la VM
### PASO 5.2: Configurar variables
### PASO 5.3: Verificar credenciales

---

## 🐳 FASE 6: DESPLEGAR CON DOCKER

### PASO 6.1: Hacer script ejecutable
### PASO 6.2: Ejecutar deploy
### PASO 6.3: Verificar contenedor
### PASO 6.4: Ver logs

---

## 🔥 FASE 7: CONFIGURAR ACCESO

### PASO 7.1: Configurar Firewall en GCP
### PASO 7.2: Obtener IP externa
### PASO 7.3: Probar acceso

---

## ✅ FASE 8: VERIFICACIÓN FINAL

### PASO 8.1: Probar endpoints
### PASO 8.2: Configurar IP estática
### PASO 8.3: Actualizar app móvil

---

¡Vamos paso a paso! 🚀


