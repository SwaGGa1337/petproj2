from sqlalchemy import select, delete

from ..database.client import ClientOrm
from ..database.database import new_session

from ..schemas.client import SClientAdd, SClient


class ClientRepository:

    @classmethod
    async def add_one(cls, data: SClientAdd) -> int:
        async with new_session() as session:
            client_dict = data.model_dump()

            client = ClientOrm(**client_dict)
            session.add(client)
            await session.flush()
            await session.commit()
            return client.id

    @classmethod
    async def find_all(cls) -> list[SClient]:
        async with new_session() as session:
            query = select(ClientOrm)
            result = await session.execute(query)
            client_models = result.scalars().all()
            client_schemas = [
                SClient.model_validate(client_model) for client_model in client_models
            ]
            return client_schemas

    @classmethod
    async def find_by_id(cls, client_id: int) -> SClient:
        async with new_session() as session:
            client = await session.get(ClientOrm, client_id)
            if client:
                return SClient.model_validate(client)
            else:
                return None

    @classmethod
    async def delete_by_id(cls, client_id: int) -> None:
        async with new_session() as session:
            query = delete(ClientOrm).where(ClientOrm.id == client_id)
            await session.execute(query)
            await session.commit()
