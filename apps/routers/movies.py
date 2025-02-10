from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, Path, HTTPException
from sqlalchemy.exc import IntegrityError

from apps.dependencies import Container
from apps.movies.core.ports.queries.movies_query_service import MoviesQueryService
from apps.movies.core.service.movie_vectors_generation_service import (
    MovieVectorsGenerationService,
)
from apps.movies.core.service.movies_save_service import MoviesSaveService
from apps.movies.core.service.search_movie_by_description_service import (
    SearchMovieByDescriptionService,
)

router = APIRouter()


@router.post("/update-movies")
@inject
def update_movies(
    movies_save_service: MoviesSaveService = Depends(
        Provide[Container.movies_save_service]
    ),
):
    movies_save_service.update_movies()
    return {"message": "Movies saved successfully"}


@router.post("/update-movies-vectors")
@inject
def update_movies_vectors(
    movie_vectors_generation_service: MovieVectorsGenerationService = Depends(
        Provide[Container.movie_vectors_generation_service]
    ),
):
    try:
        movie_vectors_generation_service.create_vectorized_representation()
        return {"message": "Movies vectors saved successfully"}
    except IntegrityError as e:
        raise HTTPException(status_code=404, detail=f"Duplicate key error: {e.orig}")


@router.delete("/movies")
@inject
def delete_movies(
    movies_save_service: MoviesSaveService = Depends(
        Provide[Container.movies_save_service]
    ),
):
    movies_save_service.delete_movies()
    return {"message": "Movies deleted successfully"}


@router.delete("/movies-vectors")
@inject
def delete_movie_vectors(
    movie_vectors_generation_service: MovieVectorsGenerationService = Depends(
        Provide[Container.movie_vectors_generation_service]
    ),
):
    movie_vectors_generation_service.delete_movies_vectors()
    return {"message": "Movies vectors deleted successfully"}


@router.get("/movies/by_name/{name}")
@inject
def find_by_name(
    name: str = Path(..., title="Film name", example="Harry Potter"),
    movies_query_service: MoviesQueryService = Depends(
        Provide[Container.movies_query_service]
    ),
):
    return movies_query_service.find_by_name(name=name)


@router.get("/movies/by_desription/{description}")
@inject
def find_by_desription(
    description: str = Path(
        ..., title="Film description", example="Jack trying to save Rose from ship"
    ),
    search_movie_by_description_service: SearchMovieByDescriptionService = Depends(
        Provide[Container.search_movie_by_description_service]
    ),
):
    return search_movie_by_description_service.find_movies_by_description(
        description=description
    )
