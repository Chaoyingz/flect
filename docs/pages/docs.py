from fastapi import APIRouter
from tui import apply_layout
from tui import components as c

from docs.layouts.docs_layout import docs_layout

docs_router = APIRouter()


@docs_router.get("/docs")
@apply_layout(docs_layout)
async def docs_page() -> c.AnyComponents:
    return [
        c.Heading(
            level=1,
            text="Introduction",
            className="text-3xl mb-3",
        ),
        c.Text(
            text="In the backend, use Pydantic models that match the props of frontend React "
            "components. This allows you to create beautiful, interactive UIs use Python.",
            className="text-lg",
        ),
        c.Container(
            className="mt-3",
            children=[
                c.Text(
                    text="tui is a project inspired by FastUI, designed to simplify and accelerate web application "
                    "development. It is built on the powerful combination of FastAPI for backend efficiency and "
                    "Shadcn UI for creating stylish and responsive user interfaces.",
                    className="text-lg mt-3",
                )
            ],
        ),
    ]
