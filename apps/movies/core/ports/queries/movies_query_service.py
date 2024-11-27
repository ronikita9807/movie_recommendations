from typing import Protocol
from uuid import UUID

from apps.movies.core.ports.dto.movie import MovieDTO


class MoviesQueryService(Protocol):
    def get_movies_by_ids(self, movie_ids: list[UUID]) -> list[MovieDTO]: ...

    def find_by_name(self, name: str) -> list[MovieDTO]: ...
