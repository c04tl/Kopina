from pathlib import Path
from PIL import Image, ImageOps
from string import ascii_lowercase
from random import choice
import argparse
from random import choice


EXTENSIONES_SOPORTADAS = {".jpg", ".jpeg", ".png", ".webp"}


def validar_calidad(calidad: int) -> int:
    """
    Valida que la calidad esté dentro del rango aceptado por Pillow.

    Args:
        calidad: Valor de calidad de compresión entre 1 y 100.

    Returns:
        El mismo valor de calidad si es válido.

    Raises:
        ValueError: Si la calidad está fuera del rango permitido.
    """
    if not 1 <= calidad <= 100:
        raise ValueError("La calidad debe estar entre 1 y 100.")

    return calidad

def validar_longitud_nombre(longitud: int) -> int:
    if not 5 <= longitud <= 50:
        raise ValueError("La longitud debe estar entre 5 y 50.")

    return longitud

def generar_nombre(longitud: int) -> str:
    return ''.join(choice(ascii_lowercase) for i in range(longitud))

def comprimir_imagen(
    ruta_imagen: Path,
    ruta_salida: Path,
    longitud_nombre: int = 10,
    calidad: int = 70,
    orientation: str = "keep",
    overwrite: bool = False
) -> None:
    """
    Comprime una imagen, elimina metadatos y la guarda en la ruta destino.

    Importante:
    - No se pasa `exif` al guardar, por lo que Pillow no conserva EXIF.
    - No se pasa `icc_profile`, por lo que también se elimina el perfil ICC.
    - Si orientation='keep', primero se aplica la orientación EXIF a los pixeles.

    Args:
        ruta_imagen: Ruta de la imagen original.
        ruta_salida: Ruta donde se guardará la imagen comprimida.
        calidad: Calidad de compresión entre 1 y 100.
        orientation: Política de orientación:
            - "keep": conserva la orientación visual aplicándola antes de borrar EXIF.
            - "strip": borra EXIF sin corregir orientación.
        overwrite: Si True, sobrescribe archivos existentes.
    """
    if ruta_salida.exists() and not overwrite:
        print(f"[SKIP] Ya existe: {ruta_salida}")
        return

    ruta_salida.parent.mkdir(parents=True, exist_ok=True)

    try:
        with Image.open(ruta_imagen) as img:
            # Corrige visualmente la orientación antes de borrar EXIF.
            if orientation == "keep":
                img = ImageOps.exif_transpose(img)

            # JPG/JPEG no soporta transparencia.
            # Si viene PNG/WEBP con alpha y sale como JPG, se convierte a RGB.
            if img.mode in ("RGBA", "P") and ruta_salida.suffix.lower() in {".jpg", ".jpeg"}:
                img = img.convert("RGB")

            # Al no pasar EXIF ni ICC, se eliminan metadatos sensibles.
            img.save(
                ruta_salida,
                optimize=True,
                quality=calidad
            )

            print(f"[OK] {ruta_imagen} -> {ruta_salida}")

    except Exception as error:
        print(f"[ERROR] No se pudo comprimir {ruta_imagen}: {error}")


def comprimir_directorio(
    origen: Path,
    destino: Path,
    longitud_nombre: int = 10,
    calidad: int = 70,
    orientation: str = "keep",
    recursive: bool = False,
    overwrite: bool = False
) -> None:
    """
    Comprime todas las imágenes soportadas dentro de un directorio.

    Args:
        origen: Carpeta con imágenes originales.
        destino: Carpeta donde se guardarán las imágenes comprimidas.
        calidad: Calidad de compresión entre 1 y 100.
        orientation: Política de orientación EXIF.
        recursive: Si True, procesa subcarpetas.
        overwrite: Si True, sobrescribe archivos existentes.

    Raises:
        FileNotFoundError: Si la carpeta origen no existe.
    """
    if not origen.exists():
        raise FileNotFoundError(f"No existe la carpeta origen: {origen}")

    archivos = origen.rglob("*") if recursive else origen.iterdir()

    for archivo in archivos:
        if archivo.is_file() and archivo.suffix.lower() in EXTENSIONES_SOPORTADAS:
            ruta_relativa = archivo.relative_to(origen)
            ruta_salida = destino / ruta_relativa

            comprimir_imagen(
                ruta_imagen=archivo,
                ruta_salida=ruta_salida,
                longitud_nombre=longitud_nombre,
                calidad=calidad,
                orientation=orientation,
                overwrite=overwrite
            )


def main() -> None:
    """
    Punto de entrada CLI de Kopina.
    """
    parser = argparse.ArgumentParser(
        description="Kopina viene del nahuatl y signifca sacar o extraer una cosa de otra - kopina es un compresor de imágenes con borrado de metadatos."
    )

    parser.add_argument(
        "--input",
        required=True,
        help="Ruta de imagen o carpeta de origen."
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Ruta de imagen o carpeta destino."
    )

    parser.add_argument(
        "--quality",
        type=int,
        default=70,
        help="Calidad de compresión entre 1 y 100. Default: 70."
    )

    parser.add_argument(
        "--orientation",
        choices=["keep", "strip"],
        default="keep",
        help=(
            "keep aplica orientación visual antes de borrar EXIF; "
            "strip borra EXIF sin corregir orientación."
        )
    )

    parser.add_argument(
        "--name",
        type=int,
        default=10,
        help="Longitud del nombre aleatorio del archivo entre 5 y 50. Default: 10."
    )

    parser.add_argument(
        "--recursive",
        action="store_true",
        help="Procesa imágenes dentro de subcarpetas."
    )

    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Sobrescribe archivos existentes en destino."
    )

    args = parser.parse_args()

    calidad = validar_calidad(args.quality)
    longitud = validar_longitud_nombre(args.name)
    entrada = Path(args.input)
    salida = Path(args.output)
    print("Longitud: ", longitud)

    if entrada.is_file():
        comprimir_imagen(
            ruta_imagen=entrada,
            ruta_salida=salida,
            longitud_nombre=longitud,
            calidad=calidad,
            orientation=args.orientation,
            overwrite=args.overwrite
        )

    elif entrada.is_dir():
        comprimir_directorio(
            origen=entrada,
            destino=salida,
            longitud_nombre=longitud,
            calidad=calidad,
            orientation=args.orientation,
            recursive=args.recursive,
            overwrite=args.overwrite
        )

    else:
        raise FileNotFoundError(f"La ruta de entrada no existe: {entrada}")


if __name__ == "__main__":
    main()