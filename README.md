# Recomendador de Películas API

Este proyecto es una API de recomendación de películas basada en la similitud de coseno entre las características de las películas. La API también proporciona información adicional sobre películas, actores y directores, como la cantidad de filmaciones en un mes específico, el score de popularidad de una película, o la cantidad de votos de una película.

## Tabla de Contenidos

- Uso
- Endpoints

### Requisitos
- Python 3.7 o superior.
- Bibliotecas:
  - FastAPI
  - Uvicorn
  - Pandas
  - scikit-learn

### Instrucciones
La API ofrece varios endpoints para obtener información sobre películas, actores y directores, así como recomendaciones basadas en un título dado.

## Uso

La API ofrece varios endpoints para obtener información sobre películas, actores y directores, así como recomendaciones basadas en un título dado.

### Endpoints

#### `/cantidad_filmaciones_mes/{mes}`

Devuelve la cantidad de filmaciones realizadas en un mes específico.

- **Parámetro**: `mes` (str): Nombre del mes en español.

- **Ejemplo de uso**:
    ```bash
    GET /cantidad_filmaciones_mes/enero
    ```

- **Respuesta**:
    ```json
    {
        "mensaje": "50 cantidad de películas fueron estrenadas en el mes de enero"
    }
    ```

#### `/cantidad_filmaciones_dia/{dia}`

Devuelve la cantidad de filmaciones realizadas en un día específico de la semana.

- **Parámetro**: `dia` (str): Nombre del día en español.

- **Ejemplo de uso**:
    ```bash
    GET /cantidad_filmaciones_dia/lunes
    ```

- **Respuesta**:
    ```json
    {
        "mensaje": "10 películas fueron estrenadas un lunes"
    }
    ```

#### `/score_titulo/{titulo}`

Devuelve el año de estreno y el score de popularidad de una película por su título.

- **Parámetro**: `titulo` (str): El título de la película.

- **Ejemplo de uso**:
    ```bash
    GET /score_titulo/Inception
    ```

- **Respuesta**:
    ```json
    {
        "mensaje": "La película Inception fue estrenada en 2010 con un score/popularidad de 8.8"
    }
    ```

#### `/votos_titulo/{titulo}`

Devuelve la cantidad de votos y el promedio de votos de una película por su título.

- **Parámetro**: `titulo` (str): El título de la película.

- **Ejemplo de uso**:
    ```bash
    GET /votos_titulo/Inception
    ```

- **Respuesta**:
    ```json
    {
        "mensaje": "La película Inception tiene 2500 valoraciones con un promedio de 8.5"
    }
    ```

#### `/get_actor/{nombre_actor}`

Devuelve información sobre un actor: cuántas películas ha hecho y el retorno de esas películas.

- **Parámetro**: `nombre_actor` (str): El nombre del actor o actriz.

- **Ejemplo de uso**:
    ```bash
    GET /get_actor/Leonardo%20DiCaprio
    ```

- **Respuesta**:
    ```json
    {
        "mensaje": "Leonardo DiCaprio ha participado en 15 filmaciones, ha conseguido un retorno total de 1500.00 con un promedio de 100.00 por filmación."
    }
    ```

#### `/get_director/{nombre_director}`

Devuelve información sobre un director: retorno total de sus películas y detalles de cada una.

- **Parámetro**: `nombre_director` (str): El nombre del director o directora.

- **Ejemplo de uso**:
    ```bash
    GET /get_director/Christopher%20Nolan
    ```

- **Respuesta**:
    ```json
    {
        "mensaje": "Christopher Nolan ha conseguido un retorno total de 5000.00.",
        "Película 1": "Título: Inception, Fecha de lanzamiento: 2010-07-16, Costo: 160000000, Ganancia: 800000000.",
        "Película 2": "Título: Interstellar, Fecha de lanzamiento: 2014-11-07, Costo: 165000000, Ganancia: 677000000."
    }
    ```

#### `/recomendacion/{titulo}`

Devuelve una lista de películas recomendadas basadas en la similitud de características con un título proporcionado.

- **Parámetro**: `titulo` (str): El título de la película a partir de la cual se quieren obtener recomendaciones.

- **Ejemplo de uso**:
    ```bash
    GET /recomendacion/Inception
    ```

- **Respuesta**:
    ```json
    {
        "titulo": "Inception",
        "recomendaciones": [
            "Interstellar",
            "The Prestige",
            "Memento",
            "The Matrix",
            "Shutter Island"
        ]
    }
    ```