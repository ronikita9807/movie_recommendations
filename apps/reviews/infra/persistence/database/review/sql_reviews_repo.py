from pydantic import UUID4
from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from apps.reviews.core.domain.review import Review
from apps.reviews.core.ports.comands.review import ReviewPublicCommand
from apps.reviews.core.ports.requires.reviews_repo import ReviewsRepository
from apps.reviews.infra.persistence.database.review.review import ReviewRow
from apps.reviews.infra.persistence.database.review.serializer import serialize_review


class PostgreSQLReviewsRepository(ReviewsRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, review: Review) -> None:
        review_row = serialize_review(review)
        with self.session.begin():
            self.session.add(review_row)

    def update(self, review_cmd: ReviewPublicCommand) -> None:
        with self.session.begin():
            stmt = select(ReviewRow).where(
                ReviewRow.movie_id == review_cmd.movie_id,
                ReviewRow.user_id == review_cmd.user_id,
            )
            existing = self.session.execute(stmt).scalar_one_or_none()
            if not existing:
                return
            existing.text = review_cmd.text
            existing.score = review_cmd.score
            self.session.merge(existing)

    def delete_by_id(self, movie_id: UUID4, user_id: UUID4) -> None:
        stmt = delete(ReviewRow).where(
            ReviewRow.movie_id == movie_id,
            ReviewRow.user_id == user_id,
        )
        with self.session.begin():
            self.session.execute(stmt)

    def delete(self) -> None:
        stmt = delete(ReviewRow)
        with self.session.begin():
            self.session.execute(stmt)
