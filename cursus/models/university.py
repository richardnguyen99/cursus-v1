from sqlalchemy.orm import Mapped, mapped_column

from cursus.util.extensions import db


class University(db.Model):
    __tablename__ = "university"

    id: Mapped[int] = mapped_column(db.Integer, primary_key=True)
    username: Mapped[str] = mapped_column(
        db.String, unique=True, nullable=False
    )
    email: Mapped[str] = mapped_column(db.String)

    def __init__(self, username: str, email: str):
        self.username = username
        self.email = email

    def __repr__(self):
        return f"<User {self.username}>"
