from fastapi import FastAPI
import pandas as pd
from typing import Dict
from recomendador import recomendar_peliculas

app = FastAPI()

# Función para cargar archivos Parquet desde una URL
def load_parquet_file(file_url):
    """
    Función para cargar un archivo Parquet.
    Recibe la URL de un archivo Parquet y devuelve el DataFrame correspondiente.
    """
    return pd.read_parquet(file_url)

# Evento que se ejecuta al iniciar la API
@app.on_event("startup")
async def load_data_on_startup():
    global df_cast, df_crew, df_movies
    try:
        df_cast = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/cast.parquet')
        df_crew = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/crew.parquet')
        df_movies = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/movies.parquet')
    except Exception as e:
        print(f"Error cargando archivos: {e}")

# Función para normalizar texto eliminando espacios y convirtiendo a minúsculas
def normalizar_texto(texto: str) -> str:
    """
    Normaliza el texto eliminando espacios en blanco y convirtiéndolo a minúsculas.
    Esto se usa para hacer comparaciones insensibles a mayúsculas y espacios.
    """
    texto_normalizado = texto.replace('-', '').replace('.', '')
    return ''.join(texto_normalizado.split()).lower()

# Endpoint para obtener la cantidad de filmaciones en un mes específico
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str) -> Dict[str, str]:
    """
    Devuelve la cantidad de filmaciones realizadas en un mes específico.
    Convierte el mes proporcionado en texto a su número correspondiente y cuenta las películas estrenadas ese mes.
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
    return {"mensaje": f"{cantidad_peliculas} cantidad de películas fueron estrenadas en el mes de {mes}"}

# Endpoint para obtener la cantidad de filmaciones en un día específico de la semana
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str) -> Dict[str, str]:
    """
    Devuelve la cantidad de filmaciones realizadas en un día específico de la semana.
    Convierte el día proporcionado en texto a su número correspondiente (0 para lunes, 6 para domingo).
    """
    # Diccionario que mapea los días de la semana a sus números correspondientes (0 = lunes, 6 = domingo)
    dias_semana = {
        "lunes": 0,
        "martes": 1,
        "miércoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sábado": 5,
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
    Devuelve la cantidad de votos y el promedio de votos de una película por su título.
    Normaliza el título ingresado y busca coincidencias en los datos.
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
    Devuelve información sobre un director: retorno total de sus películas y detalles de cada una. (Fecha de lanzamiento, 
    retorno individual, costo y ganancia.)
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
def obtener_recomendaciones(titulo: str):
    """
    Endpoint para obtener recomendaciones de películas basadas en el título proporcionado.
    """
    try:
        # Obtener las recomendaciones usando la función recomendar_peliculas
        recomendaciones = recomendar_peliculas(titulo)
        return {"titulo": titulo, "recomendaciones": recomendaciones}
    except KeyError:
        return {"mensaje": "Título no encontrado. Por favor, ingrese un título válido."}
    