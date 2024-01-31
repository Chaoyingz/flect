from tui import components as c

from docs.components.site_header import site_header


async def root_layout(children: c.AnyComponents) -> c.AnyComponents:
    layout = [await site_header(), c.Container(tag="main", class_name="container", children=children)]
    return layout
