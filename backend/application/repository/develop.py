from typing import List

from ..database.develop import DevelopOrm
from ..database.database import new_session
from sqlalchemy import select

from ..schemas.develop import SDevelopAdd


class DevelopRepository:
    @classmethod
    async def add_one(cls, data: SDevelopAdd) -> int:
        async with new_session() as session:
            develop_dict = data.model_dump()

            develop = DevelopOrm(**develop_dict)
            session.add(develop)
            await session.flush()
            await session.commit()
            return develop.id

    @classmethod
    async def add_photo(cls, develop_id: int, photo_data: bytes) -> None:
        async with new_session() as session:
            develop = await session.get(DevelopOrm, develop_id)
            develop.photo = photo_data
            await session.commit()

    @classmethod
    async def get_photo(cls, develop_id: int) -> bytes:
        async with new_session() as session:
            develop = await session.get(DevelopOrm, develop_id)
            if develop and develop.photo:
                return develop.photo
            else:
                return b""

    @classmethod
    async def get_develop_details(cls, develop_id: int) -> dict:
        async with new_session() as session:
            develop = await session.get(DevelopOrm, develop_id)
            if develop:
                return {
                    "id": develop.id,
                    "firstName": develop.firstName,
                    "lastName": develop.lastName,
                    "aboutDevelop": develop.aboutDevelop,
                    "description": develop.description,
                }
            else:
                return {"error": "develop not found"}

    @classmethod
    async def delete_develop(cls, develop_id: int) -> None:
        async with new_session() as session:
            develop = await session.get(DevelopOrm, develop_id)
            if develop:
                await session.delete(develop)
                await session.commit()
            else:
                raise ValueError(f"develop with ID {develop_id} not found.")

    @classmethod
    async def get_all_develops(cls) -> List[dict]:
        async with new_session() as session:
            develop = await session.execute(select(DevelopOrm))
            return [
                {
                    "id": develop.id,
                    "firstName": develop.firstName,
                    "lastName": develop.lastName,
                    "aboutDevelop": develop.aboutDevelop,
                    "description": develop.description,
                }
                for develop in develop.scalars()
            ]
