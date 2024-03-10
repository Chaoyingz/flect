from typing import Annotated

import flect.actions as a
import flect.components as c
from fastapi import Path, Request
from flect import PageResponse
from flect.head import Head
from flect.routing import CLIENT_ROOT_ROUTER_PREFIX
from flect.sitemap import Sitemap

from documentation.app.group__docs.component import get_api_reference_section
from documentation.app.group__docs.layout import get_docs_pager

ACTION_DOCS_MAP = {
    "notify": [
        c.Container(
            children=[
                c.Heading(
                    level=1,
                    text="Notify",
                    class_name="text-3xl mb-3",
                ),
                c.Paragraph(text="The Notify action is used to show a notification with a title and a description."),
            ]
        ),
        c.Container(
            children=[
                c.Heading(
                    level=2,
                    text="Try it out",
                    class_name="text-2xl mb-6 border-b pb-2",
                ),
                c.Button(
                    on_click_action=a.Notify(
                        title="Button clicked",
                        description="The button was clicked",
                    ),
                    children=[
                        c.Text(
                            text="Click me",
                        )
                    ],
                ),
            ]
        ),
        get_api_reference_section(a.Notify),
    ],
    "redirect": [
        c.Container(
            children=[
                c.Heading(
                    level=1,
                    text="Notify",
                    class_name="text-3xl mb-3",
                ),
                c.Paragraph(text="The Redirect action is used to navigate to a different URL."),
            ]
        ),
        c.Container(
            children=[
                c.Heading(
                    level=2,
                    text="Try it out",
                    class_name="text-2xl mb-6 border-b pb-2",
                ),
                c.Button(
                    on_click_action=a.Redirect(url="/actions/notify/"),
                    children=[
                        c.Text(
                            text="Click button will redirect to /actions/notify/",
                        )
                    ],
                ),
            ]
        ),
        get_api_reference_section(a.Redirect),
    ],
}


async def sitemap(dynamic_url: str) -> list[Sitemap]:
    return [
        Sitemap(
            url=dynamic_url.format(action_type=action_type),
            last_modified=None,
            change_frequency=None,
            priority=None,
        )
        for action_type in ACTION_DOCS_MAP
    ]


async def page(
    request: Request,
    action_type: Annotated[str, Path(..., description="The action type to render")],
) -> PageResponse:
    component_elements = ACTION_DOCS_MAP.get(action_type, c.Text(text="Unknown action"))
    return PageResponse(
        head=Head(
            title=f"{action_type} action",
            description=f"{action_type} action",
        ),
        body=c.Container(
            tag="div",
            class_name="flex gap-12 flex-col",
            children=[
                *component_elements,
                get_docs_pager(current_link=request.url.path.replace(CLIENT_ROOT_ROUTER_PREFIX, "")),
            ],
        ),
    )
