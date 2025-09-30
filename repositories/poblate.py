from repositories.AutorRepository import AutorRepository
from repositories.LibroRepository import LibroRepository
from models.Autor import Autor
from models.Libro import Libro
from datetime import date

# Instanciar repositorios
autor_repo = AutorRepository()
libro_repo = LibroRepository()

# 1. Crear un autor
nuevo_autor = Autor(id=None, nombre="Gabriel García Márquez", nacionalidad="Colombiana", fecha_nacimiento=date(1927, 3, 6))
autor_creado = autor_repo.add(nuevo_autor)
print("Autor creado:", autor_creado)

# 2. Crear un libro asociado al autor
nuevo_libro = Libro(id=None, titulo="Cien años de soledad", isbn="9783161484100", anio_publicacion=1967, autor_id=1)
libro_creado = libro_repo.add(nuevo_libro)
print("Libro creado:", libro_creado)

# 3. Consultar los libros de ese autor
libros_autor = libro_repo.get_libros_from_autor(1)
print("Libros del autor:", libros_autor)
