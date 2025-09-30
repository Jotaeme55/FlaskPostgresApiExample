from typing import List, Optional, Callable, TypeVar
from config.database import DatabasePool
from repositories.BaseRepository import BaseRepository
import psycopg2.extras
import logging
from models.Libro import Libro
logger = logging.getLogger(__name__)
T = TypeVar('T')


class LibroRepository(BaseRepository[Libro]):

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


    def get_by_id(self, id):
        try:
            def operation(cursor):
                cursor.execute("SELECT * FROM libros WHERE id = %s",(id,))
                row = cursor.fetchone()
                if row:
                    return Libro.from_db_row(row)
        except Exception as e:
            logger.error("la funcion get ha tenido el siguiente error: %s", e)


        return self._execute_query(operation,"Obtener libro por id")
    
    
    def get_all(self) -> List[Libro]:
        """
        Obtiene todos los libros.
        
        Returns:
            Lista de libros
        """
        def operation(cursor):
            cursor.execute("SELECT * FROM libros ORDER BY titulo")
            rows = cursor.fetchall()
            
            return [ Libro.from_db_row(row) for row in rows ]
        
        return self._execute_query(operation, "obtener todos los libros")
    
    def add(self, entity: Libro) -> Libro:
        """
        Crea un nuevo Libro.
        
        Args:
            entity: Libro a crear
            
        Returns:
            Libro creado con su ID asignado
        """
        def operation(cursor):
            cursor.execute(
                """
                INSERT INTO libros (titulo, isbn, anio_publicacion,autor_id)
                VALUES (%s, %s, %s, %s)
                RETURNING id, titulo, isbn, anio_publicacion, autor_id
                """,
                (entity.titulo, entity.isbn, entity.anio_publicacion, entity.autor_id,)
            )
            
            row = cursor.fetchone()
            return Libro.from_db_row(row)
        
        return self._execute_query(operation, "crear libro", needs_commit=True)
    
    def update(self, entity: Libro) -> Libro:
        """
        Actualiza un libro existente.
        
        Args:
            entity: Libro con los datos actualizados
            
        Returns:
            Libro actualizado
        """
        def operation(cursor):
            cursor.execute(
                """
                UPDATE libros 
                SET titulo = %s, isbn = %s, anio_publicacion = %s, autor_id = %s
                WHERE id = %s
                RETURNING id, titulo, isbn, anio_publicacion, autor_id
                """,
                (entity.titulo, entity.isbn, entity.anio_publicacion, entity.autor_id, entity.id,)
            )
            
            row = cursor.fetchone()
            
            if not row:
                raise ValueError(f"Lbro con ID {entity.id} no encontrado")
            
            return Libro.from_db_row(row)
        
        return self._execute_query(operation, f"actualizar libro ID {entity.id}", needs_commit=True)
    
    def delete(self, id: int) -> bool:
        """
        Elimina un libro por su ID.
        
        Args:
            id: ID del libro a eliminar
            
        Returns:
            True si se eliminó, False si no existía
        """
        def operation(cursor):
            cursor.execute("DELETE FROM libros WHERE id = %s", (id,))
            return cursor.rowcount > 0
        
        return self._execute_query(operation, f"eliminar libro ID {id}", needs_commit=True)
    

    def get_libros_from_autor(self, autor_id) -> List[Libro]:
        """
        Función custom, obtiene los libros de un autor
        
        Args:
            id: ID del autor            
        Returns:
            Lista de libros con autor id
        """
        def operation(cursor):
            cursor.execute("SELECT * FROM libros l WHERE l.autor_id = %s", (autor_id,))
            rows = cursor.fetchall()
            return [Libro.from_db_row(row) for row in rows]
        
        return self._execute_query(operation, "obtener libros por autor")