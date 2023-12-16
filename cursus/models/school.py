# -*- coding: utf-8 -*-

"""
Schools model
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

from .department import Department


class School(db.Model):
    """Core school model"""

    __tablename__ = "schools"

    __table_args__ = (UniqueConstraint("name", "university_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    name: Mapped[str] = mapped_column(
        String(128),
        nullable=False,
        index=True,
    )

    website: Mapped[str] = mapped_column(
        String(128),
        nullable=True,
    )

    university_id: Mapped[int] = mapped_column(
        Integer,
        ForeignKey(
            "universities.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
        nullable=False,
    )

    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    modified_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    departments: Relationship[list["Department"]] = relationship(
        "Department",
        backref="school",
        lazy=True,
        cascade="all, delete-orphan",
        collection_class=set,
    )
