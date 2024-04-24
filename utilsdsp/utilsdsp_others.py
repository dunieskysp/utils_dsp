"""
Oras funciones útiles.
    - obtain_URLfromHTML()
    - print_header()
    - clear_output()
    - calc_IMGdimensions()
    - optain_similarVars()
"""

import os
from pathlib import Path
from utilsdsp import validate_path, read_file
from outputstyles import warning, error, info


def obtain_URLfromHTML(path_src: str | object, num_line: int = 3) -> str:
    """
    Obtener la URL desde un fichero HTML, guardado con
    SingleFile (Extensión de Firefox).

    Parameters:
    path_src (str | object Path): Ruta del fichero HTML.
    num_line (int): Número de la linea donde está la URL.

    Returns:
    str: URL real del fichero HTML.
    """

    # Comprobar que exista el fichero HTML.
    if not validate_path(path_src):
        return

    # Construir rutas absolutas para evitar problemas con rutas relativas.
    path_src = Path(path_src).resolve()

    # Comprobar que sea un fichero HTML.
    if not path_src.suffix in [".html", ".HTML"]:
        print(warning("Solo se aceptan ficheros HTML:", "ico"),
              error(path_src, "ico"))
        return

    # Leer contenido del fichero HTML por lineas.
    content_html = read_file(path_src)

    try:

        num_line = num_line if isinstance(num_line, int) else 3

        # Retornar la URL real (Siempre es la 3ra línea).
        # Ej:  url: https://dominio.com/otra/dir/
        # return content_html[num_line - 1].strip().split(" ")[1]
        return content_html[num_line - 1].replace("url:", "").strip()

    except Exception as err:

        print(error("No se pudo obtener la URL de:", "ico"), info(path_src))
        # print(err)


def print_header(header: str, chars_cant: int = 100, decoration: str = "*", deco_init: int = 2) -> str:
    """
    Imprimir encabezados decorados.

    Parameters:
    header (str): Texto del encabezado.
    chars_cant (int) [Opcional]: Cantidad de carácteres del encabezado.
    decoration (str) [Opcional]: Decorado del encabezado.
    deco_init (int) [Opcional]: Cantidad de decorado inicial.

    Returns:
    str: Encabezado decorado y con la longitud especificada.
    """

    try:

        # Sanear argumentos.
        header = str(header)
        chars_cant = int(chars_cant)
        decoration = str(decoration)
        deco_init = int(deco_init)

        # Verificar que la cantidad de decoración inicial sea positiva.
        deco_init = (deco_init) if deco_init >= 0 else 1

        # Cantidad de decoración al final del encabezado.
        deco_final = chars_cant - len(header) - deco_init

        # Decoración inicial con el texto del header.
        header_init = f'{header} ' if deco_init == 0 else f'{decoration * deco_init} {header} '

        # Cantidad de decoración al final.
        header_final = decoration * deco_final if deco_final > 0 else decoration * deco_init

        return header_init + header_final

    except Exception as err:

        print(error("Error:", "ico"), err)


def clear_output() -> None:
    """
    Limpiar CLI según el SO.

    Parameters:
    None.

    Returns:
    None.
    """

    # Si es Windows.
    if os.name == "nt":
        os.system("cls")

    # Si es Unix o Linux
    elif os.name == "posix":
        os.system("clear")

    # En otros casos, imprime 120 nuevas líneas
    else:
        print("\n" * 120)


def calc_IMGdimensions(img_size: tuple, width_final: int = None, height_final: int = None) -> tuple:
    """
    Calcular las dimensiones finales (ancho, alto) de
    una imagen según su ancho o altura a modificar.

    Parameters:
    img_size (tuple): Tamaño original de la imagen (ancho, alto).
    width_final (int) [Opcional]: Ancho a modificar.
    height_final (int) [Opcional]: Alto a modificar.

    Returns:
    tuple: Devuelve el ancho y alto de la imagen modificada.
    """

    # Calcular la altura final si se introdujo un ancho.
    if width_final and isinstance(width_final, int):

        # Fórmula: height_final = width_final / width_org * height_org
        height_final = round(width_final / int(img_size[0]) * int(img_size[1]))

    # Calcular el Ancho final si se introdujo una altura.
    elif height_final and isinstance(height_final, int):

        # Fórmula: width_final = height_final / height_org * width_org
        width_final = round(height_final / int(img_size[1]) * int(img_size[0]))

    # Retornar el mismo tamaño de la imagen si no son válidos.
    else:
        width_final, height_final = img_size

    return width_final, height_final


def optain_similarVars(var_name: str, var_cant: int, all_vars: dict, value: bool = True) -> list:
    """
    Obtener el valor de las varibles que tienen el nombre similar,
    solo le cambia un número a cada una (Ej: var_1, var_2, etc).

    Parameters:
    var_name (str): Nombre común entre las varibles.
    var_cant (int): Cantidad de variables que hay similares.
    all_vars (dict): Diccionario con todas las variables [globals() o locals()].
    value (bool) [Opcional]: Obtener el valor de las variables o el nombre.

    Returns:
    list: Valores no núlos de las variables en una lista.
    """

    try:

        if value:

            result = [
                all_vars[f'{var_name}{i}'] for i in range(1, var_cant + 1) if all_vars[f'{var_name}{i}']
            ]

        else:

            result = [
                f'{var_name}{i}' for i in range(1, var_cant + 1) if all_vars[f'{var_name}{i}']
            ]

        return result

    except Exception as err:
        print(error("Error al obtener la variable:", "ico"), err)
