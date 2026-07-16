# utils/auth.py

_token = None
_user = None


def save_session(token, username=None):
    """
    Guarda la sesión actual del usuario.
    """

    global _token, _user

    _token = token
    _user = username



def get_token():
    """
    Retorna el token JWT actual.
    """

    return _token



def get_user():
    """
    Retorna el usuario autenticado.
    """

    return _user



def clear_session():
    """
    Cierra la sesión actual.
    """

    global _token, _user

    _token = None
    _user = None



def is_logged_in():
    """
    Verifica si existe una sesión activa.
    """

    return _token is not None