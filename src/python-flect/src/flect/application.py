import asyncio
import pathlib
import signal
from contextlib import asynccontextmanager
from types import ModuleType
from typing import Any, cast

from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles

from flect.constants import CUSTOM_COMPONENT_MOUNT_FOLDER_NAME, CUSTOM_COMPONENT_STATIC_FOLDER_NAME
from flect.routing import configure_app_router

STATIC_FILE_PATH = pathlib.Path(__file__).parent.parent / "static"


class flect(FastAPI):
    def __init__(
        self,
        app: ModuleType,
        **kwargs: Any,
    ) -> None:
        self.default_lifespan = kwargs.pop("lifespan", None)
        super().__init__(**kwargs, lifespan=self.lifespan)
        self.app_module = app
        self.reload_event = asyncio.Event()
        self.setup_flect()

    def setup_flect(self) -> None:
        app_router = configure_app_router(self.app_module)
        self.mount("/static", StaticFiles(directory=STATIC_FILE_PATH), name="static")
        self.mount_custom_components()
        if self.debug:
            self.add_api_route("/_hotreload", self.hotreload, methods=["GET"])
        self.include_router(app_router, tags=["flect"])

    def mount_custom_components(self) -> None:
        custom_component_dir = (
            pathlib.Path(cast(str, self.app_module.__file__)).parent.parent.parent.parent
            / CUSTOM_COMPONENT_STATIC_FOLDER_NAME
        )
        if custom_component_dir.exists():
            self.mount(
                f"/{CUSTOM_COMPONENT_MOUNT_FOLDER_NAME}",
                StaticFiles(directory=custom_component_dir),
                name=CUSTOM_COMPONENT_MOUNT_FOLDER_NAME,
            )

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
                    except asyncio.TimeoutError:
                        pass
            except Exception:
                pass

        return StreamingResponse(event_generator(), media_type="text/event-stream")
