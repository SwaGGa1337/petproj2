from typing import Optional

from sqlalchemy.orm import Mapped, mapped_column

from application.database.database import Model


class ClientOrm(Model):
    __tablename__ = "client"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    email: Mapped[str]
    description: Mapped[Optional[str]]
