from pathlib import Path


from apps.movies.core.domain.movie_vector import MovieVector
from apps.movies.core.ports.dto.movie import MovieDTO
from apps.movies.core.ports.requires.movie_vectors_repo import MovieVectorsRepository
from apps.movies.core.ports.requires.movies_repo import MoviesRepository

from apps.shared.core.service.data_service import MoviesDataService
from apps.shared.core.service.vector_representation_service import (
    VectorRepresentationService,
)

DATA_DIR = Path(__file__).resolve().parent


class MoviesService:
    def __init__(
        self,
        movie_vectors_repo: MovieVectorsRepository,
        movies_repo: MoviesRepository,
        movies_data_service: MoviesDataService,
        vector_representation_service: VectorRepresentationService,
    ):
        self._movies_data_service = movies_data_service
        self._movies_repo = movies_repo
        self._movie_vectors_repo = movie_vectors_repo
        self._vector_representation_service = vector_representation_service

    # @transactional
    def find_movies_by_description(self, description: str) -> list[MovieDTO]:
        vector = self._vector_representation_service.get_representation(description)
        movie_ids = self._movie_vectors_repo.get_movies_by_embeddings(vector)
        return self._movies_repo.get_row_movies_by_ids(movie_ids)

    # @transactional
    def find_by_name(self, name: str) -> list[MovieDTO]:
        return self._movies_repo.find_by_name(name)

    # @transactional
    def create_vectorized_representation(self) -> None:
        batch_size = 100
        batch = []
        for movie in self._movies_repo.get_all_movies():
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

    # @transactional
    def update_movies(self) -> None:
        movies = self._movies_data_service.get_movies_data()
        self._movies_repo.save(movies)

    # @transactional
    def delete_movies(self) -> None:
        return self._movies_repo.delete()

    # @transactional
    def delete_movies_vectors(self) -> None:
        return self._movie_vectors_repo.delete()
