# Backend Plataforma Telemedicina

## Descripción
Servidor central encargado de recibir información clínica desde centros remotos,
registrar metadatos, almacenar archivos y permitir consultas autorizadas.

## Tecnologías
- Flask
- Flask-JWT-Extended
- SQLAlchemy
- SQLite

## Ejecución

Instalar dependencias:

pip install -r requirements.txt

Ejecutar:

python app.py


## Endpoints

POST /login
Obtiene token JWT.

POST /upload
Recibe archivos clínicos y metadatos.

GET /studies
Consulta estudios registrados.

GET /study/<study_code>
Consulta un estudio específico.


## Seguridad implementada

- Autenticación JWT.
- Bloqueo después de 3 intentos fallidos.
- Validación de campos obligatorios.
- SHA256 para verificar integridad.
- Registro de eventos mediante logs.
