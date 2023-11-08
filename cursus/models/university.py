"""
University model
"""

import datetime

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    UniqueConstraint,
    DateTime,
    event,
    TIMESTAMP,
)
from sqlalchemy.sql import func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship, Relationship

from cursus.util.extensions import db


class University(db.Model):
    """Core university model"""

    __tablename__ = "universities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

    short_name: Mapped[str] = mapped_column(
        String(32),
        nullable=False,
        unique=True,
        index=True,
    )

    full_name: Mapped[str] = mapped_column(
        String(128),
        unique=True,
        nullable=False,
    )

    established: Mapped[int] = mapped_column(
        Integer,
        nullable=True,
        default=1800,
    )

    former_name: Mapped[str] = mapped_column(
        String(128),
        nullable=True,
    )

    motto: Mapped[str] = mapped_column(
        String(512),
        nullable=True,
    )

    type: Mapped[str] = mapped_column(
        String(64),
        nullable=True,
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    founders: Relationship[list["UniversityFounder"]] = relationship(
        "UniversityFounder",
        backref="university",
        lazy=True,
        collection_class=list,
    )

    domains: Relationship[list["UniversityDomain"]] = relationship(
        "UniversityDomain",
        backref="university",
        lazy=True,
        collection_class=list,
    )

    campuses: Relationship[list["UniversityCampus"]] = relationship(
        "UniversityCampus",
        backref="university",
        lazy=True,
        collection_class=list,
    )

    def __init__(
        self,
        full_name: str,
        established: int,
        former_name: str,
        motto: str,
    ):
        self.full_name = full_name
        self.established = established
        self.former_name = former_name
        self.motto = motto

    def __repr__(self):
        return "<University({self.full_name})>".format(self=self)

    def __str__(self):
        return f"{self.full_name} - {self.country}"


class UniversityDomain(db.Model):
    """Normalized University Domain model"""

    __tablename__ = "university_domains"

    __table_args__ = (UniqueConstraint("domain_name", "school_short_name"),)

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    domain_name: Mapped[str] = mapped_column(db.String(128), nullable=False)

    iso639_1: Mapped[str] = mapped_column(String(8), nullable=True)

    type: Mapped[str] = mapped_column(
        String(16), nullable=False, server_default="TLD"
    )

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    school_short_name: Mapped[str] = mapped_column(
        String(32), ForeignKey("universities.short_name"), nullable=False
    )


class UniversityFounder(db.Model):
    """Normalized University Founder model"""

    __tablename__ = "university_founders"

    __table_args__ = (
        UniqueConstraint("first_name", "last_name", "school_short_name"),
    )

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    first_name: Mapped[str] = mapped_column(db.String(64), nullable=False)

    last_name: Mapped[str] = mapped_column(db.String(64), nullable=False)

    middle_name: Mapped[str] = mapped_column(db.String(32), nullable=True)

    suffix: Mapped[str] = mapped_column(db.String(32), nullable=True)

    biography_link: Mapped[str] = mapped_column(db.String(255), nullable=True)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    school_short_name: Mapped[str] = mapped_column(
        String(32), ForeignKey("universities.short_name"), nullable=False
    )

    def __init__(self, first_name: str, last_name: str):
        self.first_name = first_name
        self.last_name = last_name

    def __repr__(self):
        return (
            "<UniversityFounder({self.first_name} {self.last_name})>".format(
                self=self
            )
        )


class UniversityCampus(db.Model):
    """Normalized University Campus model"""

    __tablename__ = "university_campuses"
    __table_args__ = (
        UniqueConstraint(
            "address_street",
            "country_code",
            "school_short_name",
        ),
    )

    address_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, autoincrement=True
    )

    address_street: Mapped[str] = mapped_column(db.String(128), nullable=False)

    address_city: Mapped[str] = mapped_column(db.String(64), nullable=False)

    address_state: Mapped[str] = mapped_column(db.String(64), nullable=True)

    address_zip_code: Mapped[str] = mapped_column(
        db.String(16), nullable=False
    )

    created_at: Mapped[DateTime] = mapped_column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )

    updated_at = db.Column(
        TIMESTAMP(timezone=True),
        server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"),
    )

    country_code: Mapped[str] = mapped_column(
        db.String(2), ForeignKey("countries.alpha2"), nullable=False
    )

    school_short_name: Mapped[str] = mapped_column(
        String(32), ForeignKey("universities.short_name"), nullable=False
    )

    country = relationship("Country")
