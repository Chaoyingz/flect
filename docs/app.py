from fastapi import FastAPI

from docs.routes import root_layout_router
from tui import init_tui


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(root_layout_router)
    init_tui(application)
    return application


app = get_application()
