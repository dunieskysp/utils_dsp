"""
Operaciones con rutas:
    - obtain_currentpath()
    - obtain_absolutepath()
    - change_currentpath()
    - validate_path()
    - join_path()
    - obtain_defaultpath()
    - obtain_downloadspath()

"""

import os
from pathlib import Path
from outputstyles import error, info, warning


def obtain_currentpath(os_method: bool = False) -> str:
    """
    Obtener la ruta actual.

    Parameters:
    os_method (bool) [Opcional]: Usar el paquete "os" y no "pathlib".

    Returns:
    str: Ruta absoluta actual.
    """

    # Usando el módulo "os".
    if os_method:
        return os.getcwd()

    # Usando el módulo "pathlib".
    return str(Path().absolute())


def obtain_absolutepath(path_src: str, os_method: bool = False) -> str:
    """
    Obtener la ruta absoluta (No necesariamente debe existir).

    Parameters:
    path_src (str): Ruta relativa.
    os_method (bool) [Opcional]: Usar el paquete "os" y no "pathlib".

    Returns:
    str: Ruta absoluta.
    """

    # Usando el módulo "os".
    if os_method:
        return os.path.abspath(path_src)

    # Usando el módulo "pathlib".
    return str(Path(path_src).resolve())


def change_currentpath(path_src: str) -> str:
    """
    Cambiar la ruta actual (Debe existir la ruta).

    Parameters:
    path_src (str): Nueva ruta a cambiar.

    Returns:
    str: Nueva ruta cambiada.
    """

    # Comprobar que exista el directorio de origen.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = obtain_absolutepath(path_src)

    # Cambiar la ruta.
    try:

        os.chdir(path_src)
        return path_src

    # En las primeras líneas se comprueba sí existe la ruta,
    # por lo que estas líneas no son necesarias.
    except FileNotFoundError:

        print(error("No existe el directorio:", "ico"), info(path_src))

        return

    except Exception as err:

        print(error("Error al cambiar hacia la ruta:", "ico"), info(path_src))
        print(err)

        return


def validate_path(path_src: str, os_method: bool = False, print_msg: bool = True) -> bool:
    """
    Válidar si la ruta existe.

    Parameters:
    path (str): Ruta a comprobar su existencia.
    os_method (bool) [Opcional]: Usar el módulo "os" en vez de "pathlib".
    print_msg (bool) [Opcional]: Imprimir un mensaje si no existe la ruta.

    Returns:
    bool: Booleano según la existencia de la Ruta.
    """

    # Comprobar que no este vacia la ruta.
    if not path_src:
        print(warning("Debe insertar una ruta.", "ico"))
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = obtain_absolutepath(path_src)

    # Usando el módulo "os" y el método "exists()".
    if os_method:
        result = os.path.exists(path_src)

    # Usando el módulo "pathlib" y el método "Path".
    else:
        result = Path(path_src).exists()

    # Imprimir un mensaje si no existe.
    if not result and print_msg:
        print(error('No existe:', "ico"), info(path_src))

    return result


def join_path(*args: str, os_method: bool = False) -> str:
    """
    Unir directorios en una sola ruta.

    Parameters:
    args (list): Directorios a unir en una sola ruta.
    os_method (bool) [Opcional]: Usar el paquete "os" en vez de "pathlib".

    Returns:
    str: Ruta unida absoluta.
    """

    # Seleccionar solo los argumentos de tipo "string".
    args = (arg for arg in args if isinstance(arg, str))

    # Usando el paquete "os".
    if os_method:
        return os.path.join(*args)

    # Usando el paquete "pathlib".
    return str(Path().joinpath(*args))


def obtain_defaultpath(in_PC: bool = False, mount_GDrive: bool = False) -> str:
    """
    Obtener la ruta por defecto si se trabaja en la PC o en Google Colab.

    Parameters:
    in_PC (bool) [Opcional]: Se está trabajando en la PC o no.
    mount_GDrive (bool) [Opcional]: Está montado GDriver o no en Google Colab.

    Returns:
    str: Ruta por defecto absoluta.
    """

    # Retornar la ruta por defecto de la PC.
    if in_PC:

        # Ruta actual.
        current_path = obtain_currentpath()

        return join_path(current_path, "MyDrive") if mount_GDrive else current_path

    # Retornar la ruta por defecto en Google Colab.
    return "/content/drive/MyDrive" if mount_GDrive else "/content"


def obtain_downloadspath(input_dir: str = "", in_PC: bool = False, mount_GDrive: bool = False) -> str:
    """
    # Obtener la ruta para guardar las descargas.

    Parameters:
    input_dir (str) [Opcional]: Directorio para guardar las Descargas.
    in_PC (bool) [Opcional]: Se está trabajando en la PC o no.
    mount_GDrive (bool) [Opcional]: Está montado GDriver o no en Google Colab.

    Returns:
    str: Ruta absoluta del directorio de descargas.
    """

    # Obtener la ruta padre por defecto.
    default_path = obtain_defaultpath(in_PC, mount_GDrive)

    # Sí no se introdujo ninguna ruta.
    if not input_dir:

        # Conformar una ruta por defecto para las descargas.
        return join_path(default_path, "Downloads")

    # Sí la ruta por defecto está contenida en la introducida.
    elif input_dir.startswith(default_path):

        # Usar la misma ruta introducida.
        return input_dir

    # Unir la ruta por defecto con la introducida.
    # Si las dos son rutas absolutas, se mantiene la última.
    return join_path(default_path, input_dir)