from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from ..database.database import Model


class DevelopOrm(Model):
    __tablename__ = "develop"

    id: Mapped[int] = mapped_column(primary_key=True)
    firstName: Mapped[str]
    lastName: Mapped[Optional[str]] = None
    aboutDevelop: Mapped[Optional[str]] = None
    description: Mapped[Optional[str]] = None
    photo: Mapped[Optional[bytes]]
