from fastapi import APIRouter
from tui import apply_layout
from tui import components as c

from docs.layouts.root_layout import root_layout

landing_router = APIRouter()


@landing_router.get(path="/")
@apply_layout(root_layout)
async def landing_page() -> c.AnyComponents:
    return [
        c.Container(
            tag="section",
            class_name="container",
            children=[
                c.Container(
                    tag="section",
                    class_name="flex justify-center py-28 flex-col items-center",
                    children=[
                        c.Heading(
                            level=1, text="Turning ideas into web app fast", class_name="text-center text-5xl font-bold"
                        ),
                        c.Text(
                            text="In the backend, use Pydantic models that match the props of frontend React "
                            "components. This allows you to create beautiful, interactive UIs using Python.",
                            class_name="text-center text-xl mt-8 w-1/2",
                        ),
                        c.Container(
                            tag="div",
                            class_name="flex gap-4 mt-8",
                            children=[
                                c.Link(
                                    href="/docs",
                                    children=[
                                        c.Button(
                                            children="Get Started",
                                        )
                                    ],
                                ),
                                c.Link(
                                    href="https://github.com/Chaoyingz/tui",
                                    children=[
                                        c.Button(
                                            children="GitHub",
                                            variant="outline",
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )
    ]
