from typing import Protocol
from uuid import UUID


class MovieVectorsQueryService(Protocol):
    def get_movies_by_embeddings(
        self, vector: list[float], limit: int
    ) -> list[UUID]: ...
