from fastapi import FastAPI

from contextlib import asynccontextmanager

from fastapi.middleware.cors import CORSMiddleware

from ..database.database import create_tables
from ..router.client import router as client
from ..router.develop import router as develop


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_tables()
    yield


origins = ["*"]


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(client)
app.include_router(develop)
