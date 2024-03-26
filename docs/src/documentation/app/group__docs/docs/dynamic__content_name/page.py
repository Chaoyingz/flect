from typing import Annotated

from fastapi import Path, Request
from flect import PageResponse
from flect import components as c
from flect.constants import ROOT_ROUTE_PREFIX
from flect.head import Head
from flect.sitemap import Sitemap

from documentation import CONTENT_DIR
from documentation.app.group__docs.layout import get_docs_pager
from documentation.components import Markdown


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
        head=Head(
            title=content_name,
        ),
        body=c.Container(
            tag="div",
            children=[
                Markdown.from_file(CONTENT_DIR / f"{content_name}.md"),
                get_docs_pager(current_link=request.url.path.replace(ROOT_ROUTE_PREFIX, "")),
            ],
        ),
    )
