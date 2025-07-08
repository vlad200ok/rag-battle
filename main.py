import os
import sys
import uvloop
import uvicorn
import subprocess
from loguru import logger
from typing import Literal
from pydantic import BaseModel

uvloop.install()


# TODO: change to BaseSettings
class ServerConfig(BaseModel):
    port: int = int(os.getenv("PORT"))
    server: Literal[
        "uvicorn",
        "gunicorn",
        "opentelemetry",
    ] = os.getenv("SERVER")
    alembic: bool = bool(int(os.getenv("ALEMBIC", 0)))
    reload: bool = bool(int(os.getenv("RELOAD")))
    workers: int = int(os.getenv("WORKERS"))
    gunicorn_timeout: int = int(os.getenv("GUNICORN_TIMEOUT"))
    timeout_keep_alive: int = int(os.getenv("TIMEOUT_KEEP_ALIVE", 600))


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
