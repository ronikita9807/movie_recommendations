from sqlalchemy.orm import Session

from apps.users.core.ports.dto.user import UserDTO
from apps.users.core.ports.queries.users_query_service import UsersQueryService
from sqlalchemy import select
from sqlalchemy.orm import Session

from apps.users.core.ports.queries.users_query_service import UsersQueryService
from apps.users.core.ports.dto.user import UserDTO
from apps.users.infra.persistence.database.user.user import UserRow


class PostgreSQLUsersQueryService(UsersQueryService):
    def __init__(self, session: Session):
        self.session = session

    def find_by_name(self, name: str) -> list[UserDTO]:
        pattern = f"%{name}%"
        stmt = select(UserRow).where(UserRow.user_name.ilike(pattern))
        with self.session.begin():
            results = self.session.execute(stmt).scalars().all()
        return [self._deserialize_user(row) for row in results]

    @staticmethod
    def _deserialize_user(user_row: UserRow) -> UserDTO:
        return UserDTO(
            name=user_row.name,
            surname=user_row.surname,
            user_name=user_row.user_name,
            email=user_row.email,
        )
