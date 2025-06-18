# car_collector
Pontia: API para gestionar colecciones de coches

## Descripción

**car_collector** es una API RESTful desarrollada en Python con FastAPI y SQLAlchemy que permite a un coleccionista gestionar su colección de coches. Permite crear, consultar y actualizar coleccionistas, añadir coches a su colección, así como consultar marcas y modelos de vehículos.

## Características principales

- Gestión de coleccionistas (alta, consulta, modificación)
- Asociación de coches a coleccionistas
- Consulta de marcas y modelos de coches (datos obtenidos de una API externa)
- Validación de datos con Pydantic
- Endpoints RESTful

## Instalación

1. Clona el repositorio:
   ```sh
   git clone git@github.com:Jmotos/car_collector.git
   ```

2. Instala las dependencias:
   ```sh
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

3. Crea un archivo `.env` en la raíz con tu clave de API:
   ```
   RAPIDAPI_KEY=tu_clave_aqui
   ```

4. Inicia la aplicación:
   ```sh
   uvicorn main:app --reload
   ```

## Uso

La API expone los siguientes endpoints principales:

- `GET /collectors` — Lista todos los coleccionistas
- `GET /collectors/{username}` — Consulta un coleccionista por nombre de usuario
- `POST /collectors` — Crea un nuevo coleccionista
- `PUT /collectors/{username}` — Actualiza el email de un coleccionista
- `GET /collectors/{username}/cars` — Lista los coches de un coleccionista
- `GET /makes` — Lista las marcas de coches y sus modelos

Puedes probar la API usando [FastAPI](http://127.0.0.1:8000/) una vez que la app esté corriendo.

## Estructura del proyecto

```
app/
  car/
  collector/
  db/
  make/
  model/
main.py
test/
README.md
```

## Notas

- Los datos de marcas y modelos se obtienen automáticamente de manera asincrona de una API externa la primera vez que se inicia la app.
- Es necesario tener una clave válida de [RapidAPI](https://rapidapi.com/hub) para poblar la base de datos de marcas y modelos.

## Testeo

- En el directorio /test hay 3 archivos .http preparados para poder testear todas las funcionalidades de la API, así como la gestión de errores. Está diseñado para ser utilizado con la extensión [REST client](https://marketplace.visualstudio.com/items?itemName=humao.rest-client)
- En el directorio /test hay un archivo rest.py preparado para testear las principales funcionalidade de la API, aunque no es tan completo como los archivos .http
- En la rama db se incluye una base de datos sqlite ya creada, por si no se dispone de la API_KEY de [RapidAPI](https://rapidapi.com/hub) para hacer el poblado de marcas y modelos en la base de datos.

## Posibles mejoras a futuro

- Añadir autenticación para que solo el coleccionista pueda actualizar sus datos.
- Añadiro una funcionalidad para que los coleccionista puedan publicar ofertas de coches para poder venderlo a otro coleccionista.