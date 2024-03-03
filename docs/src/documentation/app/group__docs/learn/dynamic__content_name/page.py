from typing import Annotated

from fastapi import Path
from starlette.concurrency import run_in_threadpool
from tui import PageResponse
from tui import components as c

from documentation.utils import get_markdown_content


async def page(
    content_name: Annotated[str, Path(..., description="The content name to render")],
) -> PageResponse:
    try:
        readme_text = await run_in_threadpool(get_markdown_content, f"{content_name}.md")
    except FileNotFoundError:
        readme_text = "Content not found"
    return PageResponse(
        element=c.Container(
            tag="div",
            children=[
                c.Markdown(
                    text=readme_text,
                ),
                # c.Container(
                #     tag="div",
                #     class_name="mt-10 flex",
                #     children=[
                #         c.Link(
                #             href=f"/docs/introduction/",
                #             children=[c.Button(children="< Introduction", variant="outline", size="sm")],
                #         )
                #     ],
                # ),
            ],
        )
    )
