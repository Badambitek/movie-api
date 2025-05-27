from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

# Model filmu
class Movie(BaseModel):
    id: int
    title: str
    director: str
    year: int

# Pseudo-baza danych (lista filmów)
movies_db: List[Movie] = []

# Endpoint powitalny
@app.get("/")
def read_root():
    return {"message": "API do zarządzania filmami działa"}

# Endpoint do pobrania wszystkich filmów
@app.get("/movies", response_model=List[Movie])
def get_movies():
    return movies_db

# Endpoint do dodania nowego filmu
@app.post("/movies", response_model=Movie)
def add_movie(movie: Movie):
    for m in movies_db:
        if m.id == movie.id:
            raise HTTPException(status_code=400, detail="Film o takim ID już istnieje.")
    movies_db.append(movie)
    return movie

# Endpoint do pobrania filmu po ID
@app.get("/movies/{movie_id}", response_model=Movie)
def get_movie(movie_id: int):
    for movie in movies_db:
        if movie.id == movie_id:
            return movie
    raise HTTPException(status_code=404, detail="Film nie znaleziony")

# Endpoint do usunięcia filmu
@app.delete("/movies/{movie_id}")
def delete_movie(movie_id: int):
    global movies_db
    movies_db = [m for m in movies_db if m.id != movie_id]
    return {"message": "Film usunięty"}
