import psycopg2
from psycopg2 import Error, OperationalError
from app.config import Config

class Database:
    def __init__(self):
        self.connection = None
        self.cursor = None
    
    def connect(self):
        try:
            self.connection = psycopg2.connect(Config.get_db_url())
            self.cursor = self.connection.cursor()
            return True
        except OperationalError as e:
            print(f"Error de conexion: {e}")
            return False
        except Error as e:
            print(f"Error: {e}")
            return False
    
    def disconnect(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
    
    def execute_query(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            self.connection.commit()
            return True
        except Error as e:
            print(f"Error en la consulta: {e}")
            self.connection.rollback()
            return False
    
    def fetch_all(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchall()
        except Error as e:
            print(f"Error en la consulta: {e}")
            return []
    
    def fetch_one(self, query, params=None):
        try:
            self.cursor.execute(query, params or ())
            return self.cursor.fetchone()
        except Error as e:
            print(f"Error en la consulta: {e}")
            return None