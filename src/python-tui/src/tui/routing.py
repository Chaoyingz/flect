from typing import Any, Callable

from fastapi import APIRouter
from fastapi.types import DecoratedCallable

from tui import components as c


class LayoutRouter(APIRouter):
    def __init__(
        self, layout: Callable[[list[c.AnyComponent]], list[c.AnyComponent]], *args: Any, **kwargs: Any
    ) -> None:
        super().__init__(*args, **kwargs)
        self.layout: Callable[[list[c.AnyComponent]], list[c.AnyComponent]] = layout

    def api_route(self, path: str, *args: Any, **kwargs: Any) -> Callable[[DecoratedCallable], DecoratedCallable]:
        def decorator(func: DecoratedCallable) -> DecoratedCallable:
            async def f():
                return self.layout(children=await func())

            self.add_api_route(path, f, **kwargs)
            return f

        return decorator
