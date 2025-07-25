from typing import Protocol

from pydantic import UUID4

from apps.reviews.core.domain.review import Review
from apps.reviews.core.ports.comands.review import ReviewPublicCommand


class ReviewsRepository(Protocol):
    def save(self, review: Review) -> None:
        ...

    def update(self, review: ReviewPublicCommand) -> None:
        ...

    def delete_by_id(self, movie_id: UUID4, user_id: UUID4) -> None:
        ...

    def delete(self):
        ...
