from pydantic import UUID4

from apps.shared.core.domain.base import BaseDTOModel


class MovieDTO(BaseDTOModel):
    release_year: int
    title: str
    origin: str
    director: str
    cast: str
    genre: str
    wiki_page: str
    plot: str


class MovieShortDTO(BaseDTOModel):
    movie_id: UUID4
    title: str
    plot: str
