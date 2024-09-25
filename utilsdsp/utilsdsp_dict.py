"""
Operaciones con Diccioanrios:
    - join_list_to_dict: Unir dos listas en un diccionario
"""

from outputstyles import warning, bold, error


def join_list_to_dict(key_list: list, value_list: list, keys_to_str: bool = True) -> dict:
    """
    Unir dos listas en un diccionario

    Parameters:    
    key_list (list): Lista con las llaves
    value_list (list): Lista con los valores
    keys_to_str (bool): Convertir las llaves a string

    Ej (Deben tener la misma longitud):
    - key_list = ["txt", "jpg"]
    - value_list = ["Textos", "Imagenes"]

    Returns:
    dict: Diccionario con las llaves y valores asociados
    """

    def __liststr(data_list: list) -> list:
        """
        Convertir los datos de una lista a string
        """

        return [str(item) for item in data_list]

    # Comprobar que se correspondan las longitudes
    if len(key_list) != len(value_list):

        print(warning("Las longitudes no se corresponden:", "ico"))
        print(bold("Keys:"), key_list)
        print(bold("Values:"), value_list)

        return

    # Convertir las llaves a string
    keys = __liststr(key_list) if keys_to_str else key_list

    # Relacionar las dos listas en un diccionario.
    try:
        return {key: value for key, value in zip(keys, value_list)}

    except Exception as err:

        print(error("No se pudo crear el diccionario desde las dos listas.", "ico"))
        print(bold("Keys:"), key_list)
        print(bold("Values:"), value_list)
        print(err)
