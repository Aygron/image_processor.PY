"""
Funcionalidad principal de procesamiento de imágenes.

Este módulo proporciona las funciones principales para el procesamiento de imágenes,
incluyendo conversión de formatos, eliminación de fondos y operaciones de división de imágenes.
"""

import os
from pathlib import Path
from typing import Tuple, Optional, Union, Generator
from PIL import Image, ImageFile

# Enable loading of truncated images
ImageFile.LOAD_TRUNCATED_IMAGES = True

class ImageProcessorError(Exception):
    """Excepción base para errores de procesamiento de imágenes."""
    pass

def ensure_directory_exists(directory: Union[str, Path]) -> Path:
    """Asegura que el directorio especificado exista, creándolo si es necesario.
    
    Args:
        directory: Ruta al directorio
        
    Returns:
        Path: La ruta del directorio como un objeto Path
        
    Raises:
        ImageProcessorError: Si no se puede crear el directorio
    """
    try:
        path = Path(directory)
        path.mkdir(parents=True, exist_ok=True)
        return path
    except Exception as e:
        raise ImageProcessorError(f"Failed to create directory {directory}: {str(e)}")

def convert_image(
    input_path: Union[str, Path],
    output_path: Union[str, Path],
    output_format: str = 'PNG',
    remove_bg: bool = False,
    bg_color: Optional[Tuple[int, int, int]] = None
) -> None:
    """Convierte una imagen a otro formato con opción de eliminar el fondo.
    
    Args:
        input_path: Ruta a la imagen de entrada
        output_path: Ruta donde se guardará la imagen convertida
        output_format: Formato de salida (ej. 'PNG', 'BMP')
        remove_bg: Si se debe eliminar el fondo
        bg_color: Color del fondo a eliminar (tupla RGB). Si es None, usa (0,0,0) si remove_bg es True
        
    Raises:
        ImageProcessorError: Si falla la conversión
    """
    try:
        with Image.open(input_path) as img:
            # Convert to RGBA to support transparency
            img = img.convert('RGBA')
            
            if remove_bg:
                bg_color = bg_color or (0, 0, 0)
                datas = img.getdata()
                new_data = []
                
                for item in datas:
                    # Change the specified background color to transparent
                    if item[:3] == bg_color:
                        new_data.append((255, 255, 255, 0))
                    else:
                        new_data.append(item)
                
                img.putdata(new_data)
            
            # Ensure output directory exists
            output_path = Path(output_path)
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            img.save(output_path, output_format)
    except Exception as e:
        raise ImageProcessorError(f"Failed to convert {input_path}: {str(e)}")

def batch_convert(
    input_dir: Union[str, Path],
    output_dir: Union[str, Path],
    input_ext: str = '.bmp',
    output_ext: str = '.png',
    remove_bg: bool = False,
    bg_color: Optional[Tuple[int, int, int]] = None
) -> None:
    """Convierte múltiples imágenes en un directorio.
    
    Args:
        input_dir: Directorio que contiene las imágenes de entrada
        output_dir: Directorio donde se guardarán las imágenes convertidas
        input_ext: Extensión de archivo para filtrar los archivos de entrada
        output_ext: Extensión de archivo de salida
        remove_bg: Si se debe eliminar el fondo
        bg_color: Color del fondo a eliminar (tupla RGB)
    """
    input_dir = Path(input_dir)
    output_dir = ensure_directory_exists(output_dir)
    
    for img_file in input_dir.glob(f'*{input_ext}'):
        if img_file.is_file():
            output_path = output_dir / f"{img_file.stem}{output_ext}"
            convert_image(
                img_file, 
                output_path,
                output_ext[1:].upper(),
                remove_bg,
                bg_color
            )

def tile_image(
    input_path: Union[str, Path],
    output_dir: Union[str, Path],
    tile_size: Tuple[int, int] = (145, 145),
    output_ext: str = '.png'
) -> Generator[Path, None, None]:
    """Divide una imagen en mosaicos más pequeños.
    
    Args:
        input_path: Ruta a la imagen de entrada
        output_dir: Directorio donde se guardarán los mosaicos
        tile_size: Tamaño de cada mosaico (ancho, alto)
        output_ext: Extensión de archivo de salida
        
    Yields:
        Path: Ruta a cada mosaico creado
    """
    try:
        with Image.open(input_path) as img:
            img_width, img_height = img.size
            tile_width, tile_height = tile_size
            
            # Calculate number of tiles in each dimension
            x_tiles = img_width // tile_width
            y_tiles = img_height // tile_height
            
            # Ensure output directory exists
            output_dir = ensure_directory_exists(output_dir)
            base_name = Path(input_path).stem
            
            for i in range(x_tiles):
                for j in range(y_tiles):
                    left = i * tile_width
                    upper = j * tile_height
                    right = left + tile_width
                    lower = upper + tile_height
                    
                    # Crop the tile
                    tile = img.crop((left, upper, right, lower))
                    
                    # Save the tile
                    output_path = output_dir / f"{base_name}_{i}_{j}{output_ext}"
                    tile.save(output_path, output_ext[1:].upper())
                    yield output_path
                    
    except Exception as e:
        raise ImageProcessorError(f"Failed to tile image {input_path}: {str(e)}")
