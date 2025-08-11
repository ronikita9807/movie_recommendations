from apps.reviews.core.domain.review import Review
from apps.reviews.core.ports.comands.review import ReviewPublicCommand
from apps.reviews.core.ports.comands.review_delete_command import (
    ReviewDeletePublicCommand,
)
from apps.reviews.core.ports.requires.reviews_repo import ReviewsRepository


class ReviewsCreationService:
    def __init__(
        self,
        reviews_repo: ReviewsRepository,
    ):
        self._reviews_repo = reviews_repo

    def create_review(self, command: ReviewPublicCommand) -> None:
        review = Review(
            user_id=command.user_id,
            movie_id=command.movie_id,
            text=command.text,
            score=command.score,
        )
        self._reviews_repo.save(review)

    def update_review(self, command: ReviewPublicCommand) -> None:
        self._reviews_repo.update(command)

    def delete_review(self, command: ReviewDeletePublicCommand) -> None:
        self._reviews_repo.delete_by_id(
            user_id=command.user_id, movie_id=command.movie_id
        )

    def delete_reviews(self) -> None:
        return self._reviews_repo.delete()
