from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Base class untuk semua SQLAlchemy models."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Auto-generate table name dari class name
        # contoh: WorkoutModel -> workouts (manual override tetap bisa)
        return cls.__name__.lower() + "s"
