from pathlib import Path
from uuid import UUID


from apps.movies.core.domain.movie_vector import MovieVector
from apps.movies.core.ports.dto.movie import MovieDTO
from apps.movies.infra.persistence.database.movie.sql_movies_repo import (
    PostgreSQLMovieRepository,
)

from apps.movies.infra.persistence.database.movie_vector.sql_movie_vectors_repo import (
    PostgreSQLMovieVectorRepository,
)
from apps.shared.core.service.data_service import MoviesDataService
from apps.shared.core.service.vector_representation_service import (
    VectorRepresentationService,
)

DATA_DIR = Path(__file__).resolve().parent


class MoviesService:
    def __init__(
        self,
        movie_vectors_repo: PostgreSQLMovieVectorRepository,
        movies_repo: PostgreSQLMovieRepository,
        movies_data_service: MoviesDataService,
        vector_representation_service: VectorRepresentationService,
    ):
        self._movies_data_service = movies_data_service
        self._movies_repo = movies_repo
        self._movie_vectors_repo = movie_vectors_repo
        self._vector_representation_service = vector_representation_service

    # добавить поиск по описанию используя векторизацию полученного текста а затем поиск наиболее близкого вектора по значению используя ленивые извлечения объектов из базы
    # @transactional
    def find_movie_by_description(self, description: str) -> MovieDTO | None:
        a = self._movie_vectors_repo.get_by_id(
            UUID("33caff11-437e-45ea-9170-703ca6b4358b")
        )
        return a

    # @transactional
    def find_by_name(self, name: str) -> list[MovieDTO]:
        return self._movies_repo.find_by_name(name)

    # @transactional
    def create_vectorized_representation(self) -> None:
        # доставать объекты лениво
        for movie in self._movies_repo.get_all_movies():
            vector = self._vector_representation_service.get_representation(movie.plot)
            movie_vector = MovieVector(
                movie_id=movie.movie_id,
                vector=vector,
            )
            self._movie_vectors_repo.save(movie_vector)

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
