from tui import PageResponse
from tui import components as c


async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(
        element=c.Container(
            tag="main",
            children=[
                outlet,
            ],
        )
    )
