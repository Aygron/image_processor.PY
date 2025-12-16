"""
Interfaz de Línea de Comandos para el Procesador de Imágenes.

Este módulo proporciona una interfaz de línea de comandos para las herramientas de procesamiento de imágenes.
"""

import argparse
import sys
from pathlib import Path
from typing import Optional, List

from .core import batch_convert, tile_image, ImageProcessorError

def create_parser() -> argparse.ArgumentParser:
    """Crea y configura el analizador de argumentos."""
    parser = argparse.ArgumentParser(
        description='Herramientas de Procesamiento de Imágenes',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Ejemplos:
  # Convertir todos los archivos BMP a PNG
  python -m image_processor convert input/ output/ --input-ext .bmp --output-ext .png
  
  # Convertir y eliminar fondo negro
  python -m image_processor convert input/ output/ --remove-bg --bg-color 0,0,0
  
  # Dividir una imagen en mosaicos
  python -m image_processor tile input.png output/ --tile-size 100,100
'''
    )
    
    subparsers = parser.add_subparsers(dest='comando', help='Comando a ejecutar')
    
    # Comando convertir
    convert_parser = subparsers.add_parser('convert', help='Convertir imágenes entre formatos')
    convert_parser.add_argument('entrada', help='Archivo o directorio de entrada')
    convert_parser.add_argument('salida', help='Directorio de salida')
    convert_parser.add_argument('--input-ext', default='.bmp', help='Extensión de archivo de entrada (predeterminado: .bmp)')
    convert_parser.add_argument('--output-ext', default='.png', help='Extensión de archivo de salida (predeterminado: .png)')
    convert_parser.add_argument('--remove-bg', action='store_true', help='Eliminar fondo')
    convert_parser.add_argument('--bg-color', help='Color de fondo como R,G,B (ejemplo: 255,255,255)')
    
    # Comando tile
    tile_parser = subparsers.add_parser('tile', help='Dividir imagen en mosaicos')
    tile_parser.add_argument('entrada', help='Archivo de imagen de entrada')
    tile_parser.add_argument('salida', help='Directorio de salida para los mosaicos')
    tile_parser.add_argument('--tile-size', default='145,145', 
                           help='Tamaño del mosaico como ANCHO,ALTO (predeterminado: 145,145)')
    tile_parser.add_argument('--output-ext', default='.png', 
                           help='Extensión de archivo de salida (predeterminado: .png)')
    
    return parser

def parse_bg_color(color_str: Optional[str]) -> Optional[tuple]:
    """Analiza el color de fondo a partir de una cadena."""
    if not color_str:
        return None
    try:
        r, g, b = map(int, color_str.split(','))
        return (r, g, b)
    except (ValueError, AttributeError):
        raise ValueError(f"Formato de color inválido: {color_str}. Se espera R,G,B (ejemplo: 255,255,255)")

def parse_tile_size(size_str: str) -> tuple:
    """Analiza el tamaño del mosaico a partir de una cadena."""
    try:
        width, height = map(int, size_str.split(','))
        if width <= 0 or height <= 0:
            raise ValueError("Las dimensiones del mosaico deben ser números enteros positivos")
        return (width, height)
    except (ValueError, AttributeError):
        raise ValueError(f"Formato de tamaño inválido: {size_str}. Se espera ANCHO,ALTO (ejemplo: 100,100)")

def main(args: Optional[List[str]] = None) -> int:
    """Punto de entrada principal para la interfaz de línea de comandos."""
    parser = create_parser()
    
    if args is None:
        args = sys.argv[1:]
    
    if not args:
        parser.print_help()
        return 0
        
    parsed_args = parser.parse_args(args)
    
    try:
        if parsed_args.comando == 'convert':
            bg_color = parse_bg_color(parsed_args.bg_color)
            
            if Path(parsed_args.entrada).is_file():
                # Conversión de un solo archivo
                output_path = Path(parsed_args.salida) / f"{Path(parsed_args.entrada).stem}{parsed_args.output_ext}"
                batch_convert(
                    input_dir=Path(parsed_args.entrada).parent,
                    output_dir=Path(parsed_args.salida).parent,
                    input_ext=Path(parsed_args.entrada).suffix,
                    output_ext=parsed_args.output_ext,
                    remove_bg=parsed_args.remove_bg,
                    bg_color=bg_color
                )
            else:
                # Conversión por lotes
                batch_convert(
                    input_dir=parsed_args.entrada,
                    output_dir=parsed_args.salida,
                    input_ext=parsed_args.input_ext,
                    output_ext=parsed_args.output_ext,
                    remove_bg=parsed_args.remove_bg,
                    bg_color=bg_color
                )
                
        elif parsed_args.comando == 'tile':
            tile_size = parse_tile_size(parsed_args.tile_size)
            for _ in tile_image(
                input_path=parsed_args.entrada,
                output_dir=parsed_args.salida,
                tile_size=tile_size,
                output_ext=parsed_args.output_ext
            ):
                pass  # Solo iterar a través del generador
                
        else:
            parser.print_help()
            return 1
            
    except (ImageProcessorError, ValueError) as e:
        print(f"Error: {str(e)}", file=sys.stderr)
        return 1
    except KeyboardInterrupt:
        print("\nOperación cancelada por el usuario.", file=sys.stderr)
        return 1
        
    return 0

if __name__ == '__main__':
    sys.exit(main())
