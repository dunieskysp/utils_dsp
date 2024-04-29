"""
Descargar ficheros desde internet.
    - validateURL()
    - obtain_filename()
    - rename_downloadfile()
    - update_downloadlogs()
    - organize_URLsdata()
    - update_descriptionPbar()
    - download_file()
    - download_files()
"""

import requests
import validators
from pathlib import Path
from tqdm.auto import tqdm
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor, as_completed
from outputstyles import error, warning, info, success, bold
from utilsdsp import sanitize_filename, create_downloadsdir, natural_size, join_path, validate_path, write_file, obtain_downloadspath


def validateURL(url: str, accessible: bool = True, timeout: int | None = 10, stream: bool = True) -> bool | requests.Response:
    """
    Comprobar sí una URL es válida y accesible.

    Parameters:
    url (str): Dirección web a comprobar.
    accessible (bool) [Opcional]: Verificar sí es accesible.
    timeout (int | None) [Opcional]: Tiempo de espera por la respuesta del servidor.
    stream (bool) [Opcional]: No descargar la respuesta completa en memoria.

    Returns:
    bool | requests.Response: Sí no hay que comprobar la accesibilidad
    retorna un booleano, sino la respuesta del "requests".
    """

    # Comprobar la estructura de la URL.
    if not validators.url(url):
        print(error("URL no válida:", "btn_ico"), info(url))
        return False

    # Devolver "True" si no hay que comprobar la accesibilidad de la URL.
    if not accessible:
        return True

    # Obtener el contenido de la URL.
    try:

        # Hacer petición a la URL.
        response = requests.get(url, timeout=timeout, stream=stream)

        # Levantar una exception si no se obtuvo una respuesta satisfacoria.
        response.raise_for_status()

        # Retornar el contenido.
        return response

    except requests.exceptions.RequestException as err:

        print(error("No se pudo establecer conexión con:", "ico"), info(url))
        print(err)

        return False


def obtain_filename(response: requests.Response, url: str, missing_name: str | None = None) -> str:
    """
    Obtener el nombre de un archivo que se va
    a descargar desde internet.

    Parameters:
    response (requests.Response): Respuesta obtenida del URL.
    url (str): Dirección web del archivo.
    missing_name (str) [Opcional]: Nombre por defecto si no se obtiene el nombre del archivo.

    Returns:
    str: Nombre del archivo.
    """

    # Obtener el nombre según su URL.
    file = Path(url)
    missing_name = missing_name or "missing name"
    default_name = file.name if file.suffix else f'{missing_name} ({file.name})'

    # Si el servidor brinda el "Content-Disposition", se le asigna a la variable.
    if content_disposition := response.headers.get("Content-Disposition"):

        # Retornamos el nombre que aparece en "Content-Disposition".
        # (Content-Disposition: attachment; filename="nombre_del_archivo.ext";)
        return content_disposition.split('filename=')[1].split('"')[1]

    # Retornar el nombre según su URL.
    return default_name


def rename_downloadfile(path_src: str | Path) -> str:
    """
    Renombrar el archivo a descargar.

    Parameters:
    path_src (str | Path): Ruta del archivo.

    Returns:
    str: Ruta del archivo renombrado
    """

    # Segmentar la ruta original.
    path_src = Path(path_src)

    parent = path_src.parent
    name = path_src.stem
    ext = path_src.suffix

    # Conformar nueva ruta renombrada.
    num = 1
    path_new = parent / f'{name}_{str(num)}{ext}'

    # Verificar que no exista la nueva ruta.
    while validate_path(str(path_new), print_msg=False):

        # Sí existe, seguimos creando una nueva ruta hasta que no exista.
        num += 1
        path_new = parent / f'{name}_{str(num)}{ext}'

    # Retornamos la ruta del archivo renombrado.
    return str(path_new)


def update_downloadlogs(write_logs: bool, logs_path: str | Path, msg_type: str, url: str, filepath: str | None = None, err: str | None = None) -> None:
    """
    Actualizar los logs de la descarga.

    Parameters:
    write_logs (bool): Guardar los logs.
    logs_path (str | Path): Ruta del fichero de los logs.
    msg_type (str) [Opcional]: Tipo de mensaje a guardar.
    url (str) [Opcional]: URL en turno.
    filepath (str | None) [Opcional]: Ruta del archivo descargado.
    err (str | None) [Opcional]: Mensaje de error de la excepción.

    Returns:
    None.
    """

    # No hacer nada, sí no hay que guardar los logs.
    if not write_logs:
        return

    # Tipos de mensajes a guardar en los logs.
    msg_texts = {
        "url_notvalid": f'ERROR - [Invalid URL]: URL no válida o no accesible.\n\t\t\tURL: {url}\n',
        "file_empty": f'ERROR - [Empty File]: El fichero no se encuentra o está vacio.\n\t\t\tURL: {url}\n',
        "file_exists": f'WARNING - [Exists File]: Ya existe el fichero a descargar.\n\t\t\tRUTA: {filepath}\n\t\t\tURL: {url}\n',
        "downloaded": f'SUCCESS - [Downloaded File]: Fichero descargado correctamente.\n\t\t\tRUTA: {filepath}\n\t\t\tURL: {url}\n',
        "error_download": f'ERROR - [Download File]: Error al descargar el fichero.\n\t\t\tRUTA: {filepath}\n\t\t\tURL: {url}\n'
    }

    # Obtener fecha y hora actual.
    current_time = datetime.now().strftime("%Y-%m-%d %I:%M:%S%p")

    # Guardar el logs sí el mensaje es válido.
    if msg_type in msg_texts:

        # Imprimir el mensaje de error también.
        if err:
            msg = f'{current_time}\t{msg_texts[msg_type]}\n\t\t\t{err}\n'

        else:
            msg = f'{current_time}\t{msg_texts[msg_type]}'

        # Escribir los logs en un fichero.
        try:
            write_file(logs_path, content_write=msg)

        except:
            pass


def organize_URLsdata(urls_data: list, path_dst: str) -> list:
    """
    Organizar los datos de las URLs a descargar.

    Parameters:
    urls_data (list): Lista con las URLs, nombres y carpetas separados por coma.
    path_dst (str) [Opcional]: Directorio para guardar las descargas.

    Returns:
    list: Lista de tuplas con (URL, Filename, Path_Folder, pbar_pos).
    """

    list_result = []

    # Organizar por tuplas los datos de las URLs.
    for data in urls_data:

        # Segmentar los datos.
        data_segments = data.split(",")

        # Comprobar que tenga URL y solo 3 datos.
        if not data_segments[0] or len(data_segments) > 3:
            continue

        # Conformar las tuplas según los datos (URL, Filename, Folder).
        if len(data_segments) == 1:
            url_data = (
                data_segments[0],
                "",
                path_dst
            )

        if len(data_segments) == 2:
            url_data = (
                data_segments[0],
                data_segments[1].strip(),
                path_dst
            )

        if len(data_segments) == 3:
            url_data = (
                data_segments[0],
                data_segments[1].strip(),
                join_path(path_dst, data_segments[2].strip())
            )

        # Agregar los datos a la lista resultante.
        list_result.append(url_data)

    return list_result


def update_descriptionPbar(result: str, status: dict) -> tuple:
    """
    Actualizar la descripción de la barra de progreso principal.

    Parameters:
    result (str): Resultado al descargar un archivo.
    status (dict): Estadísticas de las descargas.

    Returns:
    tuple (srt, dict): Descripción actualizada y diccionario con las estadísticas.
    """

    # Actualizar el estado y tamaño de los archivos descargados.
    if result != "down_error" and result != "down_warning":
        status["downloaded"] += 1
        status["size"] += Path(result).stat().st_size

    # Actualizar las advertencias y errores.
    if result == "down_warning":
        status["warnings"] += 1

    if result == "down_error":
        status["errors"] += 1

    # Conformar la descripción con las estadisticas actualizadas.
    desc = success(
        f'Descargados {status["downloaded"]} archivos ({natural_size(status["size"])})'
    )

    desc += warning(f' - Advertencias ({status["warnings"]})')

    desc += error(f' - Errores ({status["errors"]})')

    return desc, status


def download_file(url: str, filename: str | None = None, path_dst: str | None = None, overwrite: bool = False, rename: bool = False, missing_name: str | None = None, write_logs: bool = True, logs_path: str | None = None, timeout: int = 10, chunk_size: int = 1, show_pbar: bool = True, disable_pbar: bool = False, leave: bool = True, ncols: int | None = None, colour: str | None = None, position: int | None = None, desc_len: int | None = None, print_msg: bool = True) -> str | None:
    """
    Descargar un archivo desde internet.

    Parameters:
    url (str): Dirección web archivo.
    filename (str) [Opcional]: Nombre del archivo.
    path_dst (str) [Opcional]: Directorio para guardar el archivo.

    overwrite (bool) [Opcional]: Sobrescribir el archivo sí existe.
    rename (bool) [Opcional]: Renombrar el archivo sí existe.
    missing_name (str) [Opcional]: Nombre por defecto si no se obtiene el nombre del archivo.

    write_logs (bool) [Opcional]: Guardar los logs.
    logs_path (str) [Opcional]: Ruta del fichero de los logs.

    timeout (int) [Opcional]: Tiempo de espera por una respuesta del servidor.
    chunk_size (int): Tamaño del bloque a descargar desde el servidor.

    show_pbar (bool) [Opcional]: Mostrar la barra de progreso.
    disable_pbar (bool) [Opcional]: Deshabilitar la barra de progreso.
    leave (bool) [Opcional]: Dejar la barra de progreso al completar.
    ncols (int) [Opcional]: Número de columnas de la barra de progreso.
    colour (str) [Opcional]: Color de la barra de progreso.
    position (int) [Opcional]: Posición de la barra de progreso.
    desc_len (int) [Opcional]: Longitud de la descripción.

    print_msg (bool) [Opcional]: Imprimir los mensajes (warnings & errors).

    Returns:
    str: Ruta del fichero guardado.
    """

    # Obtener la ruta para guardar la descarga.
    path_dst = create_downloadsdir(path_dst)

    # Obtener la ruta del fichero de los logs.
    logs_path = logs_path or join_path(path_dst, "logs.txt")

    # Validar la URL.
    if not (response := validateURL(url, timeout=timeout)):

        # Atualizar los logs.
        update_downloadlogs(write_logs, logs_path, "url_notvalid", url)

        return "down_error"

    # Obtener el tamaño del archivo.
    filesize = int(response.headers.get("Content-Length", 0))

    if filesize == 0:

        if print_msg:
            print(warning("El fichero no se encuentra o está vacio:", "ico"), info(url))

        # Atualizar los logs.
        update_downloadlogs(write_logs, logs_path, "file_empty", url)

        return "down_warning"

    # Obtener el nombre del archivo.
    filename = sanitize_filename(filename) if filename and isinstance(filename, str) \
        else obtain_filename(response, url, missing_name)

    # Obtener la ruta del archivo.
    filepath = join_path(path_dst, filename)

    # Comprobar que no exista el archivo.
    if validate_path(filepath, print_msg=False) and not overwrite and not rename:

        if print_msg:
            print(warning("Ya existe:", "ico"), info(filepath))
            print(bold("  URL:"), info(url))

        # Atualizar los logs.
        update_downloadlogs(write_logs, logs_path,
                            "file_exists", url, filepath)

        return "down_warning"

    # Sí existe el archivo, lo renombramos.
    if validate_path(filepath, print_msg=False) and rename:

        filepath = rename_downloadfile(filepath)
        filename = Path(filepath).name

    # Conformar el formato de la barra de progreso.
    bar_format = '{l_bar}{bar}{r_bar}' if show_pbar else '{l_bar}{r_bar}'

    # Conformar la descripción.
    if isinstance(desc_len, int) and len(filename) > desc_len:
        name = Path(filename).stem
        ext = Path(filename).suffix

        description = f'{name[:desc_len - 3 - len(ext)]}...{bold(ext)}'

    else:
        description = filename

    # Definir la barra de progreso.
    pbar = tqdm(
        total=filesize,
        desc=description,
        unit="B",
        unit_scale=True,
        bar_format=bar_format,
        disable=disable_pbar,
        ncols=ncols,
        colour=colour,
        leave=leave,
        position=position
    )

    # Descargar el archivo.
    try:

        with open(filepath, "wb") as file:

            if disable_pbar:
                print(bold("Descargando:"), info(filepath))

            # Escribir el archivo y actualizar la barra de progreso.
            for data in response.iter_content(chunk_size=chunk_size * 10):

                size = file.write(data)
                pbar.update(size)

            # Atualizar los logs.
            update_downloadlogs(write_logs, logs_path,
                                "downloaded", url, filepath)

            return filepath

    except Exception as err:

        if print_msg:
            print(error("Error al descargar:", "ico"), info(filename))
            print(bold("  URL:"), info(url))

        # Atualizar los logs.
        update_downloadlogs(write_logs, logs_path,
                            "error_download", url, filepath, err)

        return "down_error"


def download_files(urls: list, path_dst: str | None = None, max_workers: int = 1, overwrite: bool = False, rename: bool = False, missing_name: str | None = None, write_logs: bool = True, logs_path: str | None = None, timeout: int = 10, chunk_size: int = 1, show_pbar: bool = True, disable_pbar: bool = False, leave: bool = True, ncols: int | None = None, colour_main: str | None = None, colour: str | None = None, desc_len: int | None = None, print_msg: bool = False) -> str | None:
    """
    Descargar multiples archivos simultaneos desde internet.
    - Recive una lista de URL, nombre del archivo y carpeta
    donde se va a guardar, todo seperado por comas.

    Ej: urls = [
        "https://dominio.com/fichero.txt, Nuevo nombre.txt, Carpeta de textos",
        "https://dominio.com/imagen.jpg, Foto.jpg, Carpeta de imagenes",
    ]

    Parameters:
    urls (list): Lista con las URLs, nombres y carpetas separados por coma.
    path_dst (str) [Opcional]: Directorio para guardar las descargas.
    max_workers (int) [Opcional]: Cantidad de descargas simultaneas.

    overwrite (bool) [Opcional]: Sobrescribir el archivo sí existe.
    rename (bool) [Opcional]: Renombrar el archivo sí existe.
    missing_name (str) [Opcional]: Nombre por defecto si no se obtiene el nombre del archivo.

    write_logs (bool) [Opcional]: Guardar los logs.
    logs_path (str) [Opcional]: Ruta del fichero de los logs.

    timeout (int) [Opcional]: Tiempo de espera por una respuesta del servidor.
    chunk_size (int): Tamaño del bloque a descargar desde el servidor.

    show_pbar (bool) [Opcional]: Mostrar la barra de progreso.
    disable_pbar (bool) [Opcional]: Deshabilitar la barra de progreso.
    leave (bool) [Opcional]: Dejar la barra de progreso al completar.
    ncols (int) [Opcional]: Número de columnas de la barra de progreso.
    colour_main (str) [Opcional]: Color de la barra de progreso principal.
    colour (str) [Opcional]: Color de las barras de progreso secundarias.
    desc_len (int) [Opcional]: Longitud de la descripción.

    print_msg (bool) [Opcional]: Imprimir los mensajes (warnings & errors).

    Returns:
    str: Ruta del directorio donde se descargaron los archivos.
    """

    # Organizar los datos de las URLs.
    path_dst = obtain_downloadspath(path_dst)
    urls_data = organize_URLsdata(urls, path_dst)

    # Definir la barra de progreso.
    progress_bar = tqdm(
        total=len(urls_data),
        desc=bold("Descargando archivos..."),
        ncols=ncols,
        colour=colour_main,
        leave=True,
        position=0
    )

    # Comenzar la descarga de los archivos.
    try:

        # Crear un ThreadPoolExecutor para multitareas.
        with ThreadPoolExecutor(max_workers=max_workers) as executor:

            # Crear una barra de progreso con tqdm.
            with progress_bar as pbar:

                # Enviar tareas de descarga al executor y obtener su resultado al finalizar.
                futures = {
                    executor.submit(
                        download_file,
                        url=url,
                        filename=filename,
                        path_dst=path_dstfolder,

                        overwrite=overwrite,
                        rename=rename,
                        missing_name=missing_name,

                        write_logs=write_logs,
                        logs_path=logs_path,

                        timeout=timeout,
                        chunk_size=chunk_size,

                        show_pbar=show_pbar,
                        disable_pbar=disable_pbar,
                        leave=leave,
                        ncols=ncols,
                        colour=colour,
                        position=1,
                        desc_len=desc_len,

                        print_msg=print_msg
                    ): (url, filename, path_dstfolder) for url, filename, path_dstfolder in urls_data
                }

                # Estadísticas de las descargas.
                status = {
                    "downloaded": 0,
                    "size": 0,
                    "warnings": 0,
                    "errors": 0
                }

                # Itera sobre las tareas de descarga a medida que se completan.
                for future in as_completed(futures):

                    # Actualizar el porciento de la barra de progreso.
                    pbar.update(1)

                    # Obtener el resultado de la descarga finalizada actual.
                    result = future.result()

                    # Actualizar la descripción de la barra de progreso.
                    desc, status = update_descriptionPbar(result, status)

                    pbar.set_description(desc)

        return path_dst

    except Exception as err:
        print(error("Error en la descarga simultanea de archivos.", "ico"))
        print(err)
