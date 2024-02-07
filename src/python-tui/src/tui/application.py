from types import ModuleType
from typing import Any

from fastapi import FastAPI

from tui.routing import get_app_router


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
        self.include_router(get_app_router(self.app))
