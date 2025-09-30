from typing import List, Optional
from repositories.AutorRepository import AutorRepository
from models.Autor import Autor
import logging

logger = logging.getLogger(__name__)

class AutorService:
    """
    Servicio de lógica de negocio para Autores.
    
    Responsabilidades:
    - Validación de datos de negocio
    - Orquestación de operaciones complejas
    - Manejo de reglas de negocio
    - Transformación de datos entre capas
    
    Principios SOLID:
    - SRP: Solo maneja lógica de negocio de autores
    - DIP: Depende de la abstracción AutorRepository
    - OCP: Extensible sin modificar AutorRepository
    """
    
    def __init__(self, autor_repository: AutorRepository = None):
        """
        Inicializa el servicio con inyección de dependencias.
        
        Args:
            autor_repository: Repositorio de autores (opcional para testing)
        """
        self.autor_repo = autor_repository or AutorRepository()
    
    def crear_autor(self, datos: dict) -> Autor:
        """
        Crea un nuevo autor con validaciones de negocio.
        
        Args:
            datos: Diccionario con {nombre, nacionalidad, fecha_nacimiento}
            
        Returns:
            Autor creado
            
        Raises:
            ValueError: Si los datos no son válidos
        """
        # Validaciones de negocio
        self._validar_datos_autor(datos)
        
        # Crear entidad
        autor = Autor.from_dict(datos)
        
        # Persistir
        autor_creado = self.autor_repo.add(autor)
        
        logger.info(f"Autor creado: {autor_creado.nombre} (ID: {autor_creado.id})")
        return autor_creado
    
    def obtener_autor_por_id(self, id: int) -> Optional[Autor]:
        """
        Obtiene un autor por su ID.
        
        Args:
            id: ID del autor
            
        Returns:
            Autor o None si no existe
            
        Raises:
            ValueError: Si el ID no es válido
        """
        if id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        autor = self.autor_repo.get_by_id(id)
        
        if not autor:
            logger.warning(f"Autor con ID {id} no encontrado")
        
        return autor
    
    def obtener_todos_autores(self) -> List[Autor]:
        """
        Obtiene todos los autores ordenados.
        
        Returns:
            Lista de autores
        """
        autores = self.autor_repo.get_all()
        logger.info(f"Obtenidos {len(autores)} autores")
        return autores
    
    def actualizar_autor(self, id: int, datos: dict) -> Autor:
        """
        Actualiza un autor existente.
        
        Args:
            id: ID del autor a actualizar
            datos: Datos nuevos del autor
            
        Returns:
            Autor actualizado
            
        Raises:
            ValueError: Si los datos no son válidos o el autor no existe
        """
        # Validar que existe
        autor_existente = self.obtener_autor_por_id(id)
        if not autor_existente:
            raise ValueError(f"Autor con ID {id} no encontrado")
        
        # Validar nuevos datos
        self._validar_datos_autor(datos)
        
        # Crear entidad actualizada
        autor = Autor(
            id=id,
            nombre=datos['nombre'],
            nacionalidad=datos['nacionalidad'],
            fecha_nacimiento=datos['fecha_nacimiento']
        )
        
        # Persistir
        autor_actualizado = self.autor_repo.update(autor)
        
        logger.info(f"Autor actualizado: {autor_actualizado.nombre} (ID: {id})")
        return autor_actualizado
    
    def eliminar_autor(self, id: int) -> bool:
        """
        Elimina un autor por su ID.
        
        Args:
            id: ID del autor a eliminar
            
        Returns:
            True si se eliminó, False si no existía
            
        Raises:
            ValueError: Si el ID no es válido
        """
        if id <= 0:
            raise ValueError("El ID debe ser un número positivo")
        
        eliminado = self.autor_repo.delete(id)
        
        if eliminado:
            logger.info(f"Autor con ID {id} eliminado")
        else:
            logger.warning(f"Autor con ID {id} no encontrado para eliminar")
        
        return eliminado
    
    def _validar_datos_autor(self, datos: dict) -> None:
        """
        Valida los datos de un autor según reglas de negocio.
        
        Args:
            datos: Diccionario con los datos del autor
            
        Raises:
            ValueError: Si alguna validación falla
        """
        # Validar campos requeridos
        campos_requeridos = ['nombre', 'nacionalidad', 'fecha_nacimiento']
        for campo in campos_requeridos:
            if campo not in datos or not datos[campo]:
                raise ValueError(f"El campo '{campo}' es requerido")
        
        # Validar nombre (al menos 2 caracteres, solo letras y espacios)
        nombre = datos['nombre'].strip()
        if len(nombre) < 2:
            raise ValueError("El nombre debe tener al menos 2 caracteres")
        
        if not all(c.isalpha() or c.isspace() for c in nombre):
            raise ValueError("El nombre solo puede contener letras y espacios")
        
        # Validar nacionalidad (al menos 2 caracteres)
        nacionalidad = datos['nacionalidad'].strip()
        if len(nacionalidad) < 2:
            raise ValueError("La nacionalidad debe tener al menos 2 caracteres")
        
        # Validar formato de fecha (básico)
        fecha = datos['fecha_nacimiento']
        if not self._validar_formato_fecha(fecha):
            raise ValueError("La fecha debe estar en formato YYYY-MM-DD")
    
    def _validar_formato_fecha(self, fecha: str) -> bool:
        """
        Valida que una fecha tenga formato YYYY-MM-DD.
        
        Args:
            fecha: String con la fecha
            
        Returns:
            True si es válida
        """
        try:
            from datetime import datetime
            datetime.strptime(fecha, '%Y-%m-%d')
            return True
        except ValueError:
            return False