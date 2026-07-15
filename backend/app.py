from flask import Flask
from flask_jwt_extended import JWTManager
from config import Config
from database import db
import logging 
from models import (
    Patient,
    Operator,
    Center,
    Study,
    File,
    Report,
    History,
    User
)
from routes import register_routes
import os 

app = Flask(__name__)

logging.basicConfig(

    filename="server.log",

    level=logging.INFO,

    format="%(asctime)s - %(levelname)s - %(message)s"
)
 
# Cargar configuración
app.config.from_object(Config)

# Inicializar JWT
jwt = JWTManager(app)

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)

# Inicializar la base de datos
db.init_app(app)

# Registrar todas las rutas de la API
register_routes(app)

@app.route("/")
def home():
    return "Servidor de Telemedicina funcionando correctamente."

if __name__ == "__main__":
    with app.app_context():
        db.create_all()  # Más adelante creará todas las tablas

    app.run(debug=True)