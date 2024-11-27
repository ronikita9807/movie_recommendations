from typing import Protocol, Iterable
from uuid import UUID

from apps.movies.core.ports.dto.movie import MovieDTO, MovieShortDTO


class MoviesQueryService(Protocol):
    def get_movies_by_ids(self, movie_ids: list[UUID]) -> list[MovieDTO]: ...

    def get_all_movies(self, batch_size: int) -> Iterable[MovieShortDTO]: ...

    def find_by_name(self, name: str) -> list[MovieDTO]: ...
