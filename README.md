# Gestor de Tareas

Este proyecto es una aplicación web para gestionar tareas, desarrollada con FastAPI y PostgreSQL. Permite crear, actualizar, eliminar e importar/exportar listas de tareas y sus tareas asociadas.

## Características

- **Gestión de Listas**: Crear, actualizar y eliminar listas de tareas.
- **Gestión de Tareas**: Añadir, actualizar y eliminar tareas dentro de las listas.
- **Importación/Exportación**: Importar y exportar datos de listas y tareas en formato JSON.
- **Interfaz de Usuario**: Interfaz web sencilla y fácil de usar.

## Tecnologías Utilizadas

- **Backend**: FastAPI
- **Base de Datos**: PostgreSQL
- **ORM**: SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript
- **Plantillas**: Jinja2

## Requisitos Previos

- Python 3.8+
- PostgreSQL
- Node.js (para gestionar dependencias de frontend si es necesario)

## Instalación

1. **Clonar el repositorio**:
   ```bash
   git clone https://github.com/tu_usuario/tu_repositorio.git
   cd tu_repositorio
   ```

2. **Configurar el entorno virtual**:
   ```bash
   python -m venv env
   source env/bin/activate  # En Windows usa `env\Scripts\activate`
   ```

3. **Instalar dependencias**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configurar la base de datos**:
   - Asegúrate de que PostgreSQL esté instalado y ejecutándose.
   - Crea una base de datos llamada `task_list`.
   - Actualiza la URL de la base de datos en `database.py` si es necesario.

5. **Iniciar la aplicación**:
   ```bash
   uvicorn main:app --reload
   ```

## Uso

- Accede a la aplicación en `http://localhost:8000`.
- Usa la interfaz para gestionar tus listas y tareas.
- Importa o exporta datos desde la sección correspondiente.

## Contribuciones

Las contribuciones son bienvenidas. Por favor, sigue los pasos estándar de GitHub para contribuir.

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.

