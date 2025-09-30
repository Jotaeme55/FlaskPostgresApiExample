from typing import List, Optional, Callable, TypeVar
from config.database import DatabasePool
from repositories.BaseRepository import BaseRepository
import psycopg2.extras
import logging
from models.Autor import Autor
logger = logging.getLogger(__name__)
T = TypeVar('T')

class AutorRepository(BaseRepository[Autor]):
    """
    Repositorio concreto para Autores.
    
    Principios SOLID aplicados:
    - SRP: Solo se encarga de la persistencia de Autores
    - OCP: Extiende BaseRepository sin modificarlo
    - LSP: Puede sustituir a BaseRepository[Autor]
    - ISP: Implementa solo los métodos necesarios
    - DIP: Depende de la abstracción DatabasePool
    
    Patrón Template Method: _execute_query encapsula la lógica común
    """
    
    def __init__(self):
        self.db_pool = DatabasePool()
    
    def _execute_query(self, operation: Callable, operation_name: str, needs_commit: bool = False):
        """
        Template Method: Encapsula la lógica común de manejo de conexiones.
        
        Args:
            operation: Función que recibe cursor y ejecuta la operación
            operation_name: Nombre de la operación para logging
            needs_commit: Si la operación requiere commit (INSERT, UPDATE, DELETE)
            
        Returns:
            Resultado de la operación
        """
        conn = None
        try:
            conn = self.db_pool.get_connection()
            cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            
            result = operation(cursor)
            
            if needs_commit:
                conn.commit()
            
            cursor.close()
            return result
            
        except Exception as e:
            if conn and needs_commit:
                conn.rollback()
            logger.error(f"Error en {operation_name}: {e}")
            raise
        finally:
            if conn:
                self.db_pool.release_connection(conn)
    
    def get_by_id(self, id: int) -> Optional[Autor]:
        """
        Obtiene un autor por su ID.
        
        Args:
            id: ID del autor a buscar
            
        Returns:
            Autor o None si no existe
        """
        def operation(cursor):
            cursor.execute("SELECT * FROM autores WHERE id = %s", (id,))
            row = cursor.fetchone()
            
            if row:
                return Autor.from_db_row(row)
            return None
        
        return self._execute_query(operation, f"obtener autor ID {id}")
    
    def get_all(self) -> List[Autor]:
        """
        Obtiene todos los autores.
        
        Returns:
            Lista de autores
        """
        def operation(cursor):
            cursor.execute("SELECT * FROM autores ORDER BY nombre")
            rows = cursor.fetchall()
            
            return [ Autor.from_db_row(row) for row in rows ]
        
        return self._execute_query(operation, "obtener todos los autores")
    
    def add(self, entity: Autor) -> Autor:
        """
        Crea un nuevo autor.
        
        Args:
            entity: Autor a crear
            
        Returns:
            Autor creado con su ID asignado
        """
        def operation(cursor):
            cursor.execute(
                """
                INSERT INTO autores (nombre, nacionalidad, fecha_nacimiento)
                VALUES (%s, %s, %s)
                RETURNING id, nombre, nacionalidad, fecha_nacimiento
                """,
                (entity.nombre, entity.nacionalidad, entity.fecha_nacimiento)
            )
            
            row = cursor.fetchone()
            return Autor.from_db_row(row)
        
        return self._execute_query(operation, "crear autor", needs_commit=True)
    
    def update(self, entity: Autor) -> Autor:
        """
        Actualiza un autor existente.
        
        Args:
            entity: Autor con los datos actualizados
            
        Returns:
            Autor actualizado
        """
        def operation(cursor):
            cursor.execute(
                """
                UPDATE autores 
                SET nombre = %s, nacionalidad = %s, fecha_nacimiento = %s
                WHERE id = %s
                RETURNING id, nombre, nacionalidad, fecha_nacimiento
                """,
                (entity.nombre, entity.nacionalidad, entity.fecha_nacimiento, entity.id)
            )
            
            row = cursor.fetchone()
            
            if not row:
                raise ValueError(f"Autor con ID {entity.id} no encontrado")
            
            return Autor.from_db_row(row)
        
        return self._execute_query(operation, f"actualizar autor ID {entity.id}", needs_commit=True)
    
    def delete(self, id: int) -> bool:
        """
        Elimina un autor por su ID.
        
        Args:
            id: ID del autor a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        def operation(cursor):
            cursor.execute("DELETE FROM autores WHERE id = %s", (id,))
            return cursor.rowcount > 0
        
        return self._execute_query(operation, f"eliminar autor ID {id}", needs_commit=True)