import psutil
import os
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd

# Obtener el proceso actual
process = psutil.Process(os.getpid())

# Cargar el DataFrame df_modelo
df_modelo = pd.read_parquet('/Users/alejocampos/Library/Mobile Documents/com~apple~CloudDocs/SOYHENRY/LABS/PI1_FASTAPI/Datasets/matriz_features2.parquet')

# Medir la memoria antes del cálculo de la similitud
mem_before = process.memory_info().rss / (1024 ** 2)  # Convertir a MB
print(f"Memoria antes del cálculo de la similitud: {mem_before:.2f} MB")

# Calcular la similitud de coseno
cosine_sim = cosine_similarity(df_modelo)

# Medir la memoria después del cálculo
mem_after = process.memory_info().rss / (1024 ** 2)  # Convertir a MB
print(f"Memoria después del cálculo de la similitud: {mem_after:.2f} MB")

# Diferencia en el uso de memoria
print(f"Memoria utilizada por el cálculo de cosine_similarity: {mem_after - mem_before:.2f} MB")
