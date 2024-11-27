from typing import Optional, Iterable, Protocol
from uuid import UUID


from apps.movies.core.domain.movie import Movie


class MoviesRepository(Protocol):
    def get_by_id(self, movie_id: UUID) -> Optional[Movie]: ...

    def get_all_movies(self, batch_size: int) -> Iterable[Movie]: ...

    def save(self, movies: list[Movie]) -> None: ...

    def delete(self): ...
