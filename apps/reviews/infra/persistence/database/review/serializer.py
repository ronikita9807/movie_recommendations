from apps.reviews.core.domain.review import Review
from apps.reviews.infra.persistence.database.review.review import ReviewRow


def serialize_review(review: Review) -> ReviewRow:
    return ReviewRow(
        id=review.id,
        user_id=review.user_id,
        movie_id=review.movie_id,
        text=review.text,
        score=review.score,
    )
