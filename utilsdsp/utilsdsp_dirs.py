"""
Operaciones con directorios.
    - create_dir()
    - create_downloadsdir()
    - create_symboliclink()
    - delete_dir()
    - select_files()
    - prepare_paths()
    - move_dir()
    - move_files()
    - copy_dir()
    - rename_dir()
"""

import os
from pathlib import Path
from shutil import rmtree, move, copyfile, copytree
from outputstyles import error, success, warning, info, bold
from utilsdsp import obtain_defaultpath, obtain_downloadspath, validate_path


# NOTE: Crear directorios.
def create_dir(path_src: str | object, parents: bool = True, print_msg: bool = False) -> str:
    """
    Crear Directorio(s).

    Parameters:
    path_src (str | object Path): Ruta del directorio(s) a crear.
    parents (bool) [Opcional]: Crear o no la ruta padre si no existe.
    print_msg (bool) [Opcional]: Imprimir mensajes satisfactorios.

    Returns:
    str: Ruta absoluta del directorio(s) creado(s).
    """

    # Comprobar que no este vacia la ruta.
    if not path_src:
        print(warning("Debe insertar una ruta.", "ico"))
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()

    try:

        # Crear el nuevo directorio recursivamente o no.
        path_src.mkdir(parents=parents)

        # Imprimir mensaje satisfatorio.
        if print_msg:
            print(success("Creado:", "ico"), info(path_src))

        return str(path_src)

    # Si el directorio ya existía.
    except FileExistsError:

        # Imprimir mensaje de advertencia.
        if print_msg:
            print(warning("Ya existe:", "ico"), info(path_src))

        return str(path_src)

    # Si los directorios padres no existen.
    except FileNotFoundError as err:

        # Imprimir mensaje de error.
        print(error("No existe el directorio padre:", "ico"),
              info(path_src.parent))
        print(err)

    # Sí no se pudo crear el directorio.
    except OSError as err:

        # Imprimir mensaje de error.
        print(error("Error al crear:", "btn_ico"), info(path_src))
        print(err)


def create_downloadsdir(input_dir: str = "", mount_GDrive: bool = False, print_msg: bool = False) -> str:
    """
    Crear el directorio de descargas.

    Parameters:
    input_dir (str) [Opcional]: Directorio para guardar las descargas.
    mount_GDrive (bool) [Opcional]: Está montado GDriver o no.
    print_msg (bool) [Opcional]: Imprimir mensaje al crear el directorio.

    Returns:
    str: Ruta absoluta del directorio de descargas.
    """

    # Obtener la ruta padre por defecto.
    default_path = obtain_defaultpath(mount_GDrive)

    # Obtener la ruta para guardar las descargas.
    downloads_path = obtain_downloadspath(input_dir, mount_GDrive)

    # Crear el directorio de descargas.
    downloads_dir = create_dir(downloads_path, print_msg=print_msg)

    # En caso de que haya ocurrido algún error al crear el directorio.
    if not downloads_dir:

        # Advertir que se va a usar la ruta por defecto.
        print(
            warning("Se va a usar:", "ico"),
            info(default_path)
        )

        # Retornar la ruta padre por defecto.
        return default_path

    # Retornar la ruta del directorio creado.
    return downloads_dir


def create_symboliclink(path_src: str, path_dst: str, delete_dst: bool = False) -> str:
    """
    Crear enlace simbólico.

    Parameters:
    path_src (str): Ruta del directorio o fichero original.
    path_dst (str): Ruta del directorio a crear el enlace simbólico.
    delete_dst (bool) [Opcional]: Borrar el destino sí existe.

    Returns:
    str: Ruta absoluta del enlace simbólico.
    """

    # Comprobar que existan las rutas.
    if not (validate_path(path_src) and validate_path(path_dst)):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()
    path_dst = Path(path_dst).resolve()

    # Ruta absoluta del enlace simbólico.
    path_symboliclink = path_dst / path_src.name

    # Comprobar si existe el destino y no se puede borrar.
    if path_symboliclink.exists() and not delete_dst:

        print(warning("Ya existe:", "ico"), info(path_symboliclink))

        return

    # Comprobar si existe el destino y borrarlo.
    if path_symboliclink.exists():

        # Eliminar enlace símbolico.
        if path_symboliclink.is_symlink():

            path_symboliclink.unlink()

        # Eliminar fichero o directorio.
        else:

            delete_dir(path_symboliclink)

    # Crear el enlace símbolico.
    try:

        path_symboliclink.symlink_to(path_src)

        return path_symboliclink

    except Exception as err:

        print(
            error("Error al crear el enlace simbólico en:", "ico"),
            info(path_symboliclink)
        )
        print(err)


# NOTE: Eliminar directorios.
def delete_dir(path_src: str | object, print_msg: bool = True) -> bool:
    """
    Eliminar un directorio o fichero.

    Parameters:
    path_src (str | object Path): Ruta del directorio o fichero a eliminar.
    print_msg (bool) [Opcional]: Imprimir mensaje de error.

    Returns:
    bool: Booleano según si se pudo eliminar o no.
    """

    # Comprobar que exista el directorio o fichero.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()

    # Eliminar un fichero.
    if path_src.is_file():

        try:

            os.remove(path_src)

            return True

        except Exception as err:
            pass

    # Eliminar un directorio.
    try:

        rmtree(path_src)

        return True

    except Exception as err:
        pass

    # Imprimir mensaje de error si no se pudo eliminar.
    if print_msg:
        print(error("Error al eliminar:", "btn_ico"), info(path_src))
        print(err)

    return


def del_emptydirs(path_src: str | object, print_msg: bool = True) -> None:
    """
    Borrar recursivamente los sub-directorios vacios.

    Parameters:
    path_scan (str | object Path): Ruta del directorio raíz.
    print_msg (bool) [Opcional]: Imprimir mensaje satisfactorio.

    Returns:
    None.
    """

    # Comprobar que exista el directorio o fichero.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()

    # Obtener todos los subdirectorios.
    all_subdirs = [item for item in path_src.rglob("*") if item.is_dir()]

    # Ordenar reversamente la lista
    all_subdirs.sort(reverse=True)

    # Borrar todos los subdirectorios vacios
    for subdir in all_subdirs:

        # Verificar que este vacio el directorio.
        if not any(subdir.glob("*")):

            try:

                # Borrar sub-directorio actual.
                subdir.rmdir()

                if print_msg:
                    print(success("Borrado:", "ico"), info(subdir))

            except Exception as err:

                print(error("No se pudo borrar:", "ico"), info(subdir))
                print(err)


# NOTE: Seleccionar ficheros y subdirectorios dentro de un directorio.
def select_contentdir(path_src: str | object, file_type: str = "", recursive: bool = False, print_msg: bool = True) -> list:
    """
    Seleccionar todo el contenido de en un directorio.

    Parameters:
    path_src (str | object Path): Ruta del directorio raíz.
    file_type (str) [Opcional]: Tipos de ficheros a seleccionar.
    recursive (bool) [Opcional]: Buscar en los sub-directorios.
    print_msg (bool) [Opcional]: Imprimir mensaje sí no hay ficheros.

    Returns:
    list: Lista de objetos (Path) de los ficheros encontrados.
    """

    # Comprobar que exista el directorio.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()

    # Seleccionamos todo, sí no hay tipos de de ficheros.
    file_type = f'*.{file_type}' if file_type else '*'

    # Buscar en el directorio raíz y en sus sub-directorios.
    if recursive:
        result = [item for item in path_src.rglob(file_type)]

    # Buscar solo en el directorio raíz.
    else:
        result = [item for item in path_src.glob(file_type)]

    # Comprobar que se hayan encontrados ficheros.
    if not result and print_msg:

        if file_type in ["*", "*.*"]:
            msg = 'No hay contenido en:'

        else:
            msg = f'No hay ficheros {file_type.upper().replace("*.","")} en:'

        print(warning(msg, "ico"), info(path_src))

    return result


# NOTE: Mover, copiar y renombrar.
def prepare_paths(path_src: str | object, path_dst: str | object, overwrite: bool, metod_rename: bool = False, new_name: str = "") -> tuple:
    """
    Preparar las rutas para mover, copiar y renombrar directorios.

    Parameters:
    path_src (str | object Path): Ruta del fichero o directorio de origen.
    path_dst (str | object Path): Ruta del directorio de destino.
    overwrite (bool): Sobrescribir el destino sí existe.
    metod_rename (bool) [Opcional]: Método renombrar.
    new_name (str) [Opcional]: Nuevo nombre sí es método renombrar.

    Returns:
    tuple: Ruta de origen (path_src), destino (path_dst),
           final (path_dst_final) y mensaje pre-elaborado.
    """

    # Comprobar que exista el fichero o directorio de origen.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()
    path_dst = Path(path_dst).resolve() if path_dst else path_src.parent

    # Ruta final del destino
    path_dst_final = path_dst / path_src.name if not metod_rename \
        else path_dst / new_name

    # Comprobar que no exista el destino.
    if path_dst_final.exists():

        # Eliminamos el destino sí está "overwrite" activo.
        if overwrite:

            delete_dir(path_dst_final)

        else:

            print(warning("Ya existe:", "ico"), info(path_dst_final))
            return

    # Crear el directorio de destino sí no existe.
    if not create_dir(path_dst):
        return

    # Mensaje pre-elaborado.
    msg = f'{info(path_src)}\n  {bold("hacia:")} {info(path_dst)}'

    return path_src, path_dst, path_dst_final, msg


def move_dir(path_src: str | object, path_dst: str | object, print_msg: bool = False, overwrite: bool = False) -> str:
    """
    Mover un fichero o directorio.

    Parameters:
    path_src (str | object Path): Ruta del fichero o directorio a mover.
    path_dst (str) | object Path: Ruta del directorio al que se va a mover.
    print_msg (bool) [Opcional]: Imprimir un mensaje satisfactorio.
    overwrite (bool) [Opcional]: Sobrescribir el destino sí existe.

    Returns:
    str: Ruta absoluta del fichero o directorio movido.
    """

    # Preparar las rutas.
    paths = prepare_paths(path_src, path_dst, overwrite)

    if not paths:
        return

    # Desempaquetar las variables necesarias.
    path_src, path_dst, path_dst_final, msg = paths

    # Mover el fichero o directorio.
    try:

        move(path_src, path_dst)

        if print_msg:
            print(success("Movido:", "ico"), msg)

        return str(path_dst_final)

    except Exception as err:

        print(error("Error al mover:", "ico"), msg)
        print(err)


def move_files(files: list, path_dst: str | object, print_msg: bool = False, overwrite: bool = False, file_type: str = "*") -> None:
    """
    Mover una lista de ficheros o directorios.

    Parameters:
    files (list): Lista con las rutas (str | object Path) a mover.
    path_dst (str) | object Path: Ruta del directorio al que se va a mover.
    print_msg (bool) [Opcional]: Imprimir un mensaje satisfactorio.
    overwrite (bool) [Opcional]: Sobrescribir el destino sí existe.
    file_type (srt) [Opcional]: Tipo de ficheros a mover.

    Returns:
    None.
    """

    if print_msg:
        print(
            bold(f'Moviendo ficheros {file_type.upper()} hacia:'),
            info(path_dst)
        )

    try:
        _ = [
            move_dir(file, path_dst, print_msg, overwrite) for file in files
        ]

    except Exception as err:

        print(
            error(
                f'No se pudieron mover los ficheros {file_type.upper()} hacia:', "ico"),
            info(path_dst)
        )
        print(err)


def copy_dir(path_src: str | object, path_dst: str | object, print_msg: bool = False, overwrite: bool = False) -> str:
    """
    Copiar un fichero o directorio.

    Parameters:
    path_src (str | object Path): Ruta del fichero o directorio a copiar.
    path_dst (str | object Path): Ruta del directorio al que se va a copiar.
    print_msg (bool) [Opcional]: Imprimir un mensaje satisfactorio.
    overwrite (bool) [Opcional]: Sobrescribir el destino sí existe.

    Returns:
    str: Ruta absoluta del fichero o directorio copiado.
    """

    # Preparar las rutas.
    paths = prepare_paths(path_src, path_dst, overwrite)

    if not paths:
        return

    # Desempaquetar las variables necesarias.
    path_src, path_dst, path_dst_final, msg = paths

    # Copiar el fichero o directorio hacia su nuevo destino.
    try:

        # Copiar si es un directorio.
        if path_src.is_dir():

            copytree(path_src, path_dst_final, dirs_exist_ok=True)

        # Copiar sí es un fichero u otro.
        else:

            copyfile(path_src, path_dst_final)

        if print_msg:
            print(success("Copiado:", "ico"), msg)

        return str(path_dst_final)

    except Exception as err:

        print(error("Error al copiar:", "ico"), msg)
        print(err)


def rename_dir(path_src: str | object, new_name: str, path_dst: str | object = "",  print_msg: bool = False, overwrite: bool = False) -> str:
    """
    Renombrar y/o mover un fichero y directorio.

    Parameters:
    path_src (str | object Path): Ruta del fichero o directorio a renombrar.
    new_name (str): Nuevo nombre del fichero o directorio a renombrar.
    path_dst (str | object Path) [Opcional]: Ruta de destino fichero o directorio renombrado.
    print_msg (bool) [Opcional]: Imprimir un mensaje satisfactorio.
    overwrite (bool) [Opcional]: Sobrescribir el destino sí existe.

    Returns:
    str: Ruta absoluta del fichero o directorio renombrado.
    """

    # Comprobar que el nuevo nombre no este vacio.
    if not new_name:
        print(warning("El nuevo nombre no debe estar vacio.", "ico"))
        return

    # Preparar las rutas.
    paths = prepare_paths(
        path_src=path_src,
        path_dst=path_dst,
        overwrite=overwrite,
        metod_rename=True,
        new_name=new_name
    )

    if not paths:
        return

    # Desempaquetar las variables necesarias.
    path_src, path_dst, path_dst_final, msg = paths

    # Mensaje pre-elaborado.
    msg = f'{info(path_src)}\n  {bold("a:")} {info(path_dst_final)}'

    # Renombrar el fichero o directorio.
    try:

        path_src.rename(path_dst_final)

        if print_msg:
            print(success("Renombrado", "ico"), msg)

        return str(path_dst_final)

    except Exception as err:

        print(error("Error al renombrar:", "ico"), msg)
        print(err)
