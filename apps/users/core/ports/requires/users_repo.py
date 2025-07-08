from typing import Protocol
from apps.users.core.domain.user import User


class UsersRepository(Protocol):
    def save(self, user: User) -> None:
        ...

    def delete(self):
        ...
