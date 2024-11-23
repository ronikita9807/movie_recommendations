# app/main.py

from fastapi import FastAPI
from apps.routers import movies

app = FastAPI()

app.include_router(movies.router)