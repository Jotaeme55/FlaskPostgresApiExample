from datetime import date
from typing import Optional, Dict, Any

class Libro:

    def __init__(
        self,
        titulo:str, 
        isbn:str,
        id: Optional[int] = None,
        anio_publicacion:Optional[int]=None,
        autor_id : Optional[int] = None
    ):
        
        if not titulo or not titulo.strip():
            raise ValueError("El título es obligatorio y no puede estar vacío")
        if not isbn or not isbn.strip():
            raise ValueError("El ISBN es obligatorio y no puede estar vacío")

        self.id=id
        self.titulo= titulo.strip()
        self.isbn=isbn.strip()
        self.anio_publicacion=anio_publicacion
        self.autor_id = autor_id


    def to_dict(self) -> Dict[str, Any]:
        """
        Convierte el libro a un diccionario.
        Útil para serializar a JSON en las respuestas de la API.
        
        Returns:
            dict: Representación del autor
        """
        return {
            "id":self.id,
            "titulo":self.titulo,
            "isbn":self.isbn,
            "anio_publicacion": self.anio_publicacion,
            "autor_id":self.autor_id
        }

    @staticmethod
    def from_db_row(row) -> Optional['Libro']:
        """
        Factory method para crear un Libro desde una fila de base de datos.
        
        Returns:
            Libro o None si row está vacía
        """
        if not row:
            return None
        
        return Libro(
            id=row["id"],
            titulo=row["titulo"],
            isbn=row["isbn"],
            anio_publicacion=row["anio_publicacion"],
            autor_id=row["autor_id"]
        )
    
    def __repr__(self) -> str:
        """Representación string del objeto para debugging."""
        return f"<Libro(id={self.id}, titulo='{self.titulo}')>"
    
    def __eq__(self, other) -> bool:
        """Compara dos autores por ID."""
        if not isinstance(other, Libro):
            return False
        return self.id == other.id if self.id and other.id else False