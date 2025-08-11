from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException

from apps.dependencies import Container
from apps.routers.api.schemas import MessageResponse, ErrorResponse
from apps.shared.infra.exceptions.base_exceptions import ObjectExistsException
from apps.users.core.ports.comands.user import UserPublicCommand
from apps.users.core.service.users_creation_service import UsersCreationService

router = APIRouter(tags=["users"])


@router.post(
    "/user",
    summary="Создать пользователя",
    description=(
        "Создаёт нового пользователя в системе. "
        "Данные для создания передаются в теле запроса по схеме `UserPublicCommand`."
    ),
    response_model=MessageResponse,
    responses={
        200: {
            "description": "Пользователь успешно создан",
            "content": {
                "application/json": {
                    "examples": {
                        "ok": {
                            "summary": "Успешное создание",
                            "value": {"message": "User created successfully"},
                        }
                    }
                }
            },
        },
        400: {
            "model": ErrorResponse,
            "description": "Пользователь уже существует",
            "content": {
                "application/json": {
                    "examples": {
                        "exists": {
                            "value": {"detail": "User with this email already exists"}
                        }
                    }
                }
            },
        },
    },
    openapi_extra={
        "requestBody": {
            "content": {
                "application/json": {
                    "examples": {
                        "minimal": {
                            "summary": "Минимальный набор данных",
                            "value": {
                                "username": "harry",
                                "email": "harry@example.com",
                            },
                        },
                        "full": {
                            "summary": "Полный пример",
                            "value": {
                                "username": "hermione",
                                "email": "hermione@example.com",
                                "first_name": "Hermione",
                                "last_name": "Granger",
                                "password": "securepass",
                            },
                        },
                    }
                }
            }
        }
    },
)
@inject
def create_user(
    command: UserPublicCommand,
    users_creation_service: UsersCreationService = Depends(
        Provide[Container.users_creation_service]
    ),
):
    try:
        users_creation_service.create_user(command)
    except ObjectExistsException as error:
        raise HTTPException(status_code=400, detail=str(error))

    return {"message": "User created successfully"}


@router.delete(
    "/users",
    summary="Удалить всех пользователей",
    description="Полностью очищает список пользователей. **Осторожно: операция необратима.**",
    response_model=MessageResponse,
    responses={
        200: {
            "description": "Все пользователи удалены",
            "content": {
                "application/json": {
                    "examples": {
                        "ok": {"value": {"message": "Movies deleted successfully"}}
                    }
                }
            },
        },
    },
)
@inject
def delete_user(
    users_creation_service: UsersCreationService = Depends(
        Provide[Container.users_creation_service]
    ),
):
    users_creation_service.delete_users()
    return {"message": "Movies deleted successfully"}
