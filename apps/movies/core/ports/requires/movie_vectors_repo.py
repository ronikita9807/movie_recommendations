from typing import Optional, Protocol
from uuid import UUID

from apps.movies.core.domain.movie_vector import MovieVector


class MovieVectorsRepository(Protocol):
    def get_by_id(self, movie_id: UUID) -> Optional[MovieVector]: ...

    def get_movies_by_embeddings(
        self, vector: list[float], limit: int
    ) -> list[UUID]: ...

    def save(self, movie_vectors: list[MovieVector]) -> None: ...

    def delete(self): ...
