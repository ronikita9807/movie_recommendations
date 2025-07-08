from sqlalchemy import String, Integer, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.shared.infra.persistence.database.base import Base


class ReviewRow(Base):
    __tablename__ = "reviews"

    id: Mapped[UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.user_id", ondelete="CASCADE"),
        nullable=False,
    )
    movie_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("movie.movie_id", ondelete="CASCADE"),
        nullable=False,
    )
    text: Mapped[str] = mapped_column(String, nullable=True)
    score: Mapped[int] = mapped_column(Integer, nullable=False)

    # relations
    user: Mapped["UserRow"] = relationship("UserRow", back_populates="reviews")
    movie: Mapped["MovieRow"] = relationship("MovieRow", back_populates="reviews")
