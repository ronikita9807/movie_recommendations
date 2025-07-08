from typing import Protocol
from apps.users.core.ports.dto.user import UserDTO


class UsersQueryService(Protocol):
    def find_by_name(self, name: str) -> list[UserDTO]:
        ...
