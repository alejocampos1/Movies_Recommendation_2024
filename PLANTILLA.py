from fastapi import FastAPI
import pandas as pd



app = FastAPI()

@app.get("/cantidad_filmaciones_mes/{mes}")
def cantidad_filmaciones_mes(mes: str) -> Dict[str, str]:
    # Aquí iría el código para contar las películas por mes en español
    # Considera convertir el mes a un formato que esté presente en el dataset
    # Por ejemplo: {'enero': 1, 'febrero': 2, ...}
    return {"mensaje": f"X cantidad de películas fueron estrenadas en el mes de {mes}"}

@app.get("/cantidad_filmaciones_dia/{dia}")
def cantidad_filmaciones_dia(dia: str) -> Dict[str, str]:
    # Aquí iría el código para contar las películas por día
    return {"mensaje": f"X cantidad de películas fueron estrenadas en los días {dia}"}

@app.get("/score_titulo/{titulo}")
def score_titulo(titulo: str) -> Dict[str, str]:
    # Aquí buscarías en el dataset el título, su año de estreno y el score
    # Ajusta esta lógica según cómo esté estructurado tu dataset
    return {"mensaje": f"La película {titulo} fue estrenada en el año X con un score/popularidad de X"}

@app.get("/votos_titulo/{titulo}")
def votos_titulo(titulo: str) -> Dict[str, str]:
    # Busca la película y verifica que tenga más de 2000 valoraciones
    # Si cumple, retorna la cantidad de votos y el promedio
    return {"mensaje": f"La película {titulo} tiene X valoraciones con un promedio de X"}

@app.get("/get_actor/{nombre_actor}")
def get_actor(nombre_actor: str) -> Dict[str, str]:
    
    return {"mensaje": f"El actor {nombre_actor} ha participado en X filmaciones con un retorno de X y promedio de X por filmación"}

@app.get("/get_director/{nombre_director}")
def get_director(nombre_director: str) -> Dict[str, str]:
    # Aquí buscarías el nombre del director y devolverías su éxito y detalles de sus películas
    return {"mensaje": f"El director {nombre_director} ha dirigido X películas. Detalles: {[]}"}

# Ejecutar la API: uvicorn nombre_del_archivo:app --reload