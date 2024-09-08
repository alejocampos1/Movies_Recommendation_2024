from fastapi import FastAPI
import pandas as pd
from typing import Dict
from concurrent.futures import ThreadPoolExecutor

app = FastAPI()

def load_parquet_file(file_url):
    """Función para cargar un archivo Parquet."""
    return pd.read_parquet(file_url)

@app.on_event("startup")
async def load_data_on_startup():
    global df_cast, df_collections, df_crew, df_genres, df_movies, df_prodcompanies, df_prodcountries
    try:
        # URLs de los archivos Parquet
        file_urls = {
            "df_cast": "https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/cast.parquet",
            "df_collections": "https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/collections.parquet",
            "df_crew": "https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/crew.parquet",
            "df_genres": "https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/genres.parquet",
            "df_movies": "https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/movies.parquet",
            "df_prodcompanies": "https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/prodcompanies.parquet",
            "df_prodcountries": "https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/Datasets_Limpios/Parquet/prodcountries.parquet"
        }

        # Usar ThreadPoolExecutor para cargar archivos en paralelo
        with ThreadPoolExecutor(max_workers=8) as executor:
            future_to_df = {executor.submit(load_parquet_file, url): df_name for df_name, url in file_urls.items()}

            # Asignar el resultado de cada carga a su respectiva variable global
            for future in future_to_df:
                df_name = future_to_df[future]
                globals()[df_name] = future.result()

        print("Todos los archivos se han cargado correctamente.")

    except Exception as e:
        print(f"Error al cargar los archivos Parquet: {str(e)}")

# Función auxiliar para normalizar texto
def normalizar_texto(texto: str) -> str:
    return ''.join(texto.split()).lower()

# Endpoint para obtener la cantidad de filmaciones en un mes
@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str) -> Dict[str, str]:
    meses = {
        "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6, 
        "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12
    }
    mes = mes.lower()
    if mes not in meses:
        return {"mensaje": "Ingrese un mes válido"}
    numero_mes = meses.get(mes)
    cantidad_peliculas = df_movies[df_movies['release_date'].dt.month == numero_mes]['release_date'].count()

    return {"mensaje": f"{cantidad_peliculas} cantidad de películas fueron estrenadas en el mes de {mes}"}

# Endpoint para obtener la cantidad de filmaciones en un día específico
@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str) -> Dict[str, str]:
    dias_semana = {
        "lunes": 0,
        "martes": 1,
        "miércoles": 2,
        "jueves": 3,
        "viernes": 4,
        "sábado": 5,
        "domingo": 6
    }
    
    dia = dia.lower()
    if dia not in dias_semana:
        return {"mensaje": 'Ingrese un día de la semana válido'}
    numero_dia = dias_semana.get(dia)
    cantidad_peliculas = df_movies[df_movies['release_date'].dt.dayofweek == numero_dia]['release_date'].count()

    return {"mensaje": f"{cantidad_peliculas} películas fueron estrenadas un {dia}"}

# Otros endpoints placeholder (puedes completarlos con tu lógica)
@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str) -> Dict[str, str]:
    return {"mensaje": f"La película {titulo} fue estrenada en el año X con un score/popularidad de X"}

# Endpoint para obtener la votación total y promedio de una película por su título
@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str) -> Dict[str, str]:
    titulo_normalizado = normalizar_texto(titulo)
    df_filtrado = df_movies[df_movies['title'].apply(normalizar_texto) == titulo_normalizado]

    if not df_filtrado.empty:
        vote_total = int(df_filtrado['vote_count'].iloc[0])
        titulo_original = df_filtrado['title'].iloc[0]
        
        if vote_total >= 2000:
            vote_average = df_filtrado['vote_average'].iloc[0]
            return {"mensaje": f"La película '{titulo_original}' tiene {vote_total} valoraciones con un promedio de {vote_average}"}
        else:
            return {"mensaje": f"El título '{titulo_original}' contiene menos de 2000 valoraciones."}
    else:
        return {"mensaje": "Por favor, ingrese un título válido."}

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str) -> Dict[str, str]:
    # Normalizar el nombre ingresado por el usuario
    nombre_normalizado = normalizar_texto(nombre_actor)
    
    # Filtrar las filas donde el nombre normalizado coincida
    df_actor_filtrado = df_cast[df_cast['nombre'].apply(normalizar_texto) == nombre_normalizado]

    # Verificar si se encontró el actor antes de acceder a los datos
    if df_actor_filtrado.empty:
        return {"mensaje": "Por favor, ingrese un nombre de actor o actriz válido."}
    
    # Obtener el nombre original del actor
    nombre_original = df_actor_filtrado['nombre'].iloc[0]
    
    # Obtener los IDs de las películas del actor y la cantidad de películas únicas
    peliculas_actor = df_actor_filtrado['idPelicula'].unique()
    
    # Número de películas únicas
    num_peliculas = len(peliculas_actor)
    
    if num_peliculas == 0:
        return {"mensaje": f"{nombre_original} no tiene películas registradas."}
    
    # Convertir df_movies['id'] a int
    df_movies['id'] = df_movies['id'].astype(int)
    
    # Filtrar las películas en df_movies usando los ids en peliculas_actor
    retorno_peliculas_actor = df_movies[df_movies['id'].isin(peliculas_actor)]['return']
    
    # Calcular el total de retorno
    total_retorno = retorno_peliculas_actor.sum()
    
    # Calcular el promedio de retorno por película
    total_promedio = total_retorno / num_peliculas if num_peliculas > 0 else 0
    
    # Devolver el mensaje con la información calculada
    return {
        "mensaje": f"{nombre_original} ha participado en {num_peliculas} filmaciones, "
                   f"ha conseguido un retorno total de {total_retorno:.2f} con un promedio de {total_promedio:.2f} por filmación."
    }
    

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str) -> Dict[str, str]:
    return {"mensaje": f"El director {nombre_director} ha dirigido X películas. Detalles: {[]}"}