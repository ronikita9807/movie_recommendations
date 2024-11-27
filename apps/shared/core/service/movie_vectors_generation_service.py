from pathlib import Path


from apps.movies.core.domain.movie_vector import MovieVector
from apps.movies.core.ports.queries.movies_query_service import MoviesQueryService
from apps.movies.core.ports.requires.movie_vectors_repo import MovieVectorsRepository
from apps.movies.core.ports.requires.movies_repo import MoviesRepository

from apps.shared.core.service.vector_representation_service import (
    VectorRepresentationService,
)

DATA_DIR = Path(__file__).resolve().parent


class MovieVectorsGenerationService:
    def __init__(
        self,
        movie_vectors_repo: MovieVectorsRepository,
        movies_query_service: MoviesQueryService,
        vector_representation_service: VectorRepresentationService,
    ):
        self._movies_query_service = movies_query_service
        self._movie_vectors_repo = movie_vectors_repo
        self._vector_representation_service = vector_representation_service

    def create_vectorized_representation(self) -> None:
        batch_size = 100
        batch = []
        for movie in self._movies_query_service.get_all_movies(batch_size=100):
            vector = self._vector_representation_service.get_representation(movie.plot)
            batch.append(
                MovieVector(
                    movie_id=movie.movie_id,
                    vector=vector,
                )
            )
            if len(batch) >= batch_size:
                self._save_and_clear_batch(batch)

        if batch:
            self._save_and_clear_batch(batch)

    def _save_and_clear_batch(self, batch: list[MovieVector]) -> None:
        self._movie_vectors_repo.save(batch)
        batch.clear()

    def delete_movies_vectors(self) -> None:
        return self._movie_vectors_repo.delete()
