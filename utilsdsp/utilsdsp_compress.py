"""
Comprimir ficheros y directorios.
    - compress()
    - uncompress()
"""

from pathlib import Path
from shutil import make_archive, unpack_archive
from outputstyles import error, info, warning
from utilsdsp import validate_path, delete_dir


def compress(path_src: str | Path, path_dst: str | Path | None = None, compress_type: str = "zip", base_include: bool = True, overwrite: bool = False, delete_src: bool = False) -> str:
    """
    Comprimir un directorio o fichero.

    Parameters:
    path_src (str | Path): Ruta del directorio o fichero a comprimir.
    path_dst (str | Path | None) [Opcional]: Ruta donde guardar el fichero compactado.
    compress_type (str) [Opcional]: Tipo de comprimido (zip, tar, gztar, bztar o xztar).
    base_include (bool) [Opcional]: Incluir el directorio base en el comprimido.
    overwrite (bool) [Opcional]: Sobrescribir el fichero comprimido sí existe.
    delete_src (bool) [Opcional]: Eliminar el fichero o directorio de destino.

    Returns:
    str: Ruta absoluta del fichero comprimido.
    """

    # Comprobar que exista el directorio o fichero de origen.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()
    path_dst = Path(path_dst).resolve() if path_dst else path_src.parent

    # Obtener el nombre del directorio o fichero sin la extensión.
    file_name = path_src.stem

    # Ruta completa del fichero final comprimido.
    path_filecompress = path_dst / f'{file_name}.{compress_type}'

    # Comprobar que no exista el fichero comprimido en la ruta de destino.
    if path_filecompress.exists() and not overwrite:
        print(warning("Ya existe:", "ico"), info(path_filecompress))
        return

    # Procedemos a crear el fichero comprimido.
    try:

        # Comprimir sí es un ficheros o un directorio con la base incluida.
        if path_src.is_file() or base_include:

            result = make_archive(
                base_name=str(path_dst / file_name),
                format=compress_type,
                root_dir=path_src.parent,
                base_dir=path_src.name
            )

        # Comprimir un directorio sin la base.
        else:
            result = make_archive(
                base_name=str(path_dst / file_name),
                format=compress_type,
                root_dir=path_src
            )

        # Eliminar el fichero o directorio de destino.
        if delete_src:
            delete_dir(path_src)

        # Retornar la ruta absoluta del fichero comprimido.
        return result

    except Exception as err:

        print(error("No se pudo comprimir:", "ico"), info(path_src))
        print(err)


def uncompress(path_src: str | Path, path_dst: str | Path | None = None, delete_src: bool = False) -> str:
    """
    Descomprimir un fichero.

    Parameters:
    path_src (str | Path): Ruta del fichero comprimido.
    path_dst (str | Path | None) [Opcional]: Ruta a descomprimir el fichero.
    delete_src (bool) [Opcional]: Eliminar el fichero comprimido.

    Returns:
    str: Ruta absoluta del fichero o directorio descomprimido.
    """

    # Comprobar que exista el fichero comprimido.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()
    path_dst = Path(path_dst).resolve() if path_dst else path_src.parent

    # Comprobar que sea un fichero admitido.
    if not path_src.suffix in [".zip", ".tar", ".gztar", ".bztar", ".xztar"]:
        print(warning("Fichero no admitido:", "ico"), info(path_src))
        return

    # Procedemos a descomprimir el fichero.
    try:

        unpack_archive(path_src, path_dst)

        # Eliminar el fichero comprimido de destino.
        if delete_src:
            delete_dir(path_src)

        # Retornar la ruta absoluta del fichero comprimido.
        return str(path_dst / path_src.stem)

    except Exception as err:

        print(error("No se pudo descomprimir:", "ico"), info(path_src))
        print(err)
