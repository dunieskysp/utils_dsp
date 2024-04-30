"""
Obtener tamaño de ficheros y directorios.
    - natural_size()
    - obtain_sizedir()
    - obtain_sizefile()
    - obtain_size()
"""

import os
from pathlib import Path
from outputstyles import error, info, warning
from utilsdsp import validate_path


def natural_size(size_file: int, unit: str | None = None) -> str:
    """
    Convertir los bytes a medidas más legibles (KB, MB, GB o TB).

    Parameters:
    size_file (int): Tamaño del fichero en bytes.
    unit (str | None) [Opcional]: Unidad para dar el resulado.
    - KB, MB, GB o TB

    Returns:
    srt: Devuelve el tamaño del fichero en bytes, KB, MB, GB o TB.
    """

    # Comprobar que sea válido el tamaño del fichero o directorio.
    if not isinstance(size_file, int):
        return warning("El tamaño debe ser un número y mayor que 0.", "ico")

    if size_file <= 0:
        return "0 bytes"

    # Unidades y sus valores en que se va a expresar el resultado.
    units = {
        "TB": 1024 ** 4,
        "GB": 1024 ** 3,
        "MB": 1024 ** 2,
        "KB": 1024,
        "BYTES": 1
    }

    # Poner en mayúscula la unidad del argumento.
    unit = unit.upper() if unit and isinstance(unit, str) else ""

    # Si la unidad introducida es válida.
    if unit in units:

        # Convertir el tamaño a esa unidad.
        size = size_file / units[unit]

    else:

        # Buscar la medida más acorde según la cantidad de bytes.
        for unit, value in units.items():

            if size_file >= value:

                size = size_file / value

                break

    # Retornamos el tamaño obtenido redondeado y con su Unidad.
    return f'{round(size, 2)} {unit.lower() if unit == "BYTES" else unit}'


def obtain_sizedir(path_src: str | Path, unit: str | None = None, file_type: str = "*") -> str:
    """
    Obtener tamaño de un directorio con "Path().rglob()" y "Path().stat()".

    Parameters:
    path_src (str | Path): Ruta del directorio para determinar su tamaño.
    unit (str | None) [Opcional]: Unidad para dar el resulado (KB, MB, GB o TB).
    file_type (str) [Opcional]: Tipos de ficheros a seleccionar.

    Returns:
    str: Suma del tamaño de todos los ficheros con su unidad de medida.
    """

    # Comprobar que exista el directorio.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()

    # Comprobar que sea un directorio.
    if not path_src.is_dir():
        return f'{error("No es un directorio:", "ico")} {info(path_src)}'

    # Obtener la suma del tamaño de todos los fichero.
    total_size = sum(
        [
            file.stat().st_size for file in path_src.rglob(f'*.{file_type}')
        ]
    )

    # Retornar el tamaño total con su unidad de medida.
    return natural_size(total_size, unit) if total_size else "0 bytes"


def obtain_sizefile(path_src: str | Path, unit: str | None = None, metod_stat: bool = False, metod_getsize: bool = False) -> str:
    """
    Obtener tamaño de un fichero.

    Parameters:
    path_src (str | Path): Ruta del fichero a determinar su tamaño.
    unit (str | None) [Opcional]: Unidad para dar el resulado (KB, MB, GB o TB).
    metod_stat (bool) [Opcional]: Usar os.stat() para determinar el tamaño.
    metod_getsize (bool) [Opcional]: Usar os.path.getsize() para determinar el tamaño.

    Returns:
    str: Tamaño del fichero con su unidad de medida.
    """

    # Comprobar que exista el fichero.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()

    # Comprobar que sea un fichero.
    if not path_src.is_file():
        return f'{error("No es un fichero:", "ico")} {info(path_src)}'

    # Método 01: os.stat().
    if metod_stat:
        return natural_size(os.stat(path_src).st_size, unit)

    # Método 02: os.path.getsize().
    elif metod_getsize:
        return natural_size(os.path.getsize(path_src), unit)

    # Método 03: Path.stat().
    return natural_size(path_src.stat().st_size, unit)


def obtain_size(path_src: str | Path, unit: str | None = None, file_type: str = "*") -> str:
    """
    Obtener tamaño de un fichero o directorio.

    Parameters:
    path_src (str | Path): Ruta del fichero o directorio a determinar su tamaño.
    unit (str | None) [Opcional]: Unidad para dar el resulado (KB, MB, GB o TB).
    file_type (str) [Opcional]: Tipos de ficheros a seleccionar.

    Returns:
    str: Tamaño del fichero o directorio con su unidad de medida.
    """

    # Comprobar que exista el directorio o fichero.
    if not validate_path(path_src):
        return

    # Sí es un fichero.
    if Path(path_src).is_file():
        return obtain_sizefile(path_src, unit)

    # Si es un directorio.
    return obtain_sizedir(path_src, unit, file_type)
