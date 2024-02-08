from types import ModuleType
from typing import Any

from fastapi import FastAPI

from tui.routing import configure_app_router


class Tui(FastAPI):
    def __init__(
        self,
        app: ModuleType,
        **kwargs: Any,
    ) -> None:
        kwargs.update({"docs_url": None, "redoc_url": None})
        super().__init__(**kwargs)
        self.app = app
        self.setup_tui()

    def setup_tui(self) -> None:
        app_router = configure_app_router(self.app)
        self.include_router(app_router)
