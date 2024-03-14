import asyncio
import pathlib
import signal
from contextlib import asynccontextmanager
from types import ModuleType
from typing import Any, Optional

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from flect.routing import configure_app_router


class flect(FastAPI):
    def __init__(
        self,
        app: ModuleType,
        prebuilt_uri: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        self.default_lifespan = kwargs.pop("lifespan", None)
        super().__init__(**kwargs, lifespan=self.lifespan)
        self.app_module = app
        self.prebuilt_uri = self.validate_prebuilt_uri(prebuilt_uri)
        self.reload_event = asyncio.Event()
        self.setup_flect()

    def setup_flect(self) -> None:
        app_router = configure_app_router(self.app_module, self.prebuilt_uri)
        if self.debug:
            self.add_api_route("/_hotreload", self.hotreload, methods=["GET"])
        self.include_router(app_router, tags=["flect"])

    def validate_prebuilt_uri(self, prebuilt_uri: Optional[str]) -> Optional[str]:
        if prebuilt_uri is not None:
            if not prebuilt_uri.startswith("http"):
                self.mount("/static", StaticFiles(directory=pathlib.Path(prebuilt_uri)), name="static")
                prebuilt_uri = "/static"
        return prebuilt_uri

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        signal.signal(signal.SIGTERM, self.on_sigterm)
        if self.default_lifespan:
            async with self.default_lifespan(app):
                yield
        else:
            yield

    def on_sigterm(self, *_: Any) -> None:
        self.reload_event.set()

    async def hotreload(self) -> StreamingResponse:
        async def event_generator():
            try:
                while True:
                    try:
                        await asyncio.wait_for(self.reload_event.wait(), timeout=5.0)
                        yield "data: reload\n\n"
                        self.reload_event.clear()
                    except (asyncio.TimeoutError, asyncio.exceptions.CancelledError):
                        pass
            except Exception:
                pass

        return StreamingResponse(event_generator(), media_type="text/event-stream")
