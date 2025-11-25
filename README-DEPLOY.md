# 📦 Archivos de Deploy

Este proyecto incluye varios archivos para facilitar el deploy en Google Cloud VM.

## 📄 Archivos Creados

### Configuración Docker
- **`backend/Dockerfile`**: Imagen Docker del backend Python/FastAPI
- **`backend/.dockerignore`**: Archivos a excluir de la imagen Docker
- **`docker-compose.yml`**: Orquestación de contenedores
- **`backend/.env.production`**: Plantilla de variables de entorno para producción

### Scripts de Deploy
- **`deploy-vm.sh`**: Script principal de deploy (automatizado)
- **`scripts/setup-vm.sh`**: Configuración inicial de la VM (instala Docker, etc.)
- **`scripts/monitor.sh`**: Monitoreo del estado del backend
- **`scripts/update-backend.sh`**: Actualizar código y reiniciar
- **`scripts/backup.sh`**: Backup de configuración

### Documentación
- **`GUIA-DEPLOY-GOOGLE-CLOUD.md`**: Guía completa paso a paso (LÉELA PRIMERO)
- **`DEPLOY-RAPIDO.md`**: Guía resumida de referencia rápida
- **`README-DEPLOY.md`**: Este archivo

---

## 🚀 ¿Por Dónde Empezar?

### Si es tu primera vez:
1. Lee **`GUIA-DEPLOY-GOOGLE-CLOUD.md`** - Tiene todo explicado detalladamente
2. Sigue los pasos uno por uno

### Si ya conoces GCP:
1. Lee **`DEPLOY-RAPIDO.md`** - Resumen de comandos
2. Ejecuta los scripts

---

## 🔧 Uso de los Scripts

### 1. Primera configuración de la VM
```bash
# En la VM (después de conectarte por SSH)
./scripts/setup-vm.sh
```
Este script instala Docker, Docker Compose, configura firewall, etc.

### 2. Deploy inicial
```bash
# Después de configurar .env y credenciales
./deploy-vm.sh
```
Construye la imagen, inicia el contenedor y verifica el servicio.

### 3. Monitoreo
```bash
# Ver estado del backend
./scripts/monitor.sh
```
Muestra estado del contenedor, recursos, logs, etc.

### 4. Actualizar código
```bash
# Después de hacer cambios en el código
./scripts/update-backend.sh
```
Descarga cambios (si usas Git), reconstruye y reinicia.

### 5. Backup
```bash
# Respaldar configuración
./scripts/backup.sh
```
Guarda .env, credenciales, etc.

---

## 📋 Checklist de Deploy

### Antes de empezar:
- [ ] Tienes cuenta de Google Cloud Platform
- [ ] Proyecto creado en GCP
- [ ] Credenciales de Supabase (URL + Service Key)
- [ ] Archivo `google-vision-key.json` de Google Cloud Vision

### En GCP:
- [ ] VM creada (e2-medium, Ubuntu 22.04)
- [ ] Firewall configurado (puerto 8003)
- [ ] Tag `petalert-backend` agregado a la VM

### En la VM:
- [ ] Docker instalado (`setup-vm.sh`)
- [ ] Proyecto clonado/subido
- [ ] Archivo `backend/.env` configurado
- [ ] Archivo `backend/google-vision-key.json` subido
- [ ] Deploy ejecutado (`deploy-vm.sh`)

### Verificación:
- [ ] `curl http://localhost:8003/health` responde OK
- [ ] Puedes acceder desde tu PC: `http://IP_PUBLICA:8003/health`
- [ ] La app móvil se conecta al backend

---

## 🌐 Arquitectura del Deploy

```
┌─────────────────────────────────────────────────┐
│         Google Cloud VM (Ubuntu 22.04)          │
│                                                 │
│  ┌───────────────────────────────────────────┐ │
│  │         Docker Container                   │ │
│  │                                            │ │
│  │  ┌──────────────────────────────────┐    │ │
│  │  │   FastAPI Backend (Python)       │    │ │
│  │  │   - Puerto: 8003                 │    │ │
│  │  │   - Google Vision API            │    │ │
│  │  │   - Embeddings (ML)              │    │ │
│  │  └──────────────────────────────────┘    │ │
│  │                 ↓                          │ │
│  │        uvicorn (ASGI server)              │ │
│  └───────────────────────────────────────────┘ │
│                   ↓                             │
│         Puerto 8003 expuesto                    │
└─────────────────────────────────────────────────┘
                    ↓
            Firewall (puerto 8003)
                    ↓
        ┌─────────────────────────┐
        │  Internet / App Móvil   │
        └─────────────────────────┘
                    ↓
        ┌─────────────────────────┐
        │     Supabase Cloud      │
        │  (PostgreSQL + Storage) │
        └─────────────────────────┘
```

---

## 🔍 Variables de Entorno

### Backend (`backend/.env`)
```bash
SUPABASE_URL=                    # URL de tu proyecto Supabase
SUPABASE_SERVICE_KEY=            # Service role key de Supabase
ALLOWED_ORIGINS=*                # Orígenes permitidos (CORS)
GENERATE_EMBEDDINGS_LOCALLY=true # Generar embeddings con ML local
GOOGLE_APPLICATION_CREDENTIALS=  # Ruta a credenciales (automático en Docker)
```

### Frontend (tu app móvil)
```bash
EXPO_PUBLIC_BACKEND_URL=http://IP_PUBLICA:8003  # URL del backend en GCP
EXPO_PUBLIC_SUPABASE_URL=                       # URL de Supabase (igual que backend)
EXPO_PUBLIC_SUPABASE_ANON_KEY=                  # Anon key de Supabase
```

---

## 💰 Costos Estimados

### Configuración Mínima (e2-medium)
- **VM e2-medium**: $24/mes (2 vCPU, 4GB RAM)
- **Disco 50GB**: $8/mes
- **Tráfico**: Variable (~$5-10/mes)
- **Total**: ~$40/mes

### Configuración Recomendada (e2-standard-2)
- **VM e2-standard-2**: $49/mes (2 vCPU, 8GB RAM)
- **Disco 50GB**: $8/mes
- **Tráfico**: Variable (~$5-10/mes)
- **Total**: ~$65/mes

💡 **Tip**: Google Cloud ofrece $300 USD en créditos para nuevos usuarios (válido por 90 días).

---

## 🔒 Seguridad

### Recomendaciones:
1. **Usar HTTPS** en producción (certificado SSL)
2. **Restringir ALLOWED_ORIGINS** a tu dominio específico
3. **No commitear** `.env` ni `google-vision-key.json` a Git
4. **Backups regulares** de la configuración
5. **Actualizar** regularmente el sistema y dependencias

### Firewall:
El puerto 8003 está expuesto a internet. En producción:
- Considera usar un proxy reverso (Nginx)
- Configura rate limiting
- Usa Cloudflare o similar para DDoS protection

---

## 🐛 Troubleshooting

### El servicio no inicia
```bash
# Ver logs detallados
docker-compose logs backend

# Verificar configuración
docker-compose config

# Reiniciar Docker
sudo systemctl restart docker
docker-compose up -d
```

### No puedo acceder desde internet
```bash
# Verificar firewall de GCP
gcloud compute firewall-rules list

# Verificar que el puerto está abierto
sudo ufw status

# Verificar que el servicio escucha
sudo netstat -tlnp | grep 8003
```

### Problemas de memoria
```bash
# Ver uso de memoria
free -h

# Ver logs del contenedor
docker stats

# Considerar: 
# - Agregar swap (scripts/setup-vm.sh lo hace)
# - Cambiar a VM con más RAM
```

### Google Vision API no funciona
```bash
# Verificar que el archivo existe
ls -la backend/google-vision-key.json

# Verificar que está en el contenedor
docker-compose exec backend ls -la /app/google-vision-key.json

# Ver logs específicos
docker-compose logs backend | grep -i vision
```

---

## 📞 Soporte

Si tienes problemas:

1. **Revisa los logs**: `docker-compose logs -f backend`
2. **Verifica la guía completa**: `GUIA-DEPLOY-GOOGLE-CLOUD.md`
3. **Ejecuta el monitor**: `./scripts/monitor.sh`
4. **Revisa el health check**: `curl http://localhost:8003/health`

---

## 🎯 Próximos Pasos (Opcional)

### Mejoras de Producción:
1. **Dominio personalizado**: Registra un dominio (ej: api.tuapp.com)
2. **HTTPS**: Configura certificado SSL con Let's Encrypt
3. **CI/CD**: Automatiza deploys con GitHub Actions
4. **Monitoreo**: Cloud Monitoring de GCP o Datadog
5. **Backup automático**: Configura backups diarios
6. **Load Balancer**: Para alta disponibilidad

### Optimizaciones:
1. **CDN**: Para archivos estáticos (imágenes)
2. **Cache**: Redis para respuestas frecuentes
3. **Autoscaling**: Escala automática según demanda
4. **Logging**: Cloud Logging centralizado

---

¡Listo para deploy! 🚀

Si es tu primera vez, comienza con **`GUIA-DEPLOY-GOOGLE-CLOUD.md`**.




