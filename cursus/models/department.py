# -*- coding: utf-8 -*-

"""
Departments model
"""

import sqlalchemy as sa

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    UniqueConstraint,
    DateTime,
    TIMESTAMP,
)
from sqlalchemy.orm import Mapped, mapped_column, Relationship, relationship
from sqlalchemy.sql import func

from cursus.util.extensions import db
from cursus.models.course import Course


class Department(db.Model):
    """Core department model"""

    __tablename__ = "departments"

    __table_args__ = (UniqueConstraint("code", "school_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
    )

    code: Mapped[str] = mapped_column(
        String(16),
        nullable=False,
        index=True,
    )

    website: Mapped[str] = mapped_column(
        String(128),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    university_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("universities.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    school_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey("schools.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )

    courses: Relationship[list["Course"]] = relationship(
        "Course",
        backref="department",
        lazy=True,
        collection_class=list,
        cascade="all, delete-orphan",
    )

    def __init__(self, name: str, code: str, website: str, school_id: int):
        self.name = name
        self.code = code
        self.website = website
        self.school_id = school_id

    def __repr__(self):
        return f"<Department (name={self.name})>"

    def __str__(self) -> str:
        return "{self.name} ({self.code})"
