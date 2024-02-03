from types import ModuleType
from typing import Any

from fastapi import FastAPI

from tui.routing import get_router


class tui(FastAPI):
    def __init__(self, app_module: ModuleType, *args: Any, **kwargs: Any):
        super().__init__(docs_url=None, redoc_url=None, *args, **kwargs)
        self.setup_tui(app_module)

    def setup_tui(self, app_module: ModuleType) -> None:
        router = get_router(app_module)
        self.include_router(router)
