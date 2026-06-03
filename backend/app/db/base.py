from sqlalchemy.orm import DeclarativeBase, declared_attr


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy ORM models."""

    @declared_attr.directive
    def __tablename__(cls) -> str:
        # Auto-generate table name from class name.
        # Example: WorkoutModel -> workoutmodels
        # Models that need a custom name should override __tablename__ directly.
        return cls.__name__.lower() + "s"
