from contextlib import asynccontextmanager

from fastapi import FastAPI

from src.base_settings import base_settings
from src.common.databases.postgres import postgres


@asynccontextmanager
async def lifespan(app: FastAPI):
    postgres.connect(base_settings.postgres.url)
    yield
    await postgres.disconnect()


def get_application():
    application = FastAPI(
        debug=True,
        lifespan=lifespan,
    )
    return application


app = get_application()

