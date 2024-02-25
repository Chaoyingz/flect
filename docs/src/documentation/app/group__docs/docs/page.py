from starlette.concurrency import run_in_threadpool
from tui import PageResponse
from tui import components as c

from documentation import CONTENT_DIR


def get_readme_text() -> str:
    with open(CONTENT_DIR / "introduction.md") as f:
        return f.read()


async def page() -> PageResponse:
    readme_text = await run_in_threadpool(get_readme_text)
    return PageResponse(
        element=c.Container(
            tag="div",
            children=[
                c.Markdown(
                    text=readme_text,
                )
            ],
        )
    )
