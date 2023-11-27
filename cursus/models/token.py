# -*- coding: utf-8 -*-

"""Cursus Token model for API authorization
"""

import cuid2

from datetime import datetime
from typing import Any
from sqlalchemy import (
    String,
    Integer,
    DateTime,
    ForeignKey,
)
from sqlalchemy.orm import Mapped, mapped_column, Relationship, relationship

from cursus.util.extensions import db

cuid_generator: cuid2.Cuid = cuid2.Cuid(length=12)


class ActiveToken(db.Model):
    __tablename__ = "active_tokens"

    id: Mapped[int] = mapped_column(
        Integer,
        primary_key=True,
        autoincrement=True,
    )

    token: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
        index=True,
        unique=True,
    )

    created: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        default=datetime.utcnow,
    )

    user_id: Mapped[str] = mapped_column(
        String(11),
        ForeignKey(
            "users.id",
            ondelete="CASCADE",
            onupdate="CASCADE",
        ),
    )

    def __init__(self, token: str, user_id: str) -> None:
        self.token = token
        self.user_id = user_id

    def __repr__(self) -> str:
        return f"<ActiveToken {self.token}>"

    def __str__(self) -> str:
        return self.token

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, str):
            return self.token == other
        elif isinstance(other, ActiveToken):
            return self.token == other.token
        return False

    @staticmethod
    def generate_token() -> str:
        """Generate a new token"""
        return cuid_generator.generate()
