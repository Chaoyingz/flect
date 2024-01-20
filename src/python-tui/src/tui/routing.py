from collections.abc import Awaitable
from typing import Any, Callable

from fastapi import APIRouter
from fastapi.types import DecoratedCallable

from tui import components as c

Layout = Callable[[list[c.AnyComponent]], Awaitable[c.AnyComponent]]


class LayoutRouter(APIRouter):
    def __init__(self, layout: Layout, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.layout = layout

    def api_route(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            async def page():
                return await self.layout(await func())

            self.add_api_route(path, page, **kwargs)
            return page

        return decorator
