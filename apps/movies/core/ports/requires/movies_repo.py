from typing import Optional, Iterable, Protocol
from uuid import UUID


from apps.movies.core.domain.movie import Movie
from apps.movies.core.ports.dto.movie import MovieDTO


class MoviesRepository(Protocol):
    def get_by_id(self, movie_id: UUID) -> Optional[Movie]: ...

    def get_row_movies_by_ids(self, movie_ids: list[UUID]) -> list[MovieDTO]: ...

    def get_all_movies(self, batch_size=100) -> Iterable[Movie]: ...

    def find_by_name(self, name: str) -> list[MovieDTO]: ...

    def save(self, movies: list[Movie]) -> None: ...

    def delete(self): ...
