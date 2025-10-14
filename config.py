from dotenv import load_dotenv
import os

# Cargar las variables del archivo .env
load_dotenv()

# Obtener la clave secreta
SECRET_KEY = os.getenv("SECRET_KEY")
