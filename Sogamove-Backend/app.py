from flask import Flask, jsonify, request
from flask_cors import CORS
from models import db, TravelHistory, User
from routes import main_routes
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

app = Flask(__name__)

# Configurar la URI para SQLite (base de datos principal)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///travel_history.db'

# Configurar la URI para PostgreSQL usando la variable de entorno
app.config['POSTGRES_URI'] = os.getenv('POSTGRES_DATABASE_URL')

# Desactivar el seguimiento de modificaciones de objetos
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurar múltiples bases de datos usando SQLALCHEMY_BINDS
app.config['SQLALCHEMY_BINDS'] = {
    'postgres': app.config['POSTGRES_URI']
}

app.secret_key = 'SogaMove'

CORS(app)

# Inicializar SQLAlchemy para ambas bases de datos
db.init_app(app)

# Intentar la conexión a la base de datos PostgreSQL
try:
    # Crear un engine para PostgreSQL
    engine = create_engine(app.config['POSTGRES_URI'])
    # Conectar y ejecutar una consulta para verificar la conexión
    with engine.connect() as connection:
        print("Conexión exitosa a PostgreSQL")
except Exception as e:
    print(f"No se pudo conectar a PostgreSQL. Error: {e}")

# Crear las tablas para SQLite y PostgreSQL si es necesario
with app.app_context():
    try:
        db.create_all()
    except Exception as e:
        print(f"Error creando tablas: {str(e)}")


    # Crear las tablas en PostgreSQL (usando el bind 'postgres' para especificar PostgreSQL)
    User.metadata.create_all(bind=db.engine)  # Crea las tablas en PostgreSQL

# Registrar rutas
app.register_blueprint(main_routes)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)

