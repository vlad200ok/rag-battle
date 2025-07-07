import os

from pydantic import BaseModel


class Service(BaseModel):
    host: str
    port: int


class TEIService(Service):
    host: str = os.getenv("EMBEDDINGS_HOST")
    port: int = int(os.getenv("EMBEDDINGS_PORT"))
