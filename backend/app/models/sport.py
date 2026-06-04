import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID
from app.db.base import Base


class Sport(Base):
    __tablename__ = "sports"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    slug: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    has_gps: Mapped[bool] = mapped_column(Boolean, default=True)

    # Relationships
    workouts: Mapped[list["Workout"]] = relationship(back_populates="sport")

    def __repr__(self) -> str:
        return f"<Sport {self.slug}>"
