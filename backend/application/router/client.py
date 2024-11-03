from fastapi import APIRouter, Form
from starlette import status

from ..repository.client import ClientRepository
from ..schemas.client import SClientAdd, SClient, SClientId


router = APIRouter(
    prefix="/clients",
    tags=["Clients"],
)


@router.post("/add_client", response_model=SClientId, status_code=status.HTTP_200_OK)
async def add_client(
    name: str = Form(...),
    email: str = Form(...),
    description: str = Form(None),
) -> SClientId:
    client = SClientAdd(
        name=name,
        email=email,
        description=description,
    )
    client_id = await ClientRepository.add_one(client)
    return SClientId(Add=True, client_id=client_id)


@router.get("/get_all_clients")
async def get_clients() -> list[SClient]:
    client = await ClientRepository.find_all()
    return client


@router.get("/find_by_id/{client_id}")
async def find_client_by_id(client_id: int) -> SClient:
    client = await ClientRepository.find_by_id(client_id)
    return client


@router.delete("/clients/{client_id}")
async def delete_client(client_id: int) -> str:
    existing_client = await ClientRepository.find_by_id(client_id)
    if existing_client:
        await ClientRepository.delete_by_id(client_id)
        return f"Client with id {client_id} has been deleted"
    else:
        return f"Client with id {client_id} does not exist, deletion failed"
