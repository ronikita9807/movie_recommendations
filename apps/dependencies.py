from fastapi import Depends
from sqlalchemy.orm import Session

from apps.movies.infra.persistence.database.movie.sql_movies_repo import (
    PostgreSQLMoviesRepository,
)
from apps.movies.infra.persistence.database.movie_vector.sql_movie_vectors_repo import (
    PostgreSQLMovieVectorsRepository,
)
from apps.shared.core.service.data_service import MoviesDataService
from apps.shared.core.service.movies_service import MoviesService
from apps.shared.core.service.vector_representation_service import (
    VectorRepresentationService,
)
from apps.shared.infra.persistence.database.base import get_session

from dependency_injector import containers, providers


def movies_data_service() -> MoviesDataService:
    return MoviesDataService()


def vector_representation_service() -> VectorRepresentationService:
    return VectorRepresentationService()


def movies_repo(session: Session = Depends(get_session)) -> PostgreSQLMoviesRepository:
    return PostgreSQLMoviesRepository(session=session)


def movie_vectors_repo(
    session: Session = Depends(get_session),
) -> PostgreSQLMovieVectorsRepository:
    return PostgreSQLMovieVectorsRepository(session=session)


def movies_service(
    movie_vectors_repo: PostgreSQLMovieVectorsRepository = Depends(movie_vectors_repo),
    movies_repo: PostgreSQLMoviesRepository = Depends(movies_repo),
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


class Container(containers.DeclarativeContainer):
    # Провайдер для MoviesService, создается как синглтон
    session = providers.Singleton(get_session)
    movies_repo = providers.Singleton(PostgreSQLMoviesRepository, session=session)
    movie_vectors_repo = providers.Singleton(
        PostgreSQLMovieVectorsRepository, session=session
    )
    movies_data_service = providers.Singleton(MoviesDataService)
    vector_representation_service = providers.Singleton(VectorRepresentationService)

    movies_service = providers.Singleton(
        MoviesService,
        movies_repo=movies_repo,
        movie_vectors_repo=movie_vectors_repo,
        movies_data_service=movies_data_service,
        vector_representation_service=vector_representation_service,
    )
