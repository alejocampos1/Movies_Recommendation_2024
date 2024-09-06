from fastapi import FastAPI
import pandas as pd

app = FastAPI()

@app.on_event("startup")
async def load_data_on_startup():
    global df_cast, df_collections, df_crew, df_genres, df_movies, df_prodcompanies, df_prodcountries
    try:
        df_cast = pd.read_csv("https://raw.githubusercontent.com/alejocampos1/Henry_PI1_Alejandro-Campos/main/Datasets/Datasets_Limpios/cast.csv")
        df_collections = pd.read_csv("https://raw.githubusercontent.com/alejocampos1/Henry_PI1_Alejandro-Campos/main/Datasets/Datasets_Limpios/collections.csv")
        df_crew = pd.read_csv("https://raw.githubusercontent.com/alejocampos1/Henry_PI1_Alejandro-Campos/main/Datasets/Datasets_Limpios/crew.csv")
        df_genres = pd.read_csv("https://raw.githubusercontent.com/alejocampos1/Henry_PI1_Alejandro-Campos/main/Datasets/Datasets_Limpios/genres.csv")
        df_movies = pd.read_csv("https://raw.githubusercontent.com/alejocampos1/Henry_PI1_Alejandro-Campos/main/Datasets/Datasets_Limpios/movies.csv")
        df_prodcompanies = pd.read_csv("https://raw.githubusercontent.com/alejocampos1/Henry_PI1_Alejandro-Campos/main/Datasets/Datasets_Limpios/prodcompanies.csv")
        df_prodcountries = pd.read_csv("https://raw.githubusercontent.com/alejocampos1/Henry_PI1_Alejandro-Campos/main/Datasets/Datasets_Limpios/prodcountries.csv")
        
        print("Todos los CSV se han cargado correctamente.")
    except Exception as e:
        print(f"Error al cargar los CSV: {str(e)}");