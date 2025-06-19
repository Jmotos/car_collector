# car_collector
Pontia: API para gestionar colecciones de coches

## Descripción

**car_collector** es una API RESTful desarrollada en Python con FastAPI y SQLAlchemy que permite a un coleccionista gestionar su colección de coches. Permite crear, consultar y actualizar coleccionistas, añadir coches a su colección, así como consultar marcas y modelos de vehículos.

## Características principales

- Gestión de coleccionistas (alta, consulta, modificación y eliminación)
- Asociación de coches a coleccionistas
- Consulta de marcas y modelos de coches (datos obtenidos de una API externa)
- Validación de datos con Pydantic
- Endpoints RESTful
- App dockerizada mediante docker-compose y que monta un volumen para persistir la base de datos

## Instalación

1. Clona el repositorio:
   ```sh
   git clone git@github.com:Jmotos/car_collector.git
   ```

2. Crea un archivo `.env` en la raíz con tu clave de [RapidAPI](https://rapidapi.com/hub):
   ```
   RAPIDAPI_KEY=tu_clave_aqui
   ```

3. Ejecuta el docker-compose
   ```
   docker-compose up --build
   ```

## Uso

La API expone los siguientes endpoints principales:

- `GET /collectors` — Lista todos los coleccionistas
- `GET /collectors/{username}` — Consulta un coleccionista por nombre de usuario
- `POST /collectors` — Crea un nuevo coleccionista
- `DELETE /collectors` — Elimina un coleccionista existente
- `PUT /collectors/{username}` — Actualiza el email de un coleccionista
- `GET /collectors/{username}/cars` — Lista los coches de un coleccionista
- `GET /makes` — Lista las marcas de coches y sus modelos

Conecta con la API accediendo a la [url](http://127.0.0.1:8000/)

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

## Posibles mejoras a futuro

- Añadir autenticación para que solo el coleccionista pueda actualizar sus datos.
- Añadir una funcionalidad para que los coleccionista puedan publicar ofertas de coches para poder venderlo a otro coleccionista.