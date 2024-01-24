from fastapi import APIRouter, FastAPI
from tui import init_tui

from docs.pages.components import components_router
from docs.pages.docs import docs_router
from docs.pages.landing import landing_router

tui_router = APIRouter(prefix="/api")
tui_router.include_router(landing_router)
tui_router.include_router(docs_router)
tui_router.include_router(components_router)


def get_application() -> FastAPI:
    application = FastAPI(docs_url="/documentation")
    application.include_router(tui_router)
    return application


app = get_application()
init_tui(app)
