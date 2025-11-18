# Ejecutar Pruebas del Backend

## Desde el directorio backend

Para ejecutar las pruebas desde el directorio `backend/`, usa:

```bash
python -m pytest ../tests/backend/unit/ -v
```

## Desde la raíz del proyecto

Para ejecutar las pruebas desde la raíz del proyecto:

```bash
cd backend
python -m pytest ../tests/backend/unit/ -v
```

O desde la raíz:

```bash
python -m pytest tests/backend/unit/ -v
```

## Nota sobre archivos antiguos

Los archivos `test_embedding_generation.py` y `test_real_embedding.py` en el directorio `backend/` son scripts de prueba antiguos y están excluidos de pytest. Si necesitas ejecutarlos, hazlo directamente:

```bash
python test_embedding_generation.py
```

## Estructura de pruebas

Las pruebas unitarias están organizadas en:
- `tests/backend/unit/` - Pruebas unitarias de APIs
- `tests/backend/conftest.py` - Configuración y fixtures compartidas
- `tests/backend/pytest.ini` - Configuración de pytest


