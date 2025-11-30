# 🔧 Configuración de TypeScript para Edge Functions

Las Edge Functions de Supabase se ejecutan en **Deno**, no en Node.js. Esto significa que TypeScript puede mostrar errores en el IDE si no está configurado correctamente.

## ⚠️ Errores Comunes en el IDE

Si ves errores como:
- `Cannot find module 'https://deno.land/std@...'`
- `Cannot find name 'Deno'`
- `Parameter 'req' implicitly has an 'any' type`

**Estos errores son normales** y no afectan el funcionamiento real de las funciones en Supabase. Las funciones se ejecutan correctamente cuando se despliegan.

## ✅ Soluciones

### Opción 1: Instalar extensión de Deno para VS Code

1. Instala la extensión oficial de Deno:
   - Abre VS Code
   - Ve a Extensiones (Ctrl+Shift+X)
   - Busca "Deno" por denoland
   - Instala "Deno" de denoland

2. Habilita Deno para las funciones:
   - Abre la paleta de comandos (Ctrl+Shift+P)
   - Escribe "Deno: Enable Deno"
   - Selecciona la carpeta `supabase/functions`

### Opción 2: Ignorar errores (Recomendado)

Estos errores son cosméticos en el IDE. Las funciones funcionan correctamente cuando se despliegan porque Supabase las ejecuta en un entorno Deno real.

### Opción 3: Usar configuración de workspace

Ya existe un archivo `.vscode/settings.json` en `supabase/functions/` que configura Deno para esa carpeta.

## 🚀 Verificar que Funciona

Para verificar que las funciones están bien escritas:

```bash
# Probar localmente con Supabase CLI
supabase functions serve send-geo-alerts

# Desplegar a Supabase
supabase functions deploy send-geo-alerts
```

Si la función se despliega y funciona correctamente, entonces el código está bien, solo son errores del IDE.

## 📝 Notas

- Las Edge Functions **NO** se compilan con el proyecto React Native
- Solo se ejecutan en el servidor de Supabase
- Los errores del IDE son cosméticos y no afectan el deployment


