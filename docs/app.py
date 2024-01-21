from fastapi import FastAPI
from tui import init_tui

from docs.pages.landing import router


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(router)
    init_tui(application)
    return application


app = get_application()
