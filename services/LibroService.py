from typing import List, Optional
from repositories.LibroRepository import LibroRepository
from repositories.AutorRepository import AutorRepository
from models.Libro import Libro
import logging

logger = logging.getLogger(__name__)

class LibroService:
    """
    Servicio de lógica de negocio para Libros.
    
    Responsabilidades:
    - Validación de datos de negocio
    - Validación de relaciones (autor existe)
    - Orquestación entre múltiples repositorios
    - Enriquecimiento de datos (incluir info del autor)
    
    Principios SOLID:
    - SRP: Solo maneja lógica de negocio de libros
    - DIP: Depende de abstracciones (repositorios)
    - OCP: Extensible sin modificar repositorios
    """
    
    def __init__(self, 
                 libro_repository: LibroRepository = None,
                 autor_repository: AutorRepository = None):
        """
        Inicializa el servicio con inyección de dependencias.
        
        Args:
            libro_repository: Repositorio de libros (opcional para testing)
            autor_repository: Repositorio de autores (opcional para testing)
        """
        self.libro_repo = libro_repository or LibroRepository()
        self.autor_repo = autor_repository or AutorRepository()
    
    def crear_libro(self, datos: dict) -> dict:
        """
        Crea un nuevo libro con validaciones de negocio.
        
        Valida que:
        - Los datos sean correctos
        - El autor exista en la BD
        
        Args:
            datos: Diccionario con {titulo, autor_id, año_publicacion, genero}
            
        Returns:
            Diccionario con el libro creado + información del autor
            
        Raises:
            ValueError: Si los datos no son válidos o el autor no existe
        """
        # Validar datos básicos
        self._validar_datos_libro(datos)
        
        # Validar que el autor existe (regla de negocio crítica)
        autor_id = datos['autor_id']
        autor = self.autor_repo.get_by_id(autor_id)
        
        if not autor:
            raise ValueError(f"El autor con ID {autor_id} no existe")
        
        # Crear entidad libro
        libro = Libro.from_dict(datos)
        
        # Persistir
        libro_creado = self.libro_repo.add(libro)
        
        logger.info(f"Libro creado: '{libro_creado.titulo}' (ID: {libro_creado.id}) del autor {autor.nombre}")
        
        # Retornar con información del autor incluida
        return self._enriquecer_libro_con_autor(libro_creado, autor)
    
    def obtener_libro_por_id(self, id: int) -> Optional[dict]:
        """
        Obtiene un libro por su ID con información del autor incluida.
        
        Args:
            id: ID del libro
            
        Returns:
            Diccionario con libro + autor, o None si no existe
            
        Raises:
            ValueError: Si el ID no es válido
        """
        if id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        libro = self.libro_repo.get_by_id(id)
        
        if not libro:
            logger.warning(f"Libro con ID {id} no encontrado")
            return None
        
        # Obtener información del autor
        autor = self.autor_repo.get_by_id(libro.autor_id)
        
        return self._enriquecer_libro_con_autor(libro, autor)
    
    def obtener_todos_libros(self) -> List[dict]:
        """
        Obtiene todos los libros con información de sus autores.
        
        Returns:
            Lista de diccionarios con libros + autores
        """
        libros = self.libro_repo.get_all()
        
        logger.info(f"Obtenidos {len(libros)} libros")
        return libros
    
    def obtener_libros_por_autor(self, autor_id: int) -> List[dict]:
        """
        Obtiene todos los libros de un autor específico.
        
        Args:
            autor_id: ID del autor
            
        Returns:
            Lista de libros del autor con información completa
            
        Raises:
            ValueError: Si el autor no existe
        """
        # Validar que el autor existe
        autor = self.autor_repo.get_by_id(autor_id)
        
        if not autor:
            raise ValueError(f"El autor con ID {autor_id} no existe")
        
        # Obtener libros del autor
        libros = self.libro_repo.get_by_autor_id(autor_id)
        
        # Enriquecer con información del autor
        libros_enriquecidos = [
            self._enriquecer_libro_con_autor(libro, autor)
            for libro in libros
        ]
        
        logger.info(f"Obtenidos {len(libros)} libros del autor {autor.nombre}")
        return libros_enriquecidos
    
    def actualizar_libro(self, id: int, datos: dict) -> dict:
        """
        Actualiza un libro existente.
        
        Args:
            id: ID del libro a actualizar
            datos: Datos nuevos del libro
            
        Returns:
            Libro actualizado con información del autor
            
        Raises:
            ValueError: Si los datos no son válidos o el libro/autor no existe
        """
        # Validar que el libro existe
        libro_existente = self.libro_repo.get_by_id(id)
        if not libro_existente:
            raise ValueError(f"Libro con ID {id} no encontrado")
        
        # Validar datos
        self._validar_datos_libro(datos)
        
        # Validar que el nuevo autor existe
        autor = self.autor_repo.get_by_id(datos['autor_id'])
        if not autor:
            raise ValueError(f"El autor con ID {datos['autor_id']} no existe")
        
        # Crear entidad actualizada
        libro = Libro(
            id=id,
            titulo=datos['titulo'],
            autor_id=datos['autor_id'],
            año_publicacion=datos['año_publicacion'],
            genero=datos['genero']
        )
        
        # Persistir
        libro_actualizado = self.libro_repo.update(libro)
        
        logger.info(f"Libro actualizado: '{libro_actualizado.titulo}' (ID: {id})")
        
        return self._enriquecer_libro_con_autor(libro_actualizado, autor)
    
    def eliminar_libro(self, id: int) -> bool:
        """
        Elimina un libro por su ID.
        
        Args:
            id: ID del libro a eliminar
            
        Returns:
            True si se eliminó, False si no existía
            
        Raises:
            ValueError: Si el ID no es válido
        """
        if id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        eliminado = self.libro_repo.delete(id)
        
        if eliminado:
            logger.info(f"Libro con ID {id} eliminado")
        else:
            logger.warning(f"Libro con ID {id} no encontrado para eliminar")
        
        return eliminado
    
    def _validar_datos_libro(self, datos: dict) -> None:
        """
        Valida los datos de un libro según reglas de negocio.
        
        Args:
            datos: Diccionario con los datos del libro
            
        Raises:
            ValueError: Si alguna validación falla
        """
        # Validar campos requeridos
        campos_requeridos = ['titulo', 'autor_id', 'año_publicacion', 'genero']
        for campo in campos_requeridos:
            if campo not in datos or datos[campo] is None:
                raise ValueError(f"El campo '{campo}' es requerido")
        
        # Validar título
        titulo = str(datos['titulo']).strip()
        if len(titulo) < 1:
            raise ValueError("El título no puede estar vacío")
        
        # Validar autor_id
        try:
            autor_id = int(datos['autor_id'])
            if autor_id <= 0:
                raise ValueError("El ID del autor debe ser positivo")
        except (ValueError, TypeError):
            raise ValueError("El ID del autor debe ser un número válido")
        
        # Validar año de publicación
        try:
            año = int(datos['año_publicacion'])
            if año < 1000 or año > 2100:
                raise ValueError("El año de publicación debe estar entre 1000 y 2100")
        except (ValueError, TypeError):
            raise ValueError("El año de publicación debe ser un número válido")
        
        # Validar género
        genero = str(datos['genero']).strip()
        if len(genero) < 2:
            raise ValueError("El género debe tener al menos 2 caracteres")
    
    def _enriquecer_libro_con_autor(self, libro: Libro, autor) -> dict:
        """
        Combina la información del libro con la del autor.
        
        Args:
            libro: Entidad Libro
            autor: Entidad Autor (puede ser None)
            
        Returns:
            Diccionario con libro + autor anidado
        """
        libro_dict = libro.to_dict()
        
        # Añadir información del autor
        libro_dict['autor'] = autor.to_dict() if autor else None
        
        return libro_dict