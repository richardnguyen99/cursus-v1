"""
University model
"""

import string
import random

from sqlalchemy import (
    ForeignKey,
    String,
    Integer,
    UniqueConstraint,
    DateTime,
    event,
)
from sqlalchemy.sql import func
from sqlalchemy.orm import Mapped, mapped_column, relationship, Relationship

from cursus.util.extensions import db


class University(db.Model):
    """Core university model"""

    __tablename__ = "universities"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)

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
        String(64),
        nullable=True,
    )

    motto: Mapped[str] = mapped_column(
        String(256),
        nullable=True,
    )

    type: Mapped[str] = mapped_column(
        String(64),
        nullable=True,
    )

    object_id: Mapped[str] = mapped_column(
        String(11),
        nullable=False,
        unique=True,
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

    __table_args__ = (UniqueConstraint("domain_name", "school_id"),)

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    domain_name: Mapped[str] = mapped_column(db.String(255), nullable=False)

    created_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[DateTime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        server_onupdate=func.now(),
    )

    school_id: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("universities.id"), nullable=False
    )


class UniversityFounder(db.Model):
    """Normalized University Founder model"""

    __tablename__ = "university_founders"

    __table_args__ = (UniqueConstraint("founder_name", "school_id"),)

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    founder_name: Mapped[str] = mapped_column(db.String(255), nullable=False)

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

    school_id: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("universities.id"), nullable=False
    )


class UniversityCampus(db.Model):
    """Normalized University Campus model"""

    __tablename__ = "university_campuses"
    __table_args__ = (
        UniqueConstraint(
            "address_number", "address_street", "country_code", "school_id"
        ),
    )

    address_id: Mapped[int] = mapped_column(
        db.Integer, primary_key=True, autoincrement=True
    )

    address_number: Mapped[str] = mapped_column(db.String(16), nullable=False)

    address_street: Mapped[str] = mapped_column(db.String(64), nullable=False)

    address_city: Mapped[str] = mapped_column(db.String(64), nullable=False)

    address_state: Mapped[str] = mapped_column(db.String(64), nullable=False)

    address_zip_code: Mapped[str] = mapped_column(
        db.String(16), nullable=False
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

    country_code: Mapped[str] = mapped_column(
        db.String(2), ForeignKey("countries.alpha2"), nullable=False
    )

    school_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("universities.id"), nullable=False, index=True
    )

    country = relationship("Country")


def _generate_string_id(length=11) -> str:
    """Generate a random string ID for the University object"""

    characters = string.ascii_letters + string.digits

    while True:
        new_id = "".join(random.choice(characters) for _ in range(length))
        existing_video = University.query.get({"object_id": new_id})

        if existing_video is None:
            return new_id


@event.listens_for(University, "before_insert")
def generate_string_id(mapper, connection, target) -> None:
    """Generate a random string ID for the University object"""

    target.object_id = _generate_string_id()
