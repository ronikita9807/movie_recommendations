from pydantic import UUID4
from sqlalchemy import and_
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
        self.session.add(review_row)
        self.session.commit()

    def update(self, review: ReviewPublicCommand) -> None:
        old_review = (
            self.session.query(ReviewRow)
            .filter(
                ReviewRow.movie_id == review.movie_id,
                ReviewRow.user_id == review.user_id,
            )
            .one_or_none()
        )

        if old_review:
            old_review.text = review.text
            old_review.score = review.score
            self.session.merge(old_review)
            self.session.commit()

    def delete_by_id(self, movie_id: UUID4, user_id: UUID4) -> None:
        self.session.query(ReviewRow).filter(
            ReviewRow.movie_id == movie_id, ReviewRow.user_id == user_id
        ).delete()
        self.session.commit()

    def delete(self):
        self.session.query(ReviewRow).delete()
        self.session.commit()
