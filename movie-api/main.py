from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class Movie(BaseModel):
    title: str
    director: str
    year: int

movies_db: List[Movie] = []

@app.get("/")
def root():
    return {"message": "API do zarządzania filmami działa"}

@app.post("/movies/")
def add_movie(movie: Movie):
    movies_db.append(movie)
    return {"message": "Film dodany", "movie": movie}

@app.get("/movies/")
def list_movies():
    return movies_db

@app.get("/movies/director/{director_name}")
def get_movies_by_director(director_name: str):
    result = [m for m in movies_db if m.director.lower() == director_name.lower()]
    if not result:
        raise HTTPException(status_code=404, detail="Nie znaleziono filmów tego reżysera")
    return result

