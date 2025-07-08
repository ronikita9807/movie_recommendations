from uuid import UUID

from sqlalchemy import Column, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from apps.reviews.infra.persistence.database.review.review import ReviewRow
from apps.shared.infra.persistence.database.base import Base


class UserRow(Base):
    __tablename__ = "users"

    user_id: Mapped[UUID] = mapped_column(primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    user_name = Column(String)
    email = Column(String)

    reviews: Mapped[list[ReviewRow]] = relationship(
        "ReviewRow",
        back_populates="user",
        cascade="all, delete-orphan",
    )
