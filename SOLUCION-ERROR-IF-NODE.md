# 🔧 Solución: Error "Wrong type" en Nodo If

## Error

```
Wrong type: '0.008283342234790325,0.06954317539930344...' is an object but was expecting a boolean [condition 0, item 0]
```

## Causa

El nodo "If" está usando el operador `exists` en `$json.body.embedding`, pero como el embedding es un **array** (objeto en JavaScript), n8n no puede evaluarlo correctamente como boolean.

## Soluciones

### ✅ Solución 1: Habilitar "Convert types where required" (Más fácil)

En el nodo "If":

1. Activa el toggle **"Convert types where required"** (ponlo en ON)
2. La condición seguirá siendo: `{{ $json.body.embedding }}` con operador `exists`
3. n8n automáticamente convertirá el array a boolean correctamente

### ✅ Solución 2: Cambiar la condición (Más explícita)

En lugar de usar `exists`, verifica si el embedding es un array no vacío:

**Condición:**
- **Left Value:** `={{ $json.body.embedding && Array.isArray($json.body.embedding) && $json.body.embedding.length > 0 }}`
- **Operator:** `equals`
- **Right Value:** `true`

O más simple:
- **Left Value:** `={{ $json.body.embedding?.length > 0 }}`
- **Operator:** `equals`
- **Right Value:** `true`

### ✅ Solución 3: Usar expresión booleana directa

**Left Value:** `={{ !!$json.body.embedding && $json.body.embedding.length > 0 }}`
- **Operator:** `equals`
- **Right Value:** `true`

## Recomendación

**Usa la Solución 1** (habilitar "Convert types where required") porque es la más simple y n8n manejará automáticamente la conversión.

## Configuración Final del Nodo If

```
Conditions:
├─ Left Value: {{ $json.body.embedding }}
├─ Operator: exists
└─ Convert types where required: ON ✅
```

Esto debería resolver el error y permitir que el nodo evalúe correctamente si el embedding existe.









