import pathlib
from types import ModuleType
from typing import Any

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from tui.routing import configure_app_router

STATIC_FILE_PATH = pathlib.Path(__file__).parent.parent / "static"


class tui(FastAPI):
    def __init__(
        self,
        app: ModuleType,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.app = app
        self.setup_tui()

    def setup_tui(self) -> None:
        app_router = configure_app_router(self.app)
        self.mount("/static", StaticFiles(directory=STATIC_FILE_PATH), name="static")
        self.include_router(app_router, tags=["tui"])
