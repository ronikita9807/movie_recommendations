from sqlalchemy.orm import Session

from apps.users.core.ports.dto.user import UserDTO
from apps.users.core.ports.queries.users_query_service import UsersQueryService


class PostgreSQLUsersQueryService(UsersQueryService):
    def __init__(self, session: Session):
        self.session = session

    def find_by_name(self, name: str) -> list[UserDTO]: ...
