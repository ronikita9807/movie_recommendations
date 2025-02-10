from apps.shared.core.ports.commands import PublicCommand


class UserPublicCommand(PublicCommand):
    name: str
    surname: str
    user_name: str
    email: str
