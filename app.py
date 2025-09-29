from flask import Flask
import logging
from config.database import DatabasePool
import atexit
from dotenv import load_dotenv
import os

load_dotenv()

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s'
)

port = int(os.getenv("PORT", 5000))

def create_app():
    app = Flask(__name__)

    # Registrar blueprint

    # Cerrar pool al finalizar la app
    db_pool = DatabasePool()
    atexit.register(db_pool.close_all_connections)
    logging.info("Pool de conexiones inicializado")

    return app

if __name__ == "__main__":
    app = create_app()
    logging.info(f"App desplegada en puerto {port}")
    app.run(host="0.0.0.0", port=port, debug=True)
