from pydantic import UUID4

from apps.shared.core.domain.base import BaseDTOModel


class UserDTO(BaseDTOModel):
    name: str
    surname: str
    user_name: str
    email: str
