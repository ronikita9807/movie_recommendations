from sqlalchemy import select, delete
from sqlalchemy.orm import Session

from apps.shared.infra.exceptions.base_exceptions import ObjectExistsException
from apps.users.core.domain.user import User
from apps.users.core.ports.requires.users_repo import UsersRepository
from apps.users.infra.persistence.database.user.serializer import serialize_user
from apps.users.infra.persistence.database.user.user import UserRow


class PostgreSQLUsersRepository(UsersRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> None:
        stmt = select(UserRow).where(UserRow.user_name == user.user_name)
        existing = self.session.execute(stmt).scalar_one_or_none()
        if existing:
            raise ObjectExistsException("User already exists in database")
        user_row = serialize_user(user)
        with self.session.begin():
            self.session.add(user_row)

    def delete(self) -> None:
        stmt = delete(UserRow)
        with self.session.begin():
            self.session.execute(stmt)
