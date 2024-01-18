from docs.components.site_header import site_header
from tui import components as c


def root_layout(children: list[c.AnyComponent]) -> list[c.AnyComponent]:
    return [
        site_header(),
        c.Container(
            tag="main",
            className="container",
            components=children
        )
    ]
