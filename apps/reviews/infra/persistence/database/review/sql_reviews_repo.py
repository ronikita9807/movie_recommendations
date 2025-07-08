from sqlalchemy.orm import Session

from apps.reviews.core.domain.review import Review
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

    def delete(self):
        self.session.query(ReviewRow).delete()
        self.session.commit()
