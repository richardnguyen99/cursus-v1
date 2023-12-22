# -*- coding: utf-8 -*-

"""
Courses model
"""

import sqlalchemy as sa

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    Boolean,
    UniqueConstraint,
    DateTime,
    TIMESTAMP,
)
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from cursus.util.extensions import db


class Course(db.Model):
    """Core course model"""

    __tablename__ = "courses"

    __table_args__ = (UniqueConstraint("code", "school_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    title: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
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

    active: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        default=True,
    )

    level: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
    )

    subject: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    description: Mapped[str] = mapped_column(
        String(1024),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    modified_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
    )

    department_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "departments.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
        index=True,
    )

    school_id: Mapped[str] = mapped_column(
        String(32),
        ForeignKey(
            "universities.short_name",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    def __init__(self, title, code, website, active=True):
        self.title = title
        self.code = code
        self.website = website
        self.active = active

    def __repr__(self):
        return f"<Course {self.code}>"

    def __str__(self):
        return self.code
