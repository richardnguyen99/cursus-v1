"""
"""

from sqlalchemy import ForeignKey, String, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

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

    state: Mapped[str] = mapped_column(
        db.String(64),
        nullable=True,
    )

    country: Mapped[str] = mapped_column(
        db.String(64),
        nullable=False,
        index=True,
    )

    domains = relationship(
        "UniversityDomain",
        backref="university",
        lazy=True,
        collection_class=list,
    )

    def __init__(self, full_name: str, country: str):
        self.full_name = full_name
        self.country = country

    def __repr__(self):
        return f"<University: {self.full_name}>"

    def __str__(self):
        return f"{self.full_name} - {self.country}"


class UniversityDomain(db.Model):
    """Normalized University Domain model"""

    __tablename__ = "university_domains"

    __table_args__ = (UniqueConstraint("domain_name", "school_id"),)

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)

    domain_name: Mapped[str] = mapped_column(db.String(255), nullable=False)

    school_id: Mapped[int] = mapped_column(
        db.Integer, ForeignKey("universities.id"), nullable=False
    )
