from typing import Optional, Iterable
from uuid import UUID

from sqlalchemy.orm import Session

from apps.movies.core.domain.movie import Movie
from apps.movies.core.ports.requires.movies_repo import MoviesRepository
from apps.movies.infra.persistence.database.movie.deserializer import (
    deserialize_movie,
)
from apps.movies.infra.persistence.database.movie.movie import MovieRow
from apps.movies.infra.persistence.database.movie.serializer import serialize_movie
from apps.shared.infra.exceptions.base_exceptions import ObjectExistsException
from apps.users.core.domain.user import User
from apps.users.core.ports.requires.users_repo import UsersRepository
from apps.users.infra.persistence.database.user.serializer import serialize_user
from apps.users.infra.persistence.database.user.user import UserRow


class PostgreSQLUsersRepository(UsersRepository):
    def __init__(self, session: Session):
        self.session = session

    def save(self, user: User) -> None:
        previous_user = self.session.query(UserRow).filter(UserRow.user_name == user.user_name).one_or_none()
        if previous_user:
            raise ObjectExistsException("User already exists in database")
        user_row = serialize_user(user)
        self.session.add(user_row)
        self.session.commit()

    def delete(self):
        self.session.query(UserRow).delete()
        self.session.commit()
