from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException, Path, Response, status

from apps.dependencies import Container
from apps.reviews.core.ports.comands.review import ReviewPublicCommand
from apps.reviews.core.ports.comands.review_delete_command import (
    ReviewDeletePublicCommand,
)
from apps.reviews.core.ports.queries.reviews_query_service import ReviewsQueryService
from apps.reviews.core.service.reviews_creation_service import ReviewsCreationService
from apps.routers.api.schemas import MessageResponse, ErrorResponse
from apps.shared.infra.exceptions.base_exceptions import ObjectExistsException


router = APIRouter(tags=["reviews"])


@router.post(
    "/review",
    summary="Создать отзыв",
    description=(
        "Создаёт новый отзыв пользователя к фильму. "
        "Идентификаторы и схема тела берутся из `ReviewPublicCommand`."
    ),
    response_model=MessageResponse,
    responses={
        200: {
            "description": "Отзыв создан",
            "content": {
                "application/json": {
                    "examples": {
                        "ok": {
                            "summary": "Успех",
                            "value": {"message": "Review created successfully"},
                        }
                    }
                }
            },
        },
        400: {
            "model": ErrorResponse,
            "description": "Такой отзыв уже существует (например, дубль по user/movie)",
            "content": {
                "application/json": {
                    "examples": {
                        "exists": {
                            "value": {"detail": "Review already exists for user/movie"}
                        }
                    }
                }
            },
        },
        500: {"model": ErrorResponse, "description": "Неожиданная ошибка"},
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "minimal": {
                            "summary": "Минимум полей",
                            "value": {
                                "user_name": "harry",
                                "movie_id": 671,
                                "rating": 5,
                                "text": "Magic!",
                            },
                        },
                        "full": {
                            "summary": "Расширенный пример",
                            "value": {
                                "user_name": "hermione",
                                "movie_id": 671,
                                "rating": 4,
                                "text": "Great, but long.",
                                "spoiler": False,
                            },
                        },
                    }
                }
            }
        }
    },
)
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


@router.patch(
    "/review",
    summary="Обновить отзыв",
    description="Частично или полностью обновляет существующий отзыв.",
    response_model=MessageResponse,
    responses={
        200: {
            "description": "Отзыв обновлён",
            "content": {
                "application/json": {
                    "examples": {
                        "ok": {
                            "summary": "Успех",
                            "value": {"message": "Review updated successfully"},
                        }
                    }
                }
            },
        },
        404: {"model": ErrorResponse, "description": "Отзыв не найден"},
        500: {"model": ErrorResponse, "description": "Неожиданная ошибка"},
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "update_text": {
                            "value": {
                                "user_name": "harry",
                                "movie_id": 671,
                                "text": "Edited text",
                            }
                        },
                        "update_rating": {
                            "value": {
                                "user_name": "harry",
                                "movie_id": 671,
                                "rating": 4,
                            }
                        },
                    }
                }
            }
        }
    },
)
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


@router.delete(
    "/review",
    summary="Удалить один отзыв",
    description="Удаляет конкретный отзыв.",
    responses={
        204: {"description": "Удалено, тело отсутствует"},
        404: {"model": ErrorResponse, "description": "Отзыв не найден"},
        500: {"model": ErrorResponse, "description": "Неожиданная ошибка"},
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "by_user_and_movie": {
                            "value": {"user_name": "harry", "movie_id": 671}
                        },
                        "by_id": {"value": {"review_id": 123}},
                    }
                }
            }
        }
    },
)
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

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get(
    "/reviews/by_user_name/{name}",
    summary="Получить отзывы пользователя по имени",
    description="Возвращает список отзывов, найденных по имени пользователя.",
    responses={
        200: {
            "description": "Массив отзывов (форма зависит от `ReviewsQueryService`)",
            "content": {
                "application/json": {
                    "examples": {
                        "some": {
                            "summary": "Есть отзывы",
                            "value": {
                                "reviews": [
                                    {
                                        "movie_id": 671,
                                        "rating": 5,
                                        "text": "Magic!",
                                        "created_at": "2025-08-01T12:00:00Z",
                                    },
                                    {
                                        "movie_id": 672,
                                        "rating": 4,
                                        "text": "Nice sequel.",
                                    },
                                ]
                            },
                        },
                        "empty": {"summary": "Пусто", "value": {"reviews": []}},
                    }
                }
            },
        }
    },
)
@inject
def get_reviews(
    name: str = Path(..., title="User name", example="harry"),
    reviews_query_service: ReviewsQueryService = Depends(
        Provide[Container.reviews_query_service]
    ),
):
    reviews = [
        review.model_dump() for review in reviews_query_service.find_by_user_name(name)
    ]
    return {"reviews": reviews}


@router.delete(
    "/reviews",
    summary="Удалить все отзывы",
    description="Полностью очищает коллекцию отзывов. **Осторожно: разрушительная операция.**",
    response_model=MessageResponse,
    responses={
        200: {
            "description": "Все отзывы удалены",
            "content": {
                "application/json": {
                    "examples": {
                        "ok": {"value": {"message": "Reviews deleted successfully"}}
                    }
                }
            },
        },
        500: {"model": ErrorResponse, "description": "Неожиданная ошибка"},
    },
)
@inject
def delete_reviews_all(
    reviews_creation_service: ReviewsCreationService = Depends(
        Provide[Container.reviews_creation_service]
    ),
):
    reviews_creation_service.delete_reviews()
    return {"message": "Reviews deleted successfully"}
