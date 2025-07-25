

from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException, Path, Response

from apps.dependencies import Container
from apps.reviews.core.ports.comands.review import ReviewPublicCommand
from apps.reviews.core.ports.comands.review_delete_command import ReviewDeletePublicCommand
from apps.reviews.core.ports.queries.reviews_query_service import ReviewsQueryService
from apps.reviews.core.service.reviews_creation_service import ReviewsCreationService
from apps.shared.infra.exceptions.base_exceptions import ObjectExistsException
from apps.users.core.service.users_creation_service import UsersCreationService

router = APIRouter()


@router.post("/review")
@inject
def create_review(
    command: ReviewPublicCommand,
    reviews_creation_service: ReviewsCreationService = Depends(
        Provide[Container.reviews_creation_service]
    ),
):
    try:
        reviews_creation_service.create_review(command)
    except ObjectExistsException as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {"message": "Review created successfully"}


@router.patch("/review")
@inject
def update_review(
    command: ReviewPublicCommand,
    reviews_creation_service: ReviewsCreationService = Depends(
        Provide[Container.reviews_creation_service]
    ),
):
    try:
        reviews_creation_service.update_review(command)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return {"message": "Review updated successfully"}


@router.delete("/review")
@inject
def delete_review(
    command: ReviewDeletePublicCommand,
    reviews_creation_service: ReviewsCreationService = Depends(
        Provide[Container.reviews_creation_service]
    ),
):
    try:
        reviews_creation_service.delete_review(command)
    except Exception as error:
        raise HTTPException(status_code=500, detail=str(error))

    return Response(status_code=204)


@router.get("/reviews/by_user_name/{name}")
@inject
def get_reviews(
    name: str = Path(..., title="User name", example="Harry Potter"),
    reviews_query_service: ReviewsQueryService = Depends(
        Provide[Container.reviews_query_service]
    ),
):
    reviews = [str(review.model_dump()) for review in reviews_query_service.find_by_user_name(name)]
    return {f"Reviews: {"\n".join(reviews)}"}


@router.delete("/reviews")
@inject
def delete_review(
    reviews_creation_service: UsersCreationService = Depends(
        Provide[Container.reviews_creation_service]
    ),
):
    reviews_creation_service.delete_users()
    return {"message": "Reviews deleted successfully"}
