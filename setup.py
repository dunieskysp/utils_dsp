from setuptools import setup, find_packages
from pathlib import Path

# La descripción larga va a ser el mismo fichero README.md
long_desc = Path("README.md").read_text()

# Datos del paquete
setup(
    name="utilsdsp",
    version="0.1.0",
    author="Duniesky Salazar Pérez",
    author_email="<duniesky.salazar@gmail.com>",
    description="Algunas funciones útiles",
    long_description=long_desc,
    long_description_content_type='text/markdown',
    url='https://github.com/dunieskysp/utils_dsp',
    packages=find_packages(),
    keywords=['python', 'utilsdsp'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]

)
