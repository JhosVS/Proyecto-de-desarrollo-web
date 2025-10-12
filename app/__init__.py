from flask import Flask
from app.config import Config
from app.db import get_connection

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Conexión test al iniciar
    @app.before_request
    def before_request():
        conn = get_connection()
        if conn:
            conn.close()

    # Registrar rutas
    from app.routes import main_bp
    app.register_blueprint(main_bp)

    return app
