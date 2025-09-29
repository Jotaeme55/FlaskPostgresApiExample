# Sistema de Gestión de Libros y Autores

API REST desarrollada con Flask utilizando arquitectura por capas para gestionar libros y autores con base de datos PostgreSQL.

## 📋 Descripción

Este proyecto implementa un backend con arquitectura en capas (controllers, services, repositories, models) para practicar buenas prácticas de desarrollo. Permite crear y consultar información sobre libros y autores con sus respectivas relaciones.

## 🏗️ Arquitectura

```
/proyecto
├── /controllers      # Endpoints y rutas de Flask
├── /services         # Lógica de negocio
├── /repositories     # Acceso a datos (queries SQL)
├── /models           # Modelos de datos (Libro, Autor)
├── /config           # Configuración de base de datos
├── app.py            # Punto de entrada de la aplicación
├── requirements.txt  # Dependencias del proyecto
├── .env              # Variables de entorno (no incluir en git)
└── README.md
```

## 🚀 Tecnologías

- **Flask** - Framework web
- **PostgreSQL** - Base de datos relacional
- **psycopg2** - Adaptador de PostgreSQL para Python
- **python-dotenv** - Gestión de variables de entorno

## 📦 Instalación

### Prerrequisitos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

### Pasos

1. **Clonar el repositorio**
```bash
git clone <url-del-repositorio>
cd proyecto
```

2. **Crear entorno virtual**
```bash
python -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

3. **Instalar dependencias**
```bash
pip install -r requirements.txt
```

4. **Configurar base de datos**

Crear la base de datos en PostgreSQL:
```bash
psql -U postgres
CREATE DATABASE libros_db;
```

Ejecutar el script de creación de tablas:
```sql
CREATE TABLE autores (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    nacionalidad VARCHAR(50),
    fecha_nacimiento DATE
);

CREATE TABLE libros (
    id SERIAL PRIMARY KEY,
    titulo VARCHAR(200) NOT NULL,
    isbn VARCHAR(13) UNIQUE NOT NULL,
    anio_publicacion INTEGER,
    autor_id INTEGER REFERENCES autores(id) ON DELETE CASCADE
);
```

5. **Configurar variables de entorno**

Crear archivo `.env` en la raíz del proyecto:
```env
DB_HOST=localhost
DB_PORT=5432
DB_NAME=libros_db
DB_USER=postgres
DB_PASSWORD=tu_contraseña
FLASK_ENV=development
```

6. **Ejecutar la aplicación**
```bash
python app.py
```

La API estará disponible en `http://localhost:5000`

## 📚 Endpoints

### Autores

- **GET** `/api/autores` - Obtener todos los autores
- **POST** `/api/autores` - Crear un nuevo autor
  ```json
  {
    "nombre": "Gabriel García Márquez",
    "nacionalidad": "Colombiano",
    "fecha_nacimiento": "1927-03-06"
  }
  ```
- **GET** `/api/autores/<id>/libros` - Obtener todos los libros de un autor

### Libros

- **GET** `/api/libros` - Obtener todos los libros
- **GET** `/api/libros/<id>` - Obtener un libro por ID (incluye información del autor)
- **POST** `/api/libros` - Crear un nuevo libro
  ```json
  {
    "titulo": "Cien años de soledad",
    "isbn": "9780307474728",
    "anio_publicacion": 1967,
    "autor_id": 1
  }
  ```

## 🗂️ Modelos de Datos

### Autor
- `id` (SERIAL PRIMARY KEY)
- `nombre` (VARCHAR)
- `nacionalidad` (VARCHAR)
- `fecha_nacimiento` (DATE)

### Libro
- `id` (SERIAL PRIMARY KEY)
- `titulo` (VARCHAR)
- `isbn` (VARCHAR UNIQUE)
- `anio_publicacion` (INTEGER)
- `autor_id` (FOREIGN KEY → autores.id)

**Relación**: Un autor puede tener muchos libros (1:N)

## 🎯 Capas de la Arquitectura

### Controllers
Gestionan las peticiones HTTP y las respuestas. No contienen lógica de negocio.

### Services
Contienen la lógica de negocio (validaciones, transformaciones, reglas).

### Repositories
Manejan el acceso a la base de datos (queries SQL).

### Models
Definen las estructuras de datos utilizadas en la aplicación.

## 🧪 Pruebas con cURL

```bash
# Crear un autor
curl -X POST http://localhost:5000/api/autores \
  -H "Content-Type: application/json" \
  -d '{"nombre":"Isabel Allende","nacionalidad":"Chilena","fecha_nacimiento":"1942-08-02"}'

# Crear un libro
curl -X POST http://localhost:5000/api/libros \
  -H "Content-Type: application/json" \
  -d '{"titulo":"La casa de los espíritus","isbn":"9788497592208","anio_publicacion":1982,"autor_id":1}'

# Obtener todos los libros
curl http://localhost:5000/api/libros
```

## 🔒 Seguridad

- No incluir el archivo `.env` en el control de versiones
- Agregar `.env` al archivo `.gitignore`
- Usar contraseñas seguras para la base de datos
- Implementar validación de datos en la capa de servicios

## 📝 Notas

Este es un proyecto educativo para practicar arquitectura por capas. Para un entorno de producción se recomienda:
- Implementar autenticación y autorización
- Agregar pruebas unitarias e integración
- Usar migraciones de base de datos (Alembic)
- Implementar logging apropiado
- Agregar manejo de errores más robusto
- Documentar la API con Swagger/OpenAPI

## 📄 Licencia

Este proyecto es de uso educativo.