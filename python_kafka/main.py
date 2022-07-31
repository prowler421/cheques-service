import threading

from . import api
from .kafka.admin import create_kafka_topics
from .kafka.consumer import from_kafka
import asyncio

from .utils.logger import get_logger

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

logger = get_logger(logname=__name__)
app = FastAPI()


async def invoke_kafka_consumer():
    await from_kafka()


def invoke_callbacks():
    logger.info("initializing kafka consumer...")
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    loop.run_until_complete(invoke_kafka_consumer())
    loop.close()


origins = [
    "http://localhost.tiangolo.com",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:8080",
    "*"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["DELETE", "GET", "POST", "PUT"],
    allow_headers=["*"],
)


@app.on_event("startup")
async def startup_event():
    logger.info("initializing kafka services...")
    await create_kafka_topics()

    thread = threading.Thread(target=invoke_callbacks)
    thread.start()


app.include_router(api.router, tags=["cheques"])
