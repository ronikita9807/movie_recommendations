# app/main.py

from fastapi import FastAPI

from apps.routers import movies, base, users

app = FastAPI()

app.include_router(base.router)
app.include_router(movies.router, tags=["movies"])
app.include_router(users.router, tags=["users"])
