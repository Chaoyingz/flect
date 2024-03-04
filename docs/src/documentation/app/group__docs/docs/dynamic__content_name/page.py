from typing import Annotated

from fastapi import Path
from flect import PageResponse
from flect import components as c
from flect.sitemap import Sitemap
from starlette.concurrency import run_in_threadpool

from documentation.utils import get_markdown_content


async def sitemap(dynamic_url: str) -> list[Sitemap]:
    return [
        Sitemap(
            url=dynamic_url.format(content_name=content_name),
            last_modified=None,
            change_frequency=None,
            priority=None,
        )
        for content_name in ["introduction", "installation", "project-structure"]
    ]


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
