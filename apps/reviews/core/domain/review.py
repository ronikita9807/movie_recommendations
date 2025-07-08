from uuid import uuid4

from pydantic import UUID4, conint, Field

from apps.shared.core.domain.base import BaseDomainModel


class Review(BaseDomainModel):
    id: UUID4 = Field(default_factory=uuid4, exclude=True)
    user_id: UUID4
    movie_id: UUID4
    text: str
    score: conint(ge=1, le=10)
