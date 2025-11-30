# ✅ Solución: Timeouts de Conexión en Windows (WinError 10060)

## 🔴 Problema
El backend experimentaba timeouts al conectarse a Supabase desde Windows:
```
[WinError 10060] Se produjo un error durante el intento de conexión ya que 
la parte conectada no respondió adecuadamente tras un periodo de tiempo
```

## ✅ Cambios Realizados

### 1. Timeouts Aumentados en `backend/utils/supabase_client.py`

**Antes:**
- Connect timeout: 10 segundos
- Pool timeout: 5 segundos

**Ahora:**
- Connect timeout: **60 segundos** (6x más tiempo)
- Pool timeout: **10 segundos** (2x más tiempo)

Esto permite que Windows tenga suficiente tiempo para establecer conexiones a través de firewalls/antivirus.

### 2. Soporte para Storage Client

Se añadió configuración de timeout también para el cliente de almacenamiento de Supabase, usado para descargar imágenes.

### 3. Retry Logic en Generación de Embeddings

Actualizado `backend/routers/reports.py` para incluir:
- **3 reintentos automáticos** en caso de timeout
- **Backoff exponencial**: 1s, 2s, 4s entre reintentos
- **Timeout de 60 segundos** para descargar imágenes
- Mejor logging para diagnosticar problemas

## 🔄 Próximos Pasos

### 1. Reiniciar el Backend

En tu terminal de backend (presiona `Ctrl+C` para detenerlo primero):

```powershell
cd backend
uvicorn main:app --reload --port 8003 --host 0.0.0.0
```

El backend detectará automáticamente los cambios y recargará.

### 2. Verificar que Funciona

Deberías ver estos logs al iniciar:
```
OK: Variables de Supabase cargadas desde ...
✅ Cliente de Supabase creado con configuración optimizada
```

### 3. Probar desde la App

1. Abre la app en tu teléfono
2. Trata de crear un nuevo reporte con una foto
3. Los logs del backend deberían mostrar:
   ```
   🔄 [embedding] Generando embedding para reporte ...
   🔍 Embedding generado: XXXX bytes de imagen descargados
   🔍 Embedding generado: 1536 dimensiones
   ✅ [embedding] Embedding guardado exitosamente
   ```

## 🐛 Si Aún Hay Problemas

### Opción A: Verificar Firewall/Antivirus
El firewall o antivirus de Windows podría estar bloqueando las conexiones a Supabase. Intenta:
1. Desactivar temporalmente el firewall
2. Añadir una excepción para Python
3. Verificar configuración de proxy

### Opción B: Probar Conexión Directa
Verifica que puedes conectarte a Supabase:
```powershell
curl https://eamsbroadstwkrkjcuvo.supabase.co
```

### Opción C: Aumentar Timeout Aún Más
Si 60 segundos no es suficiente, edita `backend/utils/supabase_client.py` línea 41:
```python
connect=120.0,  # Aumentar a 2 minutos
```

## 📊 Configuración Actual

| Parámetro | Valor |
|-----------|-------|
| Connect Timeout | 60 segundos |
| Read/Write Timeout | 30 segundos (configurable) |
| Pool Timeout | 10 segundos |
| Max Reintentos (embeddings) | 3 intentos |
| Backoff entre Reintentos | Exponencial (1s, 2s, 4s) |

## 🎯 Logs Esperados

### ✅ Éxito:
```
🔄 [embedding] Generando embedding para reporte ...
🔍 Embedding generado: 245678 bytes de imagen descargados
🔍 Embedding generado: 1536 dimensiones
✅ [embedding] Embedding guardado exitosamente
```

### ⚠️ Reintento:
```
⏱️ [embedding] Timeout al procesar imagen (intento 1/3)
🔄 [embedding] Reintento 2/3 para reporte ...
✅ [embedding] Embedding guardado exitosamente
```

### ❌ Error Persistente:
```
⏱️ [embedding] Timeout al procesar imagen (intento 3/3)
❌ [embedding] Error después de 3 intentos: Timeout
```

Si ves errores persistentes después de estos cambios, puede ser un problema de red más profundo que requiere investigar la configuración de Windows o la red.




