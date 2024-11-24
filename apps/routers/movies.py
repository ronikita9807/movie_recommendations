from fastapi import Depends, APIRouter
from fastapi.openapi.docs import get_swagger_ui_html
from apps.shared.core.service.movies_service import MoviesService
from apps.dependencies import movies_service


router = APIRouter()


@router.get("/ui", include_in_schema=False)
def custom_swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI")


@router.post("/update-movies")
def update_movies(movies_service: MoviesService = Depends(movies_service)):
    movies_service.update_movies()
    return {"message": "Movies saved successfully"}


@router.post("/update-movies-vectors")
def update_movies_vectors(movies_service: MoviesService = Depends(movies_service)):
    movies_service.create_vectorized_representation()
    return {"message": "Movies vectors saved successfully"}


@router.delete("/movies")
def delete_movies(movies_service: MoviesService = Depends(movies_service)):
    movies_service.delete_movies()
    return {"message": "Movies deleted successfully"}


@router.delete("/movies-vectors")
def delete_movies(movies_service: MoviesService = Depends(movies_service)):
    movies_service.delete_movies_vectors()
    return {"message": "Movies vectors deleted successfully"}


@router.get("/movies/by_name/{name}")
def find_by_name(name: str, movies_service: MoviesService = Depends(movies_service)):
    return movies_service.find_by_name(name=name)


@router.get("/movies/by_desription/{description}")
def find_by_desription(
    description: str, movies_service: MoviesService = Depends(movies_service)
):
    return movies_service.find_movie_by_description(description=description)
