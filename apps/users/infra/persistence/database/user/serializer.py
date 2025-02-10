from apps.users.core.domain.user import User
from apps.users.infra.persistence.database.user.user import UserRow


def serialize_user(user: User) -> UserRow:
    return UserRow(
        name=user.name,
        surname=user.surname,
        user_name=user.user_name,
        email=user.email,
        user_id=user.user_id,
    )
