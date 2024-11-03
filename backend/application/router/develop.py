from typing import Optional

from fastapi import APIRouter, UploadFile, File, Form
from starlette import status
from starlette.responses import JSONResponse, Response

from ..repository.develop import DevelopRepository
from ..schemas.develop import SDevelopAdd, SDevelopId
from fastapi.responses import StreamingResponse

router = APIRouter(
    prefix="/develops",
    tags=["Develops"],
)


@router.post("/add_develop", response_model=SDevelopId, status_code=status.HTTP_200_OK)
async def add_develop(
    firstName: str = Form(...),
    lastName: Optional[str] = Form(None),
    aboutDevelop: Optional[str] = Form(None),
    description: Optional[str] = Form(None),
    photo: UploadFile = File(None),
) -> SDevelopId:
    develop = SDevelopAdd(
        firstName=firstName,
        lastName=lastName,
        aboutDevelop=aboutDevelop,
        description=description,
    )
    develop_id = await DevelopRepository.add_one(develop)

    photo_data = None
    if photo:
        photo_data = await photo.read()
        await DevelopRepository.add_photo(develop_id, photo_data)

    return SDevelopId(
        Add=True,
        develop_id=develop_id,
        photo=f"string({len(photo_data)})" if photo else None,
    )


@router.get("/{develop_id}/photo")
async def get_develop_photo(develop_id: int):
    photo_data = await DevelopRepository.get_photo(develop_id)

    if photo_data:
        return StreamingResponse(iter([photo_data]), media_type="image/jpeg")
    else:
        return {"error": "No photo available"}


@router.get("/{develop_id}")
async def get_develop_details(develop_id: int):
    develop_details = await DevelopRepository.get_develop_details(develop_id)
    if "error" in develop_details:
        return develop_details
    else:
        return develop_details


@router.delete("/{develop_id}", status_code=204)
async def delete_develop(develop_id: int):
    try:
        await DevelopRepository.delete_develop(develop_id)
    except ValueError as e:
        return JSONResponse(status_code=404, content={"error": str(e)})
    else:
        return Response(status_code=204)


@router.get("/")
async def get_all_develops():
    all_develops = await DevelopRepository.get_all_develops()
    return all_develops
