
import psycopg2
from psycopg2 import pool
import os
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

class DatabasePool:
    """
    Singleton que gestiona un pool de conexiones a PostgreSQL.
    Garantiza una única instancia del pool en toda la aplicación.
    """
    _instance = None
    _pool = None

    def __new__(cls):
        """
        Implementación del patrón Singleton.
        Solo crea una instancia la primera vez que se llama.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)

            db_name = os.getenv('DB_NAME')
            db_user = os.getenv('DB_USER')
            db_password = os.getenv('DB_PASSWORD')

            if not all([db_name, db_user, db_password]):
                raise ValueError("❌ Variables de entorno para la BD no configuradas correctamente")


            cls._instance._pool = pool.SimpleConnectionPool(
                minconn=2,   # Mínimo de conexiones siempre abiertas
                maxconn=10,  # Máximo de conexiones permitidas
                host=os.getenv('DB_HOST', 'localhost'),
                port=os.getenv('DB_PORT', '5432'),
                database=db_name,
                user=db_user,
                password=os.getenv('DB_PASSWORD')
            )

        return cls._instance
    
    def get_connection(self):
        """
        Obtiene una conexión del pool.
        
        Returns:
            connection: Conexión a PostgreSQL
        """
        if self._pool:
            return self._pool.getconn()
        raise Exception("Pool no inicializado")
    
    def release_connection(self, connection):
        """
        Devuelve una conexión al pool para ser reutilizada.
        
        Args:
            connection: Conexión a devolver
        """
        if self._pool:
            self._pool.putconn(connection)
    
    def close_all_connections(self):
        """
        Cierra todas las conexiones del pool.
        Llamar al finalizar la aplicación.
        """
        if self._pool:
            self._pool.closeall()
            print("🔒 Pool de conexiones cerrado")