"""
"""

from sqlalchemy.orm import Mapped, mapped_column

from cursus.util.extensions import db


class University(db.Model):
    """Core university model"""

    __tablename__ = "universities"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        db.String, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(db.String)

    full_name: Mapped[str] = mapped_column(
        db.String,
        unique=True,
        nullable=False,
    )

    state: Mapped[str] = mapped_column(
        db.String,
        nullable=True,
    )

    country: Mapped[str] = mapped_column(
        db.String,
        nullable=False,
    )

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User {self.username}>"
