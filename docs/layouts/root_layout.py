from tui import components as c

from docs.components.site_header import site_header


async def root_layout(children: list[c.AnyComponent]) -> list[c.AnyComponent]:
    return [await site_header(), c.Container(tag="main", className="container", components=children)]
