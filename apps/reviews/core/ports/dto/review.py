from pydantic import UUID4

from apps.shared.core.domain.base import BaseDTOModel


class ReviewDTO(BaseDTOModel):
    user_name: str
    movie_name: str
    text: str
    score: int
