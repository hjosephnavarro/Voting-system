import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DB_HOST = os.getenv('DB_HOST', 'localhost')
    DB_USER = os.getenv('DB_USER', 'postgres')
    DB_PASSWORD = os.getenv('DB_PASSWORD', 'Contraseña')
    DB_NAME = os.getenv('DB_NAME', 'Voting')
    DB_PORT = os.getenv('DB_PORT', '5432')
    
    @staticmethod
    def get_db_url():
        return f"host={Config.DB_HOST} user={Config.DB_USER} password={Config.DB_PASSWORD} dbname={Config.DB_NAME} port={Config.DB_PORT}"