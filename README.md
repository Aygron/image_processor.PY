# Procesador de Imágenes

Un conjunto de herramientas potente y flexible para el procesamiento de imágenes, incluyendo conversión de formatos, eliminación de fondos y división de imágenes.

## Características

- **Conversión de Formatos**: Convierte entre varios formatos de imagen (BMP, PNG, etc.)
- **Eliminación de Fondos**: Elimina fondos de color sólido con transparencia
- **División de Imágenes**: Divide imágenes grandes en mosaicos más pequeños de igual tamaño
- **Procesamiento por Lotes**: Procesa múltiples archivos a la vez
- **Interfaz de Línea de Comandos**: CLI fácil de usar para automatización

## Instalación

1. Asegúrate de tener Python 3.6 o superior instalado
2. Instala el paquete:
   ```bash
   pip install -e .
   ```

## Uso

### Convertir Imágenes

Convertir todos los archivos BMP en un directorio a PNG:
```bash
python -m image_processor convert input/ output/ --input-ext .bmp --output-ext .png
```

Convertir y eliminar fondo negro:
```bash
python -m image_processor convert input/ output/ --remove-bg --bg-color 0,0,0
```

### Dividir Imágenes

Dividir una imagen en mosaicos de 100x100 píxeles:
```bash
python -m image_processor tile input.png output/ --tile-size 100,100
```

## Estructura del Proyecto

- `image_processor/` - Paquete principal
  - `__init__.py` - Inicialización del paquete
  - `core.py` - Funciones principales de procesamiento de imágenes
  - `cli.py` - Interfaz de línea de comandos
- `setup.py` - Package installation script
- `README.md` - This file

## License

MIT
