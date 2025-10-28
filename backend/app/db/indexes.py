"""Database indexes - SQLModel handles indexes via model definitions."""

# Note: With SQLModel, indexes are defined in the model classes using Field(index=True).
# No separate index creation is needed. This file is kept for backwards compatibility.


async def ensure_indexes(db=None) -> None:
    """Ensure database indexes. SQLModel creates indexes automatically."""
    pass  # No-op - indexes are created via SQLModel.metadata.create_all
