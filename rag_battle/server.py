from fastapi import FastAPI

from rag_battle import __version__
from rag_battle.routers import v1_router
from rag_battle.logs import replace_log_handler


app = FastAPI(
    title="RAG battle.",
    version=__version__,
    redoc_url=None,
)

app = replace_log_handler(app)
app.include_router(v1_router, prefix="/v1")


@app.get("/ping")
def ping():
    return 0
