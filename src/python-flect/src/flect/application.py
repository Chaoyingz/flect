import asyncio
import pathlib
from types import ModuleType
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from flect.routing.server import get_app_router


class flect(FastAPI):
    def __init__(
        self,
        app: ModuleType,
        prebuilt_uri: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        super().__init__(**kwargs)
        self.app_module = app
        self.prebuilt_uri = self.validate_prebuilt_uri(prebuilt_uri)
        self.reload_event = asyncio.Event()
        self.setup_flect()

    def setup_flect(self) -> None:
        self.include_router(get_app_router(self.app_module, self.prebuilt_uri), tags=["flect"])

    def validate_prebuilt_uri(self, prebuilt_uri: Optional[str]) -> Optional[str]:
        if prebuilt_uri is not None:
            if not prebuilt_uri.startswith("http"):
                self.mount("/static", StaticFiles(directory=pathlib.Path(prebuilt_uri)), name="static")
                prebuilt_uri = "/static"
        return prebuilt_uri
