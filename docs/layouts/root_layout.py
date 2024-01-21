import functools

from tui import components as c

from docs.components.site_header import site_header


def root_layout(func):
    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        children = await func(*args, **kwargs)
        layout = [await site_header(), c.Container(tag="main", className="container", children=children)]
        return layout

    return wrapper
