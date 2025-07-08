from pydantic import UUID4

from apps.shared.core.ports.commands import PublicCommand


class ReviewPublicCommand(PublicCommand):
    user_id: UUID4
    movie_id: UUID4
    text: str
    score: int
