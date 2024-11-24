from uuid import uuid4

from pydantic import Field, UUID4

from apps.shared.core.domain.base import BaseDomainModel


class MovieVector(BaseDomainModel):
    movie_id: UUID4 = Field(default_factory=uuid4, exclude=True)
    vector: list[float]
