from pydantic import Field
from pydantic_settings import BaseSettings


class Service(BaseSettings):
    host: str
    port: int


class TEIService(Service):
    host: str = Field(
        default=None,
        validation_alias="EMBEDDINGS_HOST",
        description="Text embeddings inference service host name or IP address.",
    )
    port: int = Field(
        default=None,
        validation_alias="EMBEDDINGS_PORT",
        description="Text embeddings inference service port number.",
    )
