from apps.movies.infra.persistence.database.movie.sql_movies_repo import (
    PostgreSQLMoviesRepository,
)
from apps.movies.infra.persistence.database.movie_vector.sql_movie_vectors_repo import (
    PostgreSQLMovieVectorsRepository,
)
from apps.movies.infra.queries.sql_movie_vectors_query_service import (
    PostgreSQLMovieVectorsQueryService,
)
from apps.movies.infra.queries.sql_movies_query_service import (
    PostgreSQLMoviesQueryService,
)
from apps.shared.core.service.data_service import MoviesDataService
from apps.shared.core.service.movie_vectors_generation_service import (
    MovieVectorsGenerationService,
)
from apps.shared.core.service.movies_save_service import MoviesSaveService
from apps.shared.core.service.search_movie_by_description_service import (
    SearchMovieByDescriptionService,
)
from apps.shared.core.service.vector_representation_service import (
    VectorRepresentationService,
)
from apps.shared.infra.persistence.database.base import get_session

from dependency_injector import containers, providers


class Container(containers.DeclarativeContainer):
    session = providers.Singleton(get_session)

    movies_repo = providers.Singleton(PostgreSQLMoviesRepository, session=session)
    movie_vectors_repo = providers.Singleton(
        PostgreSQLMovieVectorsRepository, session=session
    )

    movie_vectors_query_service = providers.Singleton(
        PostgreSQLMovieVectorsQueryService, session=session
    )
    movies_query_service = providers.Singleton(
        PostgreSQLMoviesQueryService, session=session
    )

    movies_data_service = providers.Singleton(MoviesDataService)
    vector_representation_service = providers.Singleton(VectorRepresentationService)

    movies_save_service = providers.Singleton(
        MoviesSaveService,
        movies_repo=movies_repo,
        movies_data_service=movies_data_service,
    )
    movie_vectors_generation_service = providers.Singleton(
        MovieVectorsGenerationService,
        movies_query_service=movies_query_service,
        movie_vectors_repo=movie_vectors_repo,
        vector_representation_service=vector_representation_service,
    )
    search_movie_by_description_service = providers.Singleton(
        SearchMovieByDescriptionService,
        vector_representation_service=vector_representation_service,
        movie_vectors_query_service=movie_vectors_query_service,
        movies_query_service=movies_query_service,
    )
