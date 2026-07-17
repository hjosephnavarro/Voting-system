Sistema de Votación API

API REST para gestionar votaciones, votantes y candidatos. Desarrollada con FastAPI y PostgreSQL.

## Características

- Gestión completa de votantes (CRUD)
- Gestión completa de candidatos (CRUD)
- Sistema de votación con validaciones
- Estadísticas en tiempo real
- Documentación automática con Swagger/ReDoc
- Validaciones de integridad de datos
- Arquitectura en capas (Routes → Services → Repositories → Database)
- Eliminación lógica (soft delete)
- Manejo de errores con códigos HTTP apropiados

## Tecnologías

- **FastAPI** - Framework web moderno
- **PostgreSQL** - Base de datos relacional
- **Pydantic** - Validación de datos
- **Uvicorn** - Servidor ASGI
- **psycopg2** - Conector PostgreSQL

## Requisitos Previos

- Python 3.8 o superior
- PostgreSQL 12 o superior
- pip (gestor de paquetes de Python)

## Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/tu-usuario/voting-system.git
cd voting-system

1. Crear y activar entorno virtual
# Windows
python -m venv env
env\Scripts\activate

# Linux/Mac
python -m venv env
source env/bin/activate

2. Instalar dependencias
pip install -r requirements.txt

#otra opcion es
pip install fastapi
pip install uvicorn[standard]
pip install psycopg2-binary
pip install python-dotenv
pip install pydantic
pip install pydantic-settings
pip install email-validator

3.Configurar las variables en config.py

4.Ejecutar la aplicación
python run.py

La API estará disponible en: http://localhost:8000

Documentación de la API
Una vez ejecutada la aplicación, accede a:

Swagger UI: http://localhost:8000/api/docs

ReDoc: http://localhost:8000/api/redoc

Health Check: http://localhost:8000/health

#Endpoints
#Votantes
Método	Endpoint	Descripción
POST	/voters	Registrar un nuevo votante
GET	/voters	Obtener lista de votantes
GET	/voters/{id}	Obtener detalles de un votante
PUT	/voters/{id}	Actualizar un votante
DELETE	/voters/{id}	Eliminar un votante

#Candidatos
Método	Endpoint	Descripción
POST	/candidates	Registrar un nuevo candidato
GET	/candidates	Obtener lista de candidatos
GET	/candidates/{id}	Obtener detalles de un candidato
PUT	/candidates/{id}	Actualizar un candidato
DELETE	/candidates/{id}	Eliminar un candidato

#Votos
Método	Endpoint	Descripción
POST	/votes	Emitir un voto
GET	/votes	Obtener todos los votos
GET	/votes/{id}	Obtener detalles de un voto
GET	/votes/statistics	Obtener estadísticas de votación
DELETE	/votes/{id}	Eliminar un voto

5. Ejemplos de Uso
#Crear un votante
curl -X POST http://localhost:8000/voters \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Juan Perez",
    "email": "juan@email.com"
  }'

#Crear un candidato
curl -X POST http://localhost:8000/candidates \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Carlos Lopez",
    "email": "carlos@email.com",
    "party": "Partido Azul"
  }'

##Notas Importantes
Soft Delete y Estadisticas
El sistema utiliza eliminacion logica (soft delete) para preservar la integridad de los datos historicos. Esto significa que:

Al eliminar un votante, este se marca como eliminado pero no se borra fisicamente
Al eliminar un candidato, este se marca como eliminado pero no se borra fisicamente

IMPORTANTE: Los votos emitidos por votantes eliminados o hacia candidatos eliminados permanecen en el sistema y siguen siendo contabilizados en las estadisticas

Esto es intencional para mantener la integridad de los resultados historicos. Si se elimina un votante o candidato, los votos ya emitidos no se pierden.

Respuestas de la API
Todas las respuestas incluyen codigos HTTP estandar:

200 OK - Operacion exitosa
201 Created - Recurso creado
204 No Content - Eliminacion exitosa
400 Bad Request - Datos invalidos
404 Not Found - Recurso no encontrado
409 Conflict - Conflicto (email duplicado, voto ya emitido)
500 Internal Server Error - Error del servidor

Las imagenes andan en una carpeta llamada imagenes
