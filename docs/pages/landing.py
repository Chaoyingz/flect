from fastapi import APIRouter
from tui import apply_layout
from tui import components as c

from docs.layouts.root_layout import root_layout

router = APIRouter(
    prefix="/api",
)


@router.get(path="/")
@apply_layout(root_layout)
async def landing_page() -> list[c.AnyComponent]:
    return [
        c.Container(
            tag="section",
            className="container",
            children=[
                c.Heading(
                    level=1,
                    text="Turning ideas into web app fast.",
                )
            ],
        )
    ]
