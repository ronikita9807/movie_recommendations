from typing import Protocol

from apps.reviews.core.domain.review import Review


class ReviewsRepository(Protocol):
    def save(self, review: Review) -> None:
        ...

    def delete(self):
        ...
