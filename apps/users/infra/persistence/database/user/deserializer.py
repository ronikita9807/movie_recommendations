from apps.users.core.domain.user import User
from apps.users.infra.persistence.database.user.user import UserRow


def deserialize_user(user_row: UserRow) -> User:
    return User(
        user_id=user_row.user_id,
        name=user_row.name,
        surname=user_row.surname,
        user_name=user_row.user_name,
        email=user_row.email,
    )
