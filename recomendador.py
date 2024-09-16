# recomendador.py

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
import joblib

# Cargar datos de las películas y las características
df_model = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/matriz_features.parquet')
df_premodel = pd.read_parquet('https://github.com/alejocampos1/Henry_PI1_Alejandro-Campos/raw/main/Datasets/pre_modelo.parquet')

# Calcular la similitud de coseno
cosine_sim = cosine_similarity(df_model)

# Guardar el modelo de similitud coseno en un archivo .pkl
joblib.dump((cosine_sim, df_premodel), 'modelo_recomendacion.pkl', compress=9)

def recomendar_peliculas(titulo):
    # Crear un índice basado en el título de la película
    indices = pd.Series(df_premodel.index, index=df_premodel['title']).drop_duplicates()

    # Obtener el índice de la película que coincide con el título
    idx = indices[titulo]

    # Obtener los puntajes de similitud
    sim_scores = list(enumerate(cosine_sim[idx]))

    # Ordenar las películas en base a la similitud
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # Seleccionar las 5 películas más similares
    sim_scores = sim_scores[1:6]

    # Obtener los índices de esas películas
    movie_indices = [i[0] for i in sim_scores]

    # Retornar los títulos de las películas más similares
    return df_premodel['title'].iloc[movie_indices]
