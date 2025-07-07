import sys
from loguru import logger
from typing import TypeVar
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import Response
from fastapi.routing import APIRoute
import logging

try:
    from opentelemetry import trace
except ImportError:
    trace = None

logging.getLogger("uvicorn.access").setLevel(logging.WARNING)


class LoguruRoute(APIRoute):
    def get_route_handler(self):
        original_route_handler = super().get_route_handler()

        async def custom_route_handler(request: Request) -> Response:
            response: Response = await original_route_handler(request)
            text = (
                f"{request.client.host}:{request.client.port} - "
                f'"{request.method} {request.url.path} '
                f"HTTP/{request.scope['http_version']}\" "
                f"{response.status_code}"
            )
            # Move "PING 200" to debug
            if not (request.url.path == "/ping" and response.status_code == 200):
                logger.info(text)
            else:
                logger.debug(text)
            return response

        return custom_route_handler


def level_filter(
    record: dict,
) -> bool:
    """
    Filters log messages withe log level lower
    than 'log_level'.
    Usage Example:
    --------------
    from logs import logger
    logger = logger.bind(log_level='DEBUG')
    """
    extra = record["extra"]
    extra_data = extra.get("extra", {})

    if trace is not None:
        span = trace.get_current_span()
        otel_span_id = trace.format_span_id(span.get_span_context().span_id)
        if otel_span_id != "0" * 16:
            extra_data["span_id"] = otel_span_id

        otel_trace_id = trace.format_trace_id(span.get_span_context().trace_id)
        if otel_trace_id != "0" * 32:
            extra_data["trace_id"] = otel_trace_id
    if not extra_data:
        if not extra or extra == {"extra": {}}:
            record["extra"] = ""

    log_level = extra.get("log_level")
    if log_level:
        return record["level"].no >= logger.level(log_level).no
    return True


TypeVarFastAPI = TypeVar("TypeVarFastAPI", bound=FastAPI)


def replace_log_handler(app: TypeVarFastAPI) -> TypeVarFastAPI:
    # Replace the logger in the FastAPI app
    app.router.route_class = LoguruRoute
    return app


# Remove default logger
logger.remove()

log_format = (
    "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> "
    "| {level} "
    "| <blue>{file.path}:{line}:</blue> {message}{extra}"
)
logger.add(
    sys.stderr,
    format=log_format,
    filter=level_filter,
    colorize=True,
    level="INFO",
)
