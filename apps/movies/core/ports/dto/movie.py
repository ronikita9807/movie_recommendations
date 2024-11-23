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
