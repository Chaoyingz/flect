from typing import Annotated

from fastapi import Path, Request
from flect import PageResponse
from flect import components as c
from flect.routing import CLIENT_ROOT_ROUTER_PREFIX
from flect.sitemap import Sitemap

from documentation import CONTENT_DIR
from documentation.app.group__docs.layout import get_docs_pager


async def sitemap(dynamic_url: str) -> list[Sitemap]:
    return [
        Sitemap(
            url=dynamic_url.format(content_name=content_name),
            last_modified=None,
            change_frequency=None,
            priority=None,
        )
        for content_name in ["introduction", "installation", "tutorial"]
    ]


async def page(
    request: Request,
    content_name: Annotated[str, Path(..., description="The content name to render")],
) -> PageResponse:
    return PageResponse(
        element=c.Container(
            tag="div",
            children=[
                c.Markdown.from_file(CONTENT_DIR / f"{content_name}.md"),
                get_docs_pager(current_link=request.url.path.replace(CLIENT_ROOT_ROUTER_PREFIX, "")),
            ],
        )
    )
