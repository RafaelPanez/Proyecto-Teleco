# api.py

import requests
from config import SERVER_URL, REQUEST_TIMEOUT


def login(username, password):
    """
    Autentica un usuario en el servidor.

    Retorna:
        dict con la respuesta del servidor
    """

    url = f"{SERVER_URL}/login"

    data = {
        "username": username,
        "password": password
    }

    try:
        response = requests.post(
            url,
            json=data,
            timeout=REQUEST_TIMEOUT
        )

        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Error de conexión: {str(e)}"
        }


def upload_file(filepath, token, metadata):
    """
    Envía un archivo al servidor.

    filepath:
        ruta local del archivo

    token:
        JWT recibido en login

    metadata:
        información adicional del estudio
    """

    url = f"{SERVER_URL}/upload"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        with open(filepath, "rb") as file:

            files = {
                "file": file
            }

            response = requests.post(
                url,
                headers=headers,
                files=files,
                data=metadata,
                timeout=REQUEST_TIMEOUT
            )

        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Error de conexión: {str(e)}"
        }

    except FileNotFoundError:
        return {
            "success": False,
            "message": "Archivo no encontrado"
        }


def get_studies(token):
    """
    Obtiene la lista de estudios disponibles.
    """

    url = f"{SERVER_URL}/studies"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Error de conexión: {str(e)}"
        }


def get_study(study_code, token):
    """
    Obtiene la información de un estudio específico.
    """

    url = f"{SERVER_URL}/study/{study_code}"

    headers = {
        "Authorization": f"Bearer {token}"
    }

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )

        return response.json()

    except requests.exceptions.RequestException as e:
        return {
            "success": False,
            "message": f"Error de conexión: {str(e)}"
        }