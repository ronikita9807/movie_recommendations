from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, Path, HTTPException, status
from sqlalchemy.exc import IntegrityError

from apps.dependencies import Container
from apps.movies.core.ports.queries.movies_query_service import MoviesQueryService
from apps.movies.core.service.movie_vectors_generation_service import (
    MovieVectorsGenerationService,
)
from apps.movies.core.service.movies_save_service import MoviesSaveService
from apps.movies.core.service.search_movie_by_description_service import (
    SearchMovieByDescriptionService,
)
from apps.routers.api.schemas import MessageResponse, ErrorResponse

router = APIRouter(tags=["movies"])


@router.post(
    "/update-movies",
    summary="Обновить (синхронизировать) каталог фильмов",
    description=(
        "Тригерит процесс обновления фильмов из источников данных. "
        "Используйте при первичной загрузке или периодической синхронизации."
    ),
    response_model=MessageResponse,
    responses={
        200: {
            "description": "Успешно инициировано обновление",
            "content": {
                "application/json": {
                    "examples": {
                        "ok": {
                            "summary": "Стандартный успех",
                            "value": {"message": "Movies saved successfully"},
                        }
                    }
                }
            },
        },
        500: {"model": ErrorResponse, "description": "Неожиданная ошибка"},
    },
)
@inject
def update_movies(
    movies_save_service: MoviesSaveService = Depends(
        Provide[Container.movies_save_service]
    ),
):
    movies_save_service.update_movies()
    return {"message": "Movies saved successfully"}


@router.post(
    "/update-movies-vectors",
    summary="Сгенерировать/обновить векторные представления фильмов",
    description=(
        "Создаёт/обновляет эмбеддинги фильмов для семантического поиска. "
        "Повторные запуски безопасны; при конфликте уникальности вернётся 409."
    ),
    response_model=MessageResponse,
    responses={
        200: {
            "description": "Эмбеддинги успешно сгенерированы/обновлены",
            "content": {
                "application/json": {
                    "examples": {
                        "ok": {
                            "summary": "Стандартный успех",
                            "value": {"message": "Movies vectors saved successfully"},
                        }
                    }
                }
            },
        },
        409: {
            "model": ErrorResponse,
            "description": "Конфликт уникальности (например, попытка повторной вставки)",
            "content": {
                "application/json": {
                    "examples": {
                        "duplicate_key": {
                            "summary": "Дубликат",
                            "value": {
                                "detail": "Duplicate key error: duplicate key value violates unique constraint ..."
                            },
                        }
                    }
                }
            },
        },
    },
)
@inject
def update_movies_vectors(
    movie_vectors_generation_service: MovieVectorsGenerationService = Depends(
        Provide[Container.movie_vectors_generation_service]
    ),
):
    try:
        movie_vectors_generation_service.create_vectorized_representation()
        return {"message": "Movies vectors saved successfully"}
    except IntegrityError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Duplicate key error: {e.orig}",
        )


@router.delete(
    "/movies",
    summary="Удалить все фильмы",
    description="Полностью очищает коллекцию фильмов. Используйте с осторожностью.",
    response_model=MessageResponse,
    responses={
        200: {
            "description": "Фильмы удалены",
            "content": {
                "application/json": {
                    "examples": {
                        "ok": {
                            "summary": "Стандартный успех",
                            "value": {"message": "Movies deleted successfully"},
                        }
                    }
                }
            },
        },
    },
)
@inject
def delete_movies(
    movies_save_service: MoviesSaveService = Depends(
        Provide[Container.movies_save_service]
    ),
):
    movies_save_service.delete_movies()
    return {"message": "Movies deleted successfully"}


@router.delete(
    "/movies-vectors",
    summary="Удалить все векторные представления",
    description="Очищает таблицу/хранилище эмбеддингов, не затрагивая сами фильмы.",
    response_model=MessageResponse,
    responses={
        200: {
            "description": "Вектора удалены",
            "content": {
                "application/json": {
                    "examples": {
                        "ok": {
                            "summary": "Стандартный успех",
                            "value": {"message": "Movies vectors deleted successfully"},
                        }
                    }
                }
            },
        },
    },
)
@inject
def delete_movie_vectors(
    movie_vectors_generation_service: MovieVectorsGenerationService = Depends(
        Provide[Container.movie_vectors_generation_service]
    ),
):
    movie_vectors_generation_service.delete_movies_vectors()
    return {"message": "Movies vectors deleted successfully"}


@router.get(
    "/movies/by_name/{name}",
    summary="Поиск фильмов по названию",
    description=(
        "Ищет фильмы по подстроке `name` "
        "Возвращает массив объектов фильмов. "
        "Пример запроса: `/api/movies/by_name/Harry Potter`"
    ),
    responses={
        200: {
            "description": "Список найденных фильмов",
            "content": {
                "application/json": {
                    "examples": {
                        "multiple": {
                            "summary": "Несколько совпадений",
                            "value": [
                                {
                                    "id": 671,
                                    "name": "Harry Potter and the Philosopher's Stone",
                                    "year": 2001,
                                    "description": "A boy discovers he's a wizard.",
                                    "genres": ["Fantasy", "Adventure"],
                                    "rating": 7.6,
                                },
                                {
                                    "id": 672,
                                    "name": "Harry Potter and the Chamber of Secrets",
                                    "year": 2002,
                                    "description": "The second year at Hogwarts.",
                                    "genres": ["Fantasy", "Adventure"],
                                    "rating": 7.4,
                                },
                            ],
                        },
                        "empty": {"summary": "Ничего не найдено", "value": []},
                    }
                }
            },
        }
    },
)
@inject
def find_by_name(
    name: str = Path(
        ...,
        title="Film name",
        description="Часть или полное название фильма",
        example="Harry Potter",
    ),
    movies_query_service: MoviesQueryService = Depends(
        Provide[Container.movies_query_service]
    ),
):
    return movies_query_service.find_by_name(name=name)


@router.get(
    "/movies/by_desription/{description}",
    summary="Семантический поиск по описанию",
    description=(
        "Ищет фильмы, близкие по смыслу к тексту `description` (например, с помощью векторного поиска). "
        "Возвращает массив похожих фильмов, отсортированных по релевантности."
    ),
    responses={
        200: {
            "description": "Список релевантных фильмов",
            "content": {
                "application/json": {
                    "examples": {
                        "titanic_like": {
                            "summary": "По описанию «Джек спасает Роуз с корабля»",
                            "value": [
                                {
                                    "id": 597,
                                    "name": "Titanic",
                                    "year": 1997,
                                    "description": "A love story aboard the ill-fated RMS Titanic.",
                                    "genres": ["Drama", "Romance"],
                                    "rating": 7.8,
                                },
                                {
                                    "id": 152601,
                                    "name": "A Night to Remember",
                                    "year": 1958,
                                    "description": "Dramatization of the sinking of the Titanic.",
                                    "genres": ["Drama", "History"],
                                    "rating": 7.4,
                                },
                            ],
                        }
                    }
                }
            },
        }
    },
)
@inject
def find_by_desription(
    description: str = Path(
        ...,
        title="Film description",
        description="Короткое описание сюжета/сцены",
        example="Jack trying to save Rose from ship",
    ),
    search_movie_by_description_service: SearchMovieByDescriptionService = Depends(
        Provide[Container.search_movie_by_description_service]
    ),
):
    return search_movie_by_description_service.find_movies_by_description(
        description=description
    )
