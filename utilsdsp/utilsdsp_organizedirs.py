"""
Organizar los directorios.
    - move_files_to_root()
    - move_files_to_subdir()
    - organize_files_by_type()
    - organize_files_by_name()
"""

from pathlib import Path
from outputstyles import warning, info, bold
from utilsdsp import validate_path, select_contentdir, move_files, join_path, joinlist_to_dict, del_emptydirs


def move_files_to_root(path_src: str | Path, file_type: str | None = None, delete_empty: bool = False, overwrite: bool = False, print_msg: bool = True) -> None:
    """
    Mover los ficheros hacía el directorio raíz.

    Parameters:
    path_src (str | Path): Ruta del directorio a organizar.
    file_type (str | None) [Opcional]: Tipos de ficheros a seleccionar.
    delete_empty (bool) [Opcional]: Eliminar las carpetas vacias.
    overwrite (bool) [Opcional]: Sobrescribir el destino sí existe.
    print_msg (bool) [Opcional]: Imprimir un mensaje satisfactorio.

    Returns:
    None.
    """

    # Comprobar que exista la ruta.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()

    # Seleccionar solo los ficheros en los sub-directorios.
    file_type = file_type if file_type else "*"

    files = [
        file for file in select_contentdir(path_src, file_type, True) if path_src != file.parent
    ]

    if not files:

        print(
            warning(
                f'No hay ficheros {file_type.upper()} en los sub-directorios de:', "ico"
            ),
            info(path_src)
        )

        return

    # Mover todos los ficheros seleccionados.
    move_files(
        files,
        path_dst=path_src,
        print_msg=print_msg,
        overwrite=overwrite,
        file_type=file_type
    )

    # Borrar los sub-directorios vacios.
    if delete_empty:
        print("")
        del_emptydirs(path_src, print_msg=print_msg)


def move_files_to_subdir(path_src: str | Path, subdir_name: str, file_type: str | None = None, overwrite: bool = False, print_msg: bool = True) -> None:
    """
    Crear un directorio dentro de los sub-directorios del nivel 1
    y mover los ficheros seleccionados dentro de él.

    Parameters:
    path_src (str | Path): Ruta del directorio raíz.
    subdir_name (str): Nombre del nuevo sub-directorio.
    file_type (str | None) [Opcional]: Tipos de ficheros a seleccionar.
    overwrite (bool) [Opcional]: Sobrescribir el destino sí existe.
    print_msg (bool) [Opcional]: Imprimir un mensaje satisfactorio.

    Returns:
    None.
    """

    # Comprobar que exista la ruta.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()

    # Obtener todos los sub-directorios del nivel 1.
    all_subdirs = [
        item for item in select_contentdir(path_src) if item.is_dir()
    ]

    if not all_subdirs:
        print(warning(f'No hay sub-directorios en:', "ico"), info(path_src))
        return

    # Mover los ficheros hacia el nuevo sub-directorio.
    for subdir in all_subdirs:

        # Obtener los ficheros del directorio actual.
        file_type = file_type if file_type else "*"

        files = [item for item in select_contentdir(subdir, file_type)]

        # Continuamos sí no hay ficheros.
        if not files:
            print("")
            continue

        # Ruta del nuevo sub-directorio.
        path_dst = join_path(str(subdir), subdir_name)

        # Mover los ficheros.
        move_files(files, path_dst, print_msg, overwrite, file_type)

        # Linea intermedia entre cada operación.
        print("")


def organize_files_by_type(path_src: str | Path, files_data: dict | list, path_dst: str | Path | None = None, overwrite: bool = False, print_msg: bool = True) -> None:
    """
    Organizar los ficheros según su tipo en carpetas.

    Parameters:    
    path_src (str | Path): Ruta del directorio a organizar.
    files_data (dict | list): Diccionario o lista con los tipos de ficheros y carpetas.
    path_dst (str | Path | None) [Opcional]: Ruta de destino.
    overwrite (bool) [Opcional]: Sobrescribir el destino sí existe.
    print_msg (bool) [Opcional]: Imprimir un mensaje satisfactorio.

    Ej diccionario:
    - files_data = {
        "txt":"Textos",
        "jpg":"Imagenes"
    }

    Ej lista (Deben tener la misma longitud):
    - files_ext = ["txt", "jpg"]
    - files_folder = ["Textos", "Imagenes"]

    Returns:
    None.
    """

    # Comprobar que exista la ruta.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()
    path_dst = Path(path_dst).resolve() if path_dst else path_src

    # Trabajar con los datos sí son listas.
    if isinstance(files_data, list) and len(files_data) == 2:

        ext_and_folders = joinlist_to_dict(files_data[0], files_data[1])

        if not ext_and_folders:
            return

    elif isinstance(files_data, dict):

        ext_and_folders = files_data

    # Organizar los ficheros.
    for ext, folder in ext_and_folders.items():

        # Comprobar que que no esten vacios los valores.
        if not (ext and folder):

            print(warning("Los valores no deben estar vacios.", "ico"))
            print(bold("Extensión:"), ext)
            print(bold("Carpeta:"), folder)

            print("")
            continue

        # Buscar los ficheros según la extensión.
        files = select_contentdir(path_src, file_type=ext)

        # Continuamos sí no hay ficheros.
        if not files:
            print("")
            continue

        # Obtener la ruta del directorio de destino.
        path_dst_final = join_path(str(path_dst), folder)

        # Mover los ficheros.
        move_files(files, path_dst_final, print_msg, overwrite, file_type=ext)

        # Linea intermedia entre cada operación.
        print("")


def organize_files_by_name(path_src: str | Path, path_dst: str | Path | None = None, file_type: str | None = None, secondary: str | None = None, del_name: str | None = None, subdir: str | None = None, overwrite: str = False, print_msg: bool = True) -> None:
    """
    Organizar los ficheros según su nombre en carpetas.
    - Pueden existir ficheros principales y secundarios.
    Ej:
    - Principal: The Boys - Series.com.html
    - Secundario: The Boys Episodio 1 - Series.com.html

    Parameters:    
    path_src (str | Path): Ruta del directorio a organizar.
    path_dst (str | Path | None) [Opcional]: Ruta de destino.
    file_type (str | None) [Opcional]: Tipos de ficheros a tener en cuenta.
    secondary (str | None) [Opcional]: Texto para identificar los secundarios (Episodio).
    del_name (str | None) [Opcional]: Texto a eliminar del nombre de la carpeta ( - Series.com).
    subdir (str | None) [Opcional]: Subdirectorio a crear dentro de las carpetas.
    overwrite (bool) [Opcional]: Sobrescribir el destino sí existe.
    print_msg (bool) [Opcional]: Imprimir un mensaje satisfactorio.

    Returns:
    None.
    """

    # Comprobar que exista la ruta.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()
    path_dst = Path(path_dst).resolve() if path_dst else path_src

    # Obtener todos los ficheros del nivel 1.
    file_type = file_type if file_type else "*"

    all_files = select_contentdir(path_src, file_type)

    if not all_files:
        return

    # Seleccionar los ficheros principales y secundarios.
    files_secondary = [
        item for item in all_files if secondary and secondary in item.name
    ]

    files_main = [item for item in all_files if not item in files_secondary]

    # Mover los ficheros hacia sus carpetas correspondientes.
    for file in files_main:

        # Obtener el nombre de la carpeta.
        del_name = del_name if del_name else ""
        folder_name = file.stem.replace(del_name, "")

        # Ruta de la nueva carpeta.
        path_newfolder = join_path(str(path_dst), folder_name, subdir)

        # Seleccionar los secundarios del ficheros principal en turno.
        files_sec = [
            item for item in files_secondary if item.stem.startswith(folder_name)
        ]

        # Mover el fichero principal y sus secundarios.
        move_files(
            files=[file] + files_sec,
            path_dst=path_newfolder,
            print_msg=print_msg,
            overwrite=overwrite,
            file_type=file_type
        )

        # Linea intermedia entre cada operación.
        print("")
