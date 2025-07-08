import sys
import uvloop
import uvicorn
import subprocess
from loguru import logger
from typing import Literal
from pydantic import Field
from pydantic_settings import BaseSettings

uvloop.install()


class ServerConfig(BaseSettings):
    port: int = Field(
        default=None,
        validation_alias="PORT",
        description="Server port.",
    )
    server: Literal[
        "uvicorn",
        "gunicorn",
        "opentelemetry",
    ] = Field(
        default=None,
        validation_alias="SERVER",
        description="Server type. One of uvicorn, gunicorn, opentelemetry.",
    )
    alembic: bool = Field(
        default=None,
        validation_alias="ALEMBIC",
        description="Whether or not to run alembic migrations.",
    )
    reload: bool = Field(
        default=None,
        validation_alias="RELOAD",
        description="Whether or not to reload the server on code changes.",
    )
    workers: int = Field(
        default=None,
        validation_alias="WORKERS",
        description="Number of workers to use for the server.",
    )
    gunicorn_timeout: int = Field(
        default=None,
        validation_alias="GUNICORN_TIMEOUT",
        description="Timeout for gunicorn.",
    )
    timeout_keep_alive: int = Field(
        default=600,
        validation_alias="TIMEOUT_KEEP_ALIVE",
        description="Timeout for keep alive connections.",
    )


def run_alembic_migrations(path: str | None = None):
    if path is not None:
        command = ["bash", "-c", f"cd {path} && alembic upgrade head"]
    else:
        command = ["alembic", "upgrade", "head"]
    result = subprocess.run(command, check=True)
    logger.info(result)


def main(
    root_path: str = ".",
    alembic_path: str | None = None,
    config: ServerConfig | None = None,
):
    if root_path:
        if root_path == ".":
            app_path = "server:app"
        else:
            app_path = f"{root_path}.server:app"
    else:
        app_path = "server:app"

    if config is None:
        config = ServerConfig()
    logger.info(f"ServerConfig: {config}")

    if config.alembic:
        run_alembic_migrations(alembic_path)

    server = config.server

    if server == "uvicorn":
        uvicorn.run(
            app_path,
            host="0.0.0.0",
            port=config.port,
            reload=config.reload,
            forwarded_allow_ips="*",
            timeout_keep_alive=config.timeout_keep_alive,
        )
    elif server == "gunicorn":
        command = [
            "gunicorn",
            app_path,
            "--workers",
            f"{config.workers}",  # without converting to str subprocess raises error
            "--worker-class",
            "uvicorn.workers.UvicornWorker",
            "--forwarded-allow-ips",
            "*",
            "--bind",
            f"0.0.0.0:{config.port}",
            "--timeout",
            f"{config.gunicorn_timeout}",
        ]
        if config.reload:
            command.append("--reload")
        subprocess.run(command, check=True)
    elif server == "opentelemetry":
        command = [
            "opentelemetry-instrument",
            "gunicorn",
            app_path,
            "--workers",
            f"{config.workers}",  # without converting to str subprocess raises error
            "--worker-class",
            "uvicorn.workers.UvicornWorker",
            "--forwarded-allow-ips",
            "*",
            "--bind",
            f"0.0.0.0:{config.port}",
            "--timeout",
            f"{config.gunicorn_timeout}",
        ]
        if config.reload:
            command.append("--reload")
        subprocess.run(command, check=True)
    else:
        logger.info(f"Unknown server: {server}")
        sys.exit(1)


if __name__ == "__main__":
    main("rag_battle")
