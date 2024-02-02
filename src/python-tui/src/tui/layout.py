import functools
from collections.abc import Awaitable
from typing import Any, Callable

from tui import components as c

LayoutCallable = Callable[[list[c.AnyComponent]], Awaitable[list[c.AnyComponent]]]


def apply_layout(layout: LayoutCallable) -> Callable:
    def wrapper(func: Callable) -> Callable:
        @functools.wraps(func)
        async def decorated(*args: Any, **kwargs: Any) -> list[c.AnyComponent]:
            children = await func(*args, **kwargs)
            return await layout(children)

        return decorated

    return wrapper
