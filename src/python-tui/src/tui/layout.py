import functools
import typing as _t

from tui import components as c

LayoutCallable = _t.Callable[[list[c.AnyComponent]], _t.Awaitable[list[c.AnyComponent]]]


def apply_layout(layout: LayoutCallable) -> _t.Callable:
    def wrapper(func: _t.Callable) -> _t.Callable:
        @functools.wraps(func)
        async def decorated(*args: _t.Any, **kwargs: _t.Any) -> list[c.AnyComponent]:
            children = await func(*args, **kwargs)
            return await layout(children)

        return decorated

    return wrapper
