# utils/validators.py


def validate_login(username, password):
    """
    Valida los campos del formulario de login.
    """

    if not username:
        return False, "Ingrese usuario"

    if not password:
        return False, "Ingrese contraseña"

    return True, ""



def validate_file(filepath):
    """
    Verifica que exista una ruta de archivo.
    """

    if not filepath:
        return False, "Seleccione un archivo"

    return True, ""