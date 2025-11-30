# 🔍 Diagnóstico: No se ven las mascotas

## Pasos para diagnosticar el problema

### 1. Verificar que estás autenticado

Abre la consola de desarrollo (Metro bundler) y busca estos mensajes:
- `🔍 Cargando mascotas para usuario: [ID]` - Si ves esto, el usuario está autenticado
- `Usuario no autenticado` - Si ves esto, necesitas iniciar sesión

**Solución**: Ve a la pestaña "Perfil" y verifica que estés logueado. Si no, inicia sesión.

### 2. Verificar la conexión con Supabase

En la consola, busca errores como:
- `Error cargando mascotas: [error]`
- `relation "pets" does not exist` - La tabla no existe
- `permission denied` - Problema con políticas RLS

**Solución**: 
- Verifica que Supabase esté configurado correctamente en `.env`
- Verifica que la tabla `pets` exista en Supabase
- Verifica las políticas RLS en Supabase

### 3. Verificar que tengas mascotas registradas

Ejecuta esta consulta en Supabase SQL Editor:

```sql
-- Ver todas las mascotas de tu usuario
SELECT * FROM pets 
WHERE owner_id = 'TU_USER_ID_AQUI'
ORDER BY created_at DESC;
```

**Solución**: Si no hay resultados, necesitas crear una mascota primero.

### 4. Verificar políticas RLS

Ejecuta esta consulta en Supabase SQL Editor:

```sql
-- Verificar políticas de la tabla pets
SELECT * FROM pg_policies 
WHERE tablename = 'pets';
```

Debe haber al menos una política que permita a los usuarios ver sus propias mascotas:

```sql
-- Si no existe, créala:
CREATE POLICY "Users can view all pets" ON pets 
FOR SELECT USING (true);

CREATE POLICY "Users can manage own pets" ON pets 
FOR ALL USING (auth.uid() = owner_id);
```

### 5. Verificar en la app

1. Abre la app y ve a "Mis Mascotas"
2. Si ves el mensaje "No tienes mascotas registradas aún", significa que:
   - Estás autenticado ✅
   - La conexión funciona ✅
   - Pero no tienes mascotas registradas

**Solución**: Necesitas crear una mascota. Por ahora, puedes hacerlo directamente en Supabase:

```sql
-- Crear una mascota de prueba (reemplaza TU_USER_ID)
INSERT INTO pets (owner_id, name, species, breed, color, size)
VALUES (
  'TU_USER_ID_AQUI',
  'Firulais',
  'dog',
  'Labrador',
  'Dorado',
  'large'
);
```

### 6. Verificar logs en la consola

En la consola de Metro, deberías ver:
- `✅ Mascotas cargadas: X` - Si hay mascotas
- `❌ Error cargando mascotas: [error]` - Si hay un error

### 7. Modo Debug

Si estás en modo desarrollo (`__DEV__ = true`), verás:
- Una tarjeta azul con información del usuario
- Un botón "Ver Info Debug" que muestra información en la consola

## Soluciones rápidas

### Si no estás autenticado:
1. Ve a "Perfil"
2. Inicia sesión o regístrate
3. Vuelve a "Mis Mascotas"

### Si hay error de conexión:
1. Verifica que Supabase esté configurado en `.env`
2. Verifica que la URL y la clave sean correctas
3. Reinicia la app

### Si no tienes mascotas:
1. Crea una mascota directamente en Supabase (ver SQL arriba)
2. O espera a que se implemente el formulario de creación

### Si hay error de permisos:
1. Ve a Supabase Dashboard → Authentication → Policies
2. Verifica que las políticas RLS estén correctas
3. Ejecuta el script SQL de políticas (ver arriba)

## Comandos útiles

```bash
# Ver logs de Metro
# (ya deberías tenerlos en la terminal donde corriste npm start)

# Verificar conexión a Supabase
# Abre Supabase Dashboard y verifica que las tablas existan

# Limpiar caché y reiniciar
npx expo start -c
```

## Información de Debug

Si presionas el botón "Ver Info Debug" (solo en desarrollo), verás en la consola:
- El objeto usuario completo
- El ID del usuario
- Si está autenticado o no

Esto te ayudará a identificar el problema específico.


