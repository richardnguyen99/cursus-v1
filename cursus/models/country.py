# -*- coding: utf-8 -*-

"""
Country model
"""

from sqlalchemy import String, Integer, UniqueConstraint, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column

from cursus.util.extensions import db


class Country(db.Model):
    """Core country model"""

    __tablename__ = "countries"
    __table_args__ = (UniqueConstraint("name", "alpha2", "alpha3"),)

    id: Mapped[int] = mapped_column(
        Integer, primary_key=True, autoincrement=True
    )

    name: Mapped[str] = mapped_column(
        String(128), unique=True, nullable=False, index=True
    )

    alpha2: Mapped[str] = mapped_column(
        String(2), unique=True, nullable=False, index=True
    )

    alpha3: Mapped[str] = mapped_column(
        String(3), unique=True, nullable=False, index=True
    )

    country_code: Mapped[str] = mapped_column(
        String(3), unique=True, nullable=False, index=True
    )

    iso3166_2: Mapped[str] = mapped_column(
        String(16), unique=True, nullable=False, index=True
    )

    region: Mapped[str] = mapped_column(String(64), nullable=True)

    subregion: Mapped[str] = mapped_column(String(64), nullable=True)

    region_code: Mapped[str] = mapped_column(String(3), nullable=True)

    sub_region_code: Mapped[str] = mapped_column(String(3), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )
