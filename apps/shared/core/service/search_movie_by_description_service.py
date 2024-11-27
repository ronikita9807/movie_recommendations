from pathlib import Path


from apps.movies.core.ports.dto.movie import MovieDTO
from apps.movies.core.ports.queries.movie_vectors_query_service import (
    MovieVectorsQueryService,
)
from apps.movies.core.ports.queries.movies_query_service import MoviesQueryService

from apps.shared.core.service.vector_representation_service import (
    VectorRepresentationService,
)

DATA_DIR = Path(__file__).resolve().parent


class SearchMovieByDescriptionService:
    def __init__(
        self,
        vector_representation_service: VectorRepresentationService,
        movie_vectors_query_service: MovieVectorsQueryService,
        movies_query_service: MoviesQueryService,
    ):
        self._vector_representation_service = vector_representation_service
        self._movie_vectors_query_service = movie_vectors_query_service
        self._movies_query_service = movies_query_service

    def find_movies_by_description(self, description: str) -> list[MovieDTO]:
        vector = self._vector_representation_service.get_representation(description)
        movie_ids = self._movie_vectors_query_service.get_movies_by_embeddings(
            vector=vector, limit=10
        )
        return self._movies_query_service.get_movies_by_ids(movie_ids)
