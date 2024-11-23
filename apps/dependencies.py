from fastapi import Depends
from sqlalchemy.orm import Session

from apps.movies.infra.persistence.database.movie.sql_movies_repo import PostgreSQLMovieRepository
from apps.movies.infra.persistence.database.movie_vector.sql_movie_vectors_repo import PostgreSQLMovieVectorRepository
from apps.shared.core.service.data_service import MoviesDataService
from apps.shared.core.service.movies_service import MoviesService
from apps.shared.core.service.vector_representation_service import (
    VectorRepresentationService,
)
from apps.shared.infra.persistence.database.base import get_session


def movies_data_service() -> MoviesDataService:
    return MoviesDataService()


def vector_representation_service() -> VectorRepresentationService:
    return VectorRepresentationService()


def movies_repo(session: Session = Depends(get_session)) -> PostgreSQLMovieRepository:
    return PostgreSQLMovieRepository(session=session)


def movie_vectors_repo(session: Session = Depends(get_session)) -> PostgreSQLMovieVectorRepository:
    return PostgreSQLMovieVectorRepository(session=session)


def movies_service(
    movie_vectors_repo: PostgreSQLMovieVectorRepository = Depends(movie_vectors_repo),
    movies_repo: PostgreSQLMovieRepository = Depends(movies_repo),
    movies_data_service: MoviesDataService = Depends(movies_data_service),
    vector_representation_service: VectorRepresentationService = Depends(
        vector_representation_service
    ),
) -> MoviesService:
    return MoviesService(
        movies_repo=movies_repo,
        movie_vectors_repo=movie_vectors_repo,
        movies_data_service=movies_data_service,
        vector_representation_service=vector_representation_service,
    )