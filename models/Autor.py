from datetime import date
from typing import Optional, Dict, Any

class Autor:

    """
    Representa un autor de libros.
    
    Principios aplicados:
    - Single Responsibility: solo maneja datos de autor
    - Encapsulación: atributos y métodos bien definidos
    """

    def __init__(
        self,
        id: Optional[int] = None,
        nombre: str = "",
        nacionalidad: Optional[str] = None,
        fecha_nacimiento: Optional[date] = None
    ):
        self.id = id
        self.nombre = nombre
        self.nacionalidad = nacionalidad
        self.fecha_nacimiento = fecha_nacimiento

    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el autor a un diccionario.
        Útil para serializar a JSON en las respuestas de la API.
        
        Returns:
            dict: Representación del autor
        """
        return {
            "id":self.id,
            "nombre":self.nombre,
            "nacionalidad":self.nacionalidad,
            "fecha_nacimiento": self.fecha_nacimiento.isoformat() if self.fecha_nacimiento else None
        }
    
    @staticmethod
    def from_db_row(row) -> Optional['Autor']:
        """
        Factory method para crear un Autor desde una fila de base de datos.
        
        Args:
            row: Tupla con (id, nombre, nacionalidad, fecha_nacimiento)
        
        Returns:
            Autor o None si row está vacía
        """
        if not row:
            return None
        
        return Autor(
            id=row['id'],
            nombre=row['nombre'],
            nacionalidad=row['nacionalidad'],
            fecha_nacimiento=row['fecha_nacimiento']
        )
    
    def __repr__(self) -> str:
        """Representación string del objeto para debugging."""
        return f"<Autor(id={self.id}, nombre='{self.nombre}')>"
    
    def __eq__(self, other) -> bool:
        """Compara dos autores por ID."""
        if not isinstance(other, Autor):
            return False
        return self.id == other.id if self.id and other.id else False