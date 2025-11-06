from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    """Base class for all SQLAlchemy models"""
    pass


class CountTable(Base):
    """
    Model representing a count table with a count_number field.

    Attributes:
        id: Primary key, auto-incremented
        count_number: Integer field to store count values
        description: Optional description text
        created_at: Timestamp when record was created
        updated_at: Timestamp when record was last updated
    """
    __tablename__ = "count_table"

    # Primary key
    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True,
        comment="Primary key"
    )

    # Main field
    count_number: Mapped[int] = mapped_column(
        Integer, 
        nullable=False, 
        default=0, 
        index=True,
        comment="Count number value"
    )

    # Optional description
    description: Mapped[Optional[str]] = mapped_column(
        String(255), 
        nullable=True,
        comment="Optional description"
    )

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(),
        nullable=False,
        comment="Creation timestamp"
    )

    updated_at: Mapped[Optional[datetime]] = mapped_column(
        DateTime(timezone=True), 
        onupdate=func.now(),
        nullable=True,
        comment="Last update timestamp"
    )

    def __repr__(self) -> str:
        """String representation of CountTable instance"""
        return (
            f"<CountTable("
            f"id={self.id}, "
            f"count_number={self.count_number}, "
            f"description={self.description!r}"
            f")>"
        )

    def __str__(self) -> str:
        """User-friendly string representation"""
        return f"Count #{self.id}: {self.count_number}"