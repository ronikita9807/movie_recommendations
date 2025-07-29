from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.reviews.core.domain.review import Review
from apps.reviews.core.ports.dto.review import ReviewDTO
from apps.reviews.core.ports.queries.reviews_query_service import ReviewsQueryService
from apps.reviews.infra.persistence.database.review.review import ReviewRow
from apps.reviews.infra.persistence.database.review.deserializer import (
    deserialize_review,
)
from apps.users.infra.persistence.database.user.user import UserRow


class PostgreSQLReviewsQueryService(ReviewsQueryService):
    def __init__(self, session: Session):
        self.session = session

    def find_by_user_name(self, name: str) -> list[ReviewDTO]:
        stmt = (
            select(ReviewRow)
            .join(ReviewRow.user)
            .where(UserRow.user_name == name)
        )
        with self.session.begin():
            results = self.session.execute(stmt).scalars().all()
        return [self._deserialize_review(review) for review in results]

    @staticmethod
    def _deserialize_review(review: ReviewRow) -> ReviewDTO:
        return ReviewDTO(
            user_name=review.user.user_name,
            movie_name=review.movie.title,
            text=review.text,
            score=review.score,
        )
