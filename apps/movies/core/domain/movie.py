from uuid import uuid4

from pydantic import Field, UUID4

from apps.shared.core.domain.base import BaseDomainModel


class Movie(BaseDomainModel):
    movie_id: UUID4 = Field(default_factory=uuid4, exclude=True)
    release_year: int
    title: str
    origin: str
    director: str
    cast: str
    genre: str
    wiki_page: str
    plot: str
