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
