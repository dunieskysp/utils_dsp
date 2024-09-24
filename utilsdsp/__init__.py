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

Oras funciones útiles.
    - obtain_URLfromHTML()
    - print_header()
    - clear_output()
    - calc_IMGdimensions()
    - optain_similarVars()
    - joinlist_to_dict()

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
"""

# Útiles de rutas.
from utilsdsp.utilsdsp_path import obtain_currentpath, obtain_absolutepath, change_currentpath, validate_path, join_path, obtain_defaultpath, obtain_downloadspath


# Útiles de directorios.
from utilsdsp.utilsdsp_dirs import create_dir, create_downloadsdir, create_symboliclink, delete_dir, del_emptydirs, select_contentdir, move_dir, move_files, copy_dir, rename_dir


# Útiles de ficheros.
from utilsdsp.utilsdsp_files import read_file, write_file


# Útiles de seneamiento de nombres de ficheros.
from utilsdsp.utilsdsp_sanitize import sanitize_filename


# Obtener tamaño de ficheros y directorios.
from utilsdsp.utilsdsp_sizefile import natural_size, obtain_sizedir, obtain_sizefile, obtain_size


# Comprimir ficheros y directorios.
from utilsdsp.utilsdsp_compress import compress, uncompress


# Otras funciones útiles.
from utilsdsp.utilsdsp_others import obtain_URLfromHTML, print_header, clear_output, calc_IMGdimensions, optain_similarVars, joinlist_to_dict


# Organizar los directorios.
from utilsdsp.utilsdsp_organizedirs import move_files_to_root, move_files_to_subdir, organize_files_by_type, organize_files_by_name

# Descargar ficheros desde internet.
from utilsdsp.utilsdsp_downloads import validate_and_resquest, obtain_filename, rename_download_file, update_download_logs, download_file, organize_urls_data, update_description_pbar, download_files

# Utiles de las listas
from utilsdsp.utilsdsp_list import remove_repeated_elements
