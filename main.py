# Importar librerías
from fastapi import FastAPI
import pandas as pd
from typing import Dict
from sklearn.metrics.pairwise import cosine_similarity
from contextlib import asynccontextmanager

# Definir el manejador de ciclo de vida
@asynccontextmanager
async def lifespan(app: FastAPI):
    global df_cast, df_crew, df_movies, df_model, cosine_sim, df_premodel, normalizar_texto
    try:
        # Cargar los archivos Parquet
        df_model = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/matriz_features.parquet')
        df_premodel = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/pre_modelo.parquet')
        
        # Calcular la similitud de coseno
        cosine_sim = cosine_similarity(df_model)
        print("Modelo de recomendación calculado exitosamente.")
        
        # Cargar otros archivos Parquet
        df_cast = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/cast.parquet')
        df_crew = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/crew.parquet')
        df_movies = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/movies.parquet')
        print("Archivos cargados exitosamente.")

        # Definir la función normalizar_texto durante el startup
        def normalizar_texto(texto: str) -> str:
            """
            Normaliza el texto eliminando espacios en blanco y convirtiéndolo a minúsculas.
            Esto se usa para hacer comparaciones insensibles a mayúsculas y espacios.
            """
            texto_normalizado = texto.replace('-', '').replace('.', '')
            return ''.join(texto_normalizado.split()).lower()

        print("Función normalizar_texto cargada exitosamente.")
    except Exception as e:
        print(f"Error cargando archivos o modelo: {e}")
    
    # Yield para continuar la ejecución de la aplicación
    yield
    print("La aplicación se está cerrando.")

app = FastAPI(lifespan=lifespan)

# Endpoint para obtener la cantidad de filmaciones en un mes específico
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str) -> Dict[str, str]:
    """
    Devuelve la cantidad de filmaciones realizadas en un mes específico.
    Convierte el mes proporcionado en texto a su número correspondiente y cuenta las películas estrenadas ese mes.

    Args:
        mes (str): El nombre del mes en español (ej. 'enero', 'febrero').

    Returns:
        Dict[str, str]: Un mensaje con la cantidad de películas estrenadas en el mes proporcionado.
    """
    # Diccionario que mapea los nombres de los meses a sus números correspondientes
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, 
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    
    # Convertir el mes ingresado a minúsculas para evitar problemas de capitalización
    mes = mes.lower()

    # Verificar que el mes proporcionado esté en el diccionario
    if mes not in meses:
        return {"mensaje": "Ingrese un mes válido"}

    # Obtener el número de mes y contar las películas que se estrenaron en ese mes
    numero_mes = meses.get(mes)
    cantidad_peliculas = df_movies[df_movies['release_date'].dt.month == numero_mes]['release_date'].count()

    # Devolver un mensaje con el número de películas estrenadas
    return {"mensaje": f"{cantidad_peliculas} películas fueron estrenadas en el mes de {mes}"}

# Endpoint para obtener la cantidad de filmaciones en un día específico de la semana
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str) -> Dict[str, str]:
    """
    Devuelve la cantidad de filmaciones realizadas en un día específico de la semana.
    Convierte el día proporcionado en texto a su número correspondiente (0 para lunes, 6 para domingo).

    Args:
        dia (str): El nombre del día de la semana en español (ej. 'lunes', 'martes').

    Returns:
        Dict[str, str]: Un mensaje con la cantidad de películas estrenadas en el día proporcionado.
    """
    # Diccionario que mapea los días de la semana a sus números correspondientes (0 = lunes, 6 = domingo)
    dias_semana = {
        "lunes": 0,
        "martes": 1,
        "miercoles": 2,
        "miércoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sábado": 5,
        "sabado": 5,
        "domingo": 6
    }
    
    # Convertir el día ingresado a minúsculas
    dia = dia.lower()

    # Verificar que el día proporcionado esté en el diccionario
    if dia not in dias_semana:
        return {"mensaje": 'Ingrese un día de la semana válido'}

    # Obtener el número del día y contar las películas que se estrenaron ese día
    numero_dia = dias_semana.get(dia)
    cantidad_peliculas = df_movies[df_movies['release_date'].dt.dayofweek == numero_dia]['release_date'].count()

    # Devolver un mensaje con el número de películas estrenadas
    return {"mensaje": f"{cantidad_peliculas} películas fueron estrenadas un {dia}"}

# Endpoint para obtener el año de estreno y el score de una película por su título
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str) -> Dict[str, str]:
    """
    Devuelve el año de estreno y el puntaje de popularidad de una película por su título.

    Args:
        titulo (str): El título de la película.

    Returns:
        Dict[str, str]: Un mensaje con el año de estreno y el puntaje de popularidad de la película.
    """
        # Normalizar el título ingresado por el usuario
    titulo_normalizado = normalizar_texto(titulo)
    
    # Filtrar las filas donde el título normalizado coincida
    df_filtrado = df_movies[df_movies['title'].apply(normalizar_texto) == titulo_normalizado]
    
    # Verificar si se encuentra el título en el dataset
    if df_filtrado.empty:
        return {"mensaje": "Por favor, ingrese un título de película válido."}
    
    # Obtener el título original
    titulo_original = df_filtrado['title'].iloc[0]
    
    # Variables para mensaje final
    estreno = df_filtrado['release_year'].iloc[0]
    score = df_filtrado['popularity'].iloc[0]
    
    return {"mensaje": f"La película {titulo_original} fue estrenada en {estreno} con un score/popularidad de {score:.2f}"}

# Endpoint para obtener la votación total y promedio de una película por su título
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str) -> Dict[str, str]:
    """
    Devuelve la cantidad total de votos y el promedio de votos de una película por su título.

    Args:
        titulo (str): El título de la película.

    Returns:
        Dict[str, str]: Un mensaje con el número total de votos y el promedio de votaciones de la película.
    """
    # Normalizamos el título ingresado por el usuario
    titulo_normalizado = normalizar_texto(titulo)

    # Filtrar el DataFrame df_movies por los títulos que coincidan con el título normalizado
    df_filtrado = df_movies[df_movies['title'].apply(normalizar_texto) == titulo_normalizado]

    # Verificar si se encontró la película
    if not df_filtrado.empty:
        vote_total = int(df_filtrado['vote_count'].iloc[0])  # Obtener el número total de votos
        titulo_original = df_filtrado['title'].iloc[0]  # Obtener el título original
        
        # Verificar si la película tiene más de 2000 valoraciones
        if vote_total >= 2000:
            vote_average = df_filtrado['vote_average'].iloc[0]  # Obtener la votación promedio
            return {"mensaje": f"La película '{titulo_original}' tiene {vote_total} valoraciones con un promedio de {vote_average}"}
        else:
            # Si la película tiene menos de 2000 votos, devolver este mensaje
            return {"mensaje": f"El título '{titulo_original}' contiene menos de 2000 valoraciones."}
    else:
        # Si no se encuentra el título, se pide un título válido
        return {"mensaje": "Por favor, ingrese un título válido."}

# Endpoint para obtener la información de un actor y las películas en las que participó
@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str) -> Dict[str, str]:
    """
    Devuelve información sobre un actor: cuántas películas ha hecho y el retorno de esas películas.

    Args:
        nombre_actor (str): El nombre del actor.

    Returns:
        Dict[str, str]: Un mensaje con el número de películas y el retorno total y promedio de las películas en las que participó.
    """
    # Normalizar el nombre del actor
    nombre_normalizado = normalizar_texto(nombre_actor)
    
    # Filtrar los datos de actores para encontrar coincidencias con el nombre normalizado
    df_actor_filtrado = df_cast[df_cast['nombre'].apply(normalizar_texto) == nombre_normalizado]

    # Verificar si se encontró el actor
    if df_actor_filtrado.empty:
        return {"mensaje": "Por favor, ingrese un nombre de actor o actriz válido."}
    
    # Obtener el nombre original y los IDs de las películas en las que ha participado
    nombre_original = df_actor_filtrado['nombre'].iloc[0]
    peliculas_actor = df_actor_filtrado['idPelicula'].unique()
    num_peliculas = len(peliculas_actor)  # Número de películas únicas
    
    # Si no se encontraron películas, devolver este mensaje
    if num_peliculas == 0:
        return {"mensaje": f"{nombre_original} no tiene películas registradas."}
    
    # Convertir los IDs de películas a enteros (si es necesario)
    df_movies['id'] = df_movies['id'].astype(int)

    # Filtrar las películas que coincidan con los IDs del actor
    retorno_peliculas_actor = df_movies[df_movies['id'].isin(peliculas_actor)]['return']
    
    # Calcular el retorno total y el promedio de retorno por película
    total_retorno = retorno_peliculas_actor.sum()
    total_promedio = total_retorno / num_peliculas if num_peliculas > 0 else 0
    
    # Devolver un mensaje con la información del actor y sus películas
    return {
        "mensaje": f"{nombre_original} ha participado en {num_peliculas} filmaciones, "
                   f"ha conseguido un retorno total de {total_retorno:.2f} con un promedio de {total_promedio:.2f} por filmación."
    }

# Placeholder para devolver información sobre un director
@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str) -> Dict[str, str]:
    """
    Devuelve información sobre un director: retorno total de sus películas y detalles de cada una.

    Args:
        nombre_director (str): El nombre del director.

    Returns:
        Dict[str, str]: Un mensaje con el retorno total de las películas y detalles de cada una.
    """
    # Normalizar el nombre ingresado por el usuario
    nombre_normalizado = normalizar_texto(nombre_director)
    
    # Filtrar las filas donde el nombre normalizado coincida
    df_director_filtrado = df_crew[df_crew['nombre'].apply(normalizar_texto) == nombre_normalizado]
    
        # Verificar si se encontró el director antes de acceder a los datos
    if df_director_filtrado.empty:
        return {"mensaje": "Por favor, ingrese un nombre de director o directora válido."}
    
    #Filtrar el rol de dirección dentro del crew
    df_director_filtrado = df_director_filtrado[df_director_filtrado['cargo'] == 'Director']
    
    # Obtener el nombre original del director
    nombre_original = df_director_filtrado['nombre'].iloc[0]
    
    # Obtener los IDs de las películas del director y la cantidad de películas únicas
    peliculas_director = df_director_filtrado['idPelicula'].unique()
    
    # Número de películas únicas
    num_peliculas = len(peliculas_director)
    
    # Convertir df_movies['id'] a int
    df_movies['id'] = df_movies['id'].astype(int)
    
    # Filtrar las películas en df_movies usando los ids en peliculas_director
    retorno_peliculas_director = df_movies[df_movies['id'].isin(peliculas_director)]['return']

    # 1. Suma de retorno
    total_retorno = retorno_peliculas_director.sum()

    # 2. Dataframe de películas
    df_peliculas_director = df_movies[df_movies['id'].isin(peliculas_director)][['title', 'release_date', 'budget', 'revenue']]

        # Inicializar el diccionario con el mensaje base
    output_dict = {
        "mensaje": f"{nombre_original} ha conseguido un retorno total de {total_retorno:.2f}."
    }

    # Iterar sobre las filas del DataFrame para agregar información de cada película
    conteo = 1
    for index, row in df_peliculas_director.iterrows():
        
        # Formatear el mensaje de cada película
        pelicula_info = f"Título: {row['title']}, Fecha de lanzamiento: {row['release_date'].date()}, Costo: {row['budget']}, Ganancia: {row['revenue']}."
        
        # Agregar la información de la película al diccionario con una clave única
        output_dict[f'Película {conteo}'] = pelicula_info
        conteo += 1

    # Devolver el diccionario con la información calculada
    return output_dict

@app.get("/recomendacion/{titulo}")
def recomendar_peliculas(titulo: str):
    """
    Devuelve una lista de películas recomendadas basadas en un título dado utilizando similitud de coseno.

    Args:
        titulo (str): El título de la película.

    Returns:
        Dict[str, list]: Un mensaje con el título original y una lista de películas recomendadas.
    """
    # Normalizar el título ingresado por el usuario
    titulo_normalizado = normalizar_texto(titulo)
    
    # Crear un índice basado en el título normalizado de la película
    indices = pd.Series(df_premodel.index, index=df_premodel['title'].apply(normalizar_texto)).drop_duplicates()

    # Verificar si el título existe en los datos
    if titulo_normalizado not in indices:
        return {"mensaje": f"Título '{titulo}' no encontrado. Por favor, ingrese un título válido."}

    # Obtener el índice de la película que coincide con el título normalizado
    idx = indices[titulo_normalizado]

    # Traer el título original usando el índice calculado
    nombre_original = df_premodel['title'].iloc[idx]

    # Obtener los puntajes de similitud (asegurar que sea un array 1D)
    sim_scores = list(enumerate(cosine_sim[idx].flatten()))

    # Ordenar las películas con base en la similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Seleccionar las 5 películas más similares
    sim_scores = sim_scores[1:6]

    # Obtener los índices de esas películas
    movie_indices = [i[0] for i in sim_scores]

    # Asegurarse de que los índices estén dentro de los límites del DataFrame
    valid_movie_indices = [i for i in movie_indices if i < len(df_premodel)]

    # Obtener los títulos de las películas más similares
    recomendaciones = df_premodel['title'].iloc[valid_movie_indices].tolist()

    # Retornar la respuesta formateada en JSON con el título original y la lista de recomendaciones
    return {
        "titulo": nombre_original,
        "recomendaciones": recomendaciones
    }