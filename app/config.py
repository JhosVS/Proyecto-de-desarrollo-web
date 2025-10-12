import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY", "clave_segura_agricola")
    DB_SERVER = os.environ.get("DB_SERVER", "localhost")
    DB_NAME = os.environ.get("DB_NAME", "INVENTARIO")
    DB_USER = os.environ.get("DB_USER", "sa")
    DB_PASSWORD = os.environ.get("DB_PASSWORD", "undac")
