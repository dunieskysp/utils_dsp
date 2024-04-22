"""
Útiles de dunieskysp.

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
"""

# Útiles de rutas.
from utilsdsp.utilsdsp_path import obtain_currentpath, obtain_absolutepath, change_currentpath, validate_path, join_path, obtain_defaultpath, obtain_downloadspath

# Útiles de directorios.
from utilsdsp.utilsdsp_dirs import create_dir, create_downloadsdir, create_symboliclink, delete_dir, select_files, move_dir, copy_dir, rename_dir

# Útiles de ficheros.
from utilsdsp.utilsdsp_files import read_file, write_file

# Útiles de seneamiento de nombres de ficheros.
from utilsdsp.utilsdsp_sanitize import sanitize_filename

# Obtener tamaño de ficheros y directorios.
from utilsdsp.utilsdsp_sizefile import natural_size, obtain_sizedir, obtain_sizefile, obtain_size

# Comprimir ficheros y directorios.
from utilsdsp.utilsdsp_compress import compress, uncompress
