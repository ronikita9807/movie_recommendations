from apps.users.core.domain.user import User
from apps.users.core.ports.comands.user import UserPublicCommand
from apps.users.core.ports.requires.users_repo import UsersRepository


class UsersCreationService:
    def __init__(
        self,
        users_repo: UsersRepository,
    ):
        self._users_repo = users_repo

    def create_user(self, command: UserPublicCommand) -> None:
        user = User(
            name=command.name,
            surname=command.surname,
            user_name=command.user_name,
            email=command.email,
        )
        self._users_repo.save(user)

    def delete_users(self) -> None:
        return self._users_repo.delete()
