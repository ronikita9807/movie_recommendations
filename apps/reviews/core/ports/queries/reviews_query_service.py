from typing import Protocol

from apps.reviews.core.domain.review import Review
from apps.reviews.core.ports.dto.review import ReviewDTO


class ReviewsQueryService(Protocol):
    def find_by_user_name(self, name: str) -> list[ReviewDTO]:
        ...
