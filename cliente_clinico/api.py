# api.py

import requests
import mimetypes
import os
from config import SERVER_URL, REQUEST_TIMEOUT



def login(username, password):
    """
    Inicio de sesión.
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
            "error": True,
            "message": f"Error de conexión: {str(e)}"
        }



def upload_file(filepath, token, metadata):
    """
    Subida de estudios.
    Envía:
    - archivo real
    - campos del estudio
    - JWT
    """

    url = f"{SERVER_URL}/upload"


    headers = {
        "Authorization": f"Bearer {token}"
    }


    try:

        with open(filepath, "rb") as file:

            # Detectar tipo MIME del archivo
            file_type, _ = mimetypes.guess_type(filepath)


            # Si no se reconoce la extensión
            # se manda un tipo genérico
            if file_type is None:

                file_type = "application/octet-stream"


            filename = os.path.basename(filepath)


            files = {

                "file": (
                 filename,
                    file,
                    file_type
                )

            }


            response = requests.post(
                url,
                headers=headers,
                files=files,
                data=metadata,
                timeout=REQUEST_TIMEOUT
            )


        print("STATUS:", response.status_code)
        print("RESPUESTA:", response.text)


        return response.json()



    except FileNotFoundError:

        return {
            "error": True,
            "message": "Archivo no encontrado"
        }



    except requests.exceptions.RequestException as e:

        return {
            "error": True,
            "message": f"Error de conexión: {str(e)}"
        }



def get_studies(token):
    """
    Obtiene todos los estudios.
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


        print("STATUS:", response.status_code)
        print("RESPUESTA:", response.text)


        return response.json()



    except requests.exceptions.RequestException as e:

        return {
            "error": True,
            "message": f"Error de conexión: {str(e)}"
        }



def get_study(study_code, token):
    """
    Obtiene un estudio específico.
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


        print("STATUS:", response.status_code)
        print("RESPUESTA:", response.text)


        return response.json()



    except requests.exceptions.RequestException as e:

        return {
            "error": True,
            "message": f"Error de conexión: {str(e)}"
        }
    
def delete_study(study_code, token):
    """
    Elimina un estudio del servidor.
    """

    url = f"{SERVER_URL}/study/{study_code}"

    headers = {
        "Authorization": f"Bearer {token}"
    }


    try:

        response = requests.delete(
            url,
            headers=headers,
            timeout=REQUEST_TIMEOUT
        )


        print("STATUS:", response.status_code)
        print("RESPUESTA:", response.text)


        return response.json()


    except requests.exceptions.RequestException as e:

        return {
            "error": True,
            "message": str(e)
        }
