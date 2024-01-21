from fastapi import APIRouter, FastAPI
from tui import init_tui

from docs.pages.docs import docs_router
from docs.pages.landing import landing_router

tui_router = APIRouter(prefix="/api")
tui_router.include_router(landing_router)
tui_router.include_router(docs_router)


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(tui_router)
    init_tui(application)
    return application


app = get_application()
