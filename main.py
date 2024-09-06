from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.on_event("startup")
async def load_data_on_startup():
    global df_cast, df_collections, df_crew, df_genres, df_movies, df_prodcompanies, df_prodcountries
    try:
        df_cast = pd.read_csv("/ruta/a/cast.csv")
        df_collections = pd.read_csv("/ruta/a/collections.csv")
        df_crew = pd.read_csv("/ruta/a/crew.csv")
        df_genres = pd.read_csv("/ruta/a/genres.csv")
        df_movies = pd.read_csv("/ruta/a/movies.csv")
        df_prodcompanies = pd.read_csv("/ruta/a/prodcompanies.csv")
        df_prodcountries = pd.read_csv("/ruta/a/prodcountries.csv")
        
        print("Todos los CSV se han cargado correctamente.")
    except Exception as e:
        print(f"Error al cargar los CSV: {str(e)}");