import pyodbc
from app.config import Config

def get_connection():
    try:
        conn = pyodbc.connect(
            f"DRIVER={{ODBC Driver 17 for SQL Server}};"
            f"SERVER={Config.DB_SERVER};"
            f"DATABASE={Config.DB_NAME};"
            f"UID={Config.DB_USER};"
            f"PWD={Config.DB_PASSWORD}"
        )
        return conn
    except Exception as e:
        print("❌ Error de conexión:", e)
        return None
