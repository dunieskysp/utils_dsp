"""
Útiles de @dunieskysp.

Operaciones con rutas:
    - obtain_currentpath()
    - obtain_absolutepath()
    - change_currentpath()
    - validate_path()
    - join_path()
    - obtain_defaultpath()
    - obtain_downloadspath()

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

Operaciones con ficheros.
    - read_file()
    - write_file()

Operaciones de saneamento.
    - truncate_filename()
    - sanitize_filename()

Obtener tamaño de ficheros y directorios.
    - natural_size()
    - obtain_sizedir()
    - obtain_sizefile()
    - obtain_size()

Comprimir ficheros y directorios.
    - compress()
    - uncompress()

Otras funciones útiles:
    - obtain_url_from_html: Obtener la URL desde un fichero HTML
    - create_headers_decorates: Crear un encabezado decorado
    - clear_output: Limpiar salida en la Terminal según el SO
    - calc_img_dimensions: Calcular las dimensiones de una imagen
    - obtain_similar_vars: Obtener el valor o nombre de variables similares

Organizar los directorios.
    - move_files_to_root()
    - move_files_to_subdir()
    - organize_files_by_type()
    - organize_files_by_name()

Descargar un archivo desde internet:
    - validate_and_resquest: Comprobar sí una URL es válida y accesible
    - obtain_filename: Obtener nombre del archivo que se va a descargar
    - rename_download_file: Renombrar el archivo a descargar
    - update_download_logs: Actualizar los logs de la descarga
    - download_file: Descargar un archivo desde internet

Descargar varios archivos desde internet:
    - organize_urls_data: Organizar en tuplas los datos de las URLs a descargar
    - update_description_pbar: Actualizar descripción de la barra de progreso principal
    - download_files: Descargar multiples archivos simultaneos desde internet


Operaciones con listas:
    - remove_repeated_elements: Eliminar elementos repetidos

Operaciones con Diccionarios:
    - join_list_to_dict: Unir dos listas en un diccionario
"""

# Útiles de rutas
from utilsdsp.utilsdsp_path import obtain_currentpath, obtain_absolutepath, change_currentpath, validate_path, join_path, obtain_defaultpath, obtain_downloadspath


# Útiles de directorios
from utilsdsp.utilsdsp_dirs import create_dir, create_downloadsdir, create_symboliclink, delete_dir, del_emptydirs, select_contentdir, move_dir, move_files, copy_dir, rename_dir


# Útiles de ficheros
from utilsdsp.utilsdsp_files import read_file, write_file


# Útiles de seneamiento de nombres de ficheros
from utilsdsp.utilsdsp_sanitize import sanitize_filename


# Obtener tamaño de ficheros y directorios
from utilsdsp.utilsdsp_sizefile import natural_size, obtain_sizedir, obtain_sizefile, obtain_size


# Comprimir ficheros y directorios
from utilsdsp.utilsdsp_compress import compress, uncompress


# Otras funciones útiles
from utilsdsp.utilsdsp_others import obtain_url_from_html, create_headers_decorates, clear_output, calc_img_dimensions, obtain_similar_vars


# Organizar los directorios
from utilsdsp.utilsdsp_organizedirs import move_files_to_root, move_files_to_subdir, organize_files_by_type, organize_files_by_name

# Descargar ficheros desde internet
from utilsdsp.utilsdsp_downloads import validate_and_resquest, obtain_filename, rename_download_file, update_download_logs, download_file, organize_urls_data, update_description_pbar, download_files

# Utiles de las Listas
from utilsdsp.utilsdsp_list import remove_repeated_elements

# Utiles de los Diccionarios
from utilsdsp.utilsdsp_dict import join_list_to_dict
