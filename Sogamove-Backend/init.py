from flask import Flask

def create_app():
    app = Flask(__name__)
    
    # Configuraciones
    app.config.from_pyfile('../config.py')

    # Registrar rutas
    from app.routes import routes_bp
    app.register_blueprint(routes_bp)

    return app
