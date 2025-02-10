from dependency_injector.wiring import Provide, inject
from fastapi import Depends, APIRouter, HTTPException

from apps.dependencies import Container
from apps.shared.infra.exceptions.base_exceptions import ObjectExistsException
from apps.users.core.ports.comands.user import UserPublicCommand
from apps.users.core.service.users_creation_service import UsersCreationService

router = APIRouter()


@router.post("/user")
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


@router.delete("/users")
@inject
def delete_user(
    users_creation_service: UsersCreationService = Depends(
        Provide[Container.users_creation_service]
    ),
):
    users_creation_service.delete_users()
    return {"message": "Movies deleted successfully"}
