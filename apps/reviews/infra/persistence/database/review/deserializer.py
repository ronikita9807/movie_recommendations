from apps.reviews.core.domain.review import Review
from apps.reviews.infra.persistence.database.review.review import ReviewRow


def deserialize_review(review_row: ReviewRow) -> Review:
    return Review(
        id=review_row.id,
        user_id=review_row.user_id,
        movie_id=review_row.movie_id,
        text=review_row.text,
        score=review_row.score,
    )
