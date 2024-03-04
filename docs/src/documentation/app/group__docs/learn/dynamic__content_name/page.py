from typing import Annotated

from fastapi import Path
from flect import PageResponse
from flect import components as c
from flect.sitemap import Sitemap

from documentation import CONTENT_DIR


async def sitemap(dynamic_url: str) -> list[Sitemap]:
    return [
        Sitemap(
            url=dynamic_url.format(content_name=content_name),
            last_modified=None,
            change_frequency=None,
            priority=None,
        )
        for content_name in ["project-structure", "routing", "form"]
    ]


async def page(
    content_name: Annotated[str, Path(..., description="The content name to render")],
) -> PageResponse:
    return PageResponse(
        element=c.Container(
            tag="div",
            children=[
                c.Markdown.from_file(CONTENT_DIR / f"{content_name}.md"),
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
