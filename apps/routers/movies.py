from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, Path, HTTPException
from fastapi.openapi.docs import get_swagger_ui_html
from sqlalchemy.exc import IntegrityError

from apps.dependencies import Container
from apps.movies.core.ports.queries.movies_query_service import MoviesQueryService
from apps.shared.core.service.movie_vectors_generation_service import (
    MovieVectorsGenerationService,
)
from apps.shared.core.service.movies_save_service import MoviesSaveService
from apps.shared.core.service.search_movie_by_description_service import (
    SearchMovieByDescriptionService,
)

container = Container()
router = APIRouter()


@router.get("/ui", include_in_schema=False)
@inject
def custom_swagger_ui():
    return get_swagger_ui_html(openapi_url="/openapi.json", title="Custom Swagger UI")


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


@router.on_event("startup")
async def startup_event():
    container.wire(modules=[__name__])


@router.on_event("shutdown")
async def shutdown_event():
    container.unwire()
