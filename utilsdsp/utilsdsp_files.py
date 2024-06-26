"""
Operaciones con ficheros.
    - read_file()
    - write_file()
"""

from pathlib import Path
from outputstyles import error, info, warning
from utilsdsp import create_dir, validate_path


def read_file(path_file: str | Path, by_line: bool = True) -> list | str:
    """
    Leer el contenido de un fichero.

    Parameters:
    path_file (str | Path): Ruta del fichero a leer.
    by_line (bool) [Opcional]: Leer el contenido por lineas.

    Returns:
    list | str: El contenido por líneas o un string con todo.
    """

    # Comprobar que exista el fichero.
    if not validate_path(path_file):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_file = Path(path_file).resolve()

    # Comprobar que sea un fichero.
    if not path_file.is_file():
        print(error("No es un fichero:", "ico"), info(path_file))
        return

    # Leer el contenido del fichero.
    try:

        # Retornar el resultado en una lista según las lineas.
        if by_line:
            return path_file.read_text("utf-8").split("\n")

        # Retornar el resultado en una cadena todo.
        return path_file.read_text("utf-8")

    except Exception as err:

        print(error("No se pudo leer el fichero:", "ico"), info(path_file))
        print(err)


def write_file(path_file: str | Path, content_write: str | list) -> str:
    """
    Escribir contenido dentro de un fichero.

    Parameters:
    path_file (str | Path): Ruta del fichero a escribir.
    content_write (str | list): Contenido que se va a guardar.

    Returns:
    str: Ruta del fichero guardado.
    """

    # Comprobar que el contenido no este vacio.
    if not content_write:
        print(warning("El contenido no puede estar vacio.", "ico"))
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_file = Path(path_file).resolve()

    # Comprobar sí existe y no es un fichero.
    if path_file.exists() and not path_file.is_file():
        print(warning("Ya existe y no es un fichero:", "ico"), info(path_file))
        return

    # Crear sí no existe la ruta padre.
    create_dir(path_file.parent)

    try:

        # Sí es una lista, lo escribimos por lineas.
        if isinstance(content_write, list):

            # Comprobar sí existe el fichero.
            if path_file.exists():

                # Leemos su contenido por lineas.
                content_file = read_file(path_file)

                # Agregamos el contenido a guardar.
                content_file.extend(content_write)

                content = content_file

            else:
                content = content_write

            # Convertir a string todo el contenido.
            content = [str(item) for item in content]

            # Escribimos el contenido en el fichero por lineas.
            path_file.write_text("\n".join(content), "utf-8")

        # Sí es un texto u otro, lo guardamos tal y como viene.
        else:

            # Comprobar sí existe el fichero.
            if path_file.exists():

                # Leemos su contenido como un string.
                content_file = read_file(path_file, by_line=False)

                # Agregamos el contenido a guardar.
                content = content_file + f'\n{content_write}'

            else:
                content = content_write

            # Escribimos el contenido en el fichero como un texto.
            path_file.write_text(content, "utf-8")

        # Retornar la ruta absoluta del fichero.
        return str(path_file)

    except Exception as err:

        print(error("Error al escribir en el fichero:", "ico"), info(path_file))
        print(err)
