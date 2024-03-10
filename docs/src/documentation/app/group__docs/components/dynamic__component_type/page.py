from typing import Annotated, Any, Literal, Optional

import flect.components as c
from fastapi import Path, Request
from flect import PageResponse
from flect.form import Checkbox, Input, Select, Textarea
from flect.head import Head
from flect.routing import CLIENT_ROOT_ROUTER_PREFIX
from flect.sitemap import Sitemap
from pydantic import BaseModel

from documentation.app.group__docs.component import get_api_reference_section
from documentation.app.group__docs.layout import get_docs_pager


def get_component_description_section(
    title: str,
    description: str,
) -> c.Container:
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=1,
                text=title,
                class_name="text-3xl mb-3",
            ),
            c.Text(text=description),
        ],
    )


def get_component_preview_literal_component(
    component_type: c.AnyComponent,
    literal_props: list[str],
    dynamic_props: list[str],
    default_props_values: dict[str, Any],
) -> c.Container:
    return c.Container(
        tag="div",
        class_name="flex flex-col gap-10",
        children=[
            c.Container(
                tag="div",
                children=[
                    c.Heading(
                        level=3,
                        text=literal_prop,
                    ),
                    c.Container(
                        tag="div",
                        class_name="flex gap-4 mt-3",
                        children=[
                            component_type(
                                **{
                                    literal_prop: literal_value,
                                    **{dp: [c.Text(text=literal_value)] for dp in dynamic_props},
                                    **default_props_values,
                                }
                            )
                            for literal_value in component_type.__annotations__[literal_prop].__args__
                        ],
                    ),
                ],
            )
            for literal_prop in literal_props
        ],
    )


def get_component_preview_section(
    preview: c.AnyComponent,
) -> c.AnyComponent:
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=2,
                text="Preview",
                class_name="text-2xl mb-6 border-b pb-2",
            ),
            preview,
        ],
    )


class TableExampleModel(BaseModel):
    column1: str
    column2: str
    column3: str


class FormExampleModel(BaseModel):
    username: str = Input(placeholder="Enter your username", pattern=r"^[a-zA-Z0-9]+$", min_items=2, max_items=10)
    gender: Literal["male", "female"] = Select(default="male", description="The gender of the user.")
    password: str = Input(type="password", placeholder="Enter your password")
    hobby: Optional[str] = Textarea(placeholder="Type your hobby", default=None, description="The hobby of the user.")
    terms_accepted: bool = Checkbox(class_name="ml-3", default=False, description="The terms accepted by the user.")


COMPONENT_DOCS_MAP = {
    "avatar": [
        get_component_description_section(
            title="Avatar",
            description="The Avatar component visually represents a user or a group of users.",
        ),
        get_component_preview_section(
            preview=c.Container(
                tag="div",
                class_name="flex gap-3",
                children=[
                    c.Avatar(
                        src="https://github.com/shadcn.png",
                        alt="@shadcn",
                        fallback="CN",
                    ),
                    c.Avatar(
                        fallback="CN",
                    ),
                ],
            )
        ),
        get_api_reference_section(component=c.Avatar),
    ],
    "button": [
        get_component_description_section(
            title="Button",
            description="The Button component triggers a defined action. Button labels should clearly indicate the action that will be performed upon interaction.",
        ),
        get_component_preview_section(
            preview=get_component_preview_literal_component(
                component_type=c.Button,
                literal_props=["variant", "size"],
                dynamic_props=["children"],
                default_props_values={},
            )
        ),
        get_api_reference_section(component=c.Button),
    ],
    "code-block": [
        get_component_description_section(
            title="CodeBlock",
            description="The CodeBlock component displays blocks of code.",
        ),
        get_component_preview_section(
            preview=c.CodeBlock(text="print('Hello, World!')"),
        ),
        get_api_reference_section(component=c.CodeBlock),
    ],
    "container": [
        get_component_description_section(
            title="Container",
            description="The Container component serves as a wrapper for other components.",
        ),
        get_component_preview_section(
            preview=c.Container(
                tag="div",
                children=[
                    c.Text(text="This is a sample text in container."),
                ],
            ),
        ),
        get_api_reference_section(component=c.Container),
    ],
    "form": [
        get_component_description_section(
            title="Form",
            description="The Form component collects user inputs through various form elements such as input fields, checkboxes, radio buttons, and dropdowns.",
        ),
        get_component_preview_section(
            preview=c.Form(model=FormExampleModel, submit_url="/components/form/"),
        ),
        get_api_reference_section(component=c.Form),
    ],
    "heading": [
        get_component_description_section(
            title="Heading",
            description="The Heading component displays section headings.",
        ),
        get_component_preview_section(
            preview=c.Heading(
                level=2,
                text="Heading",
            )
        ),
        get_api_reference_section(component=c.Heading),
    ],
    "link": [
        get_component_description_section(
            title="Link",
            description="The Link component creates navigation links.",
        ),
        get_component_preview_section(
            preview=get_component_preview_literal_component(
                component_type=c.Link,
                literal_props=["underline", "target"],
                dynamic_props=["children"],
                default_props_values={
                    "href": "/components/link/",
                },
            )
        ),
        get_api_reference_section(component=c.Link),
    ],
    "markdown": [
        get_component_description_section(
            title="Markdown",
            description="The Markdown component renders text in markdown format.",
        ),
        get_component_preview_section(
            preview=c.Markdown(
                text="## Markdown\n\nThis is a sample markdown text.\n\n- Item 1\n- Item 2\n- Item 3",
            )
        ),
        get_api_reference_section(component=c.Markdown),
    ],
    "table": [
        get_component_description_section(
            title="Table",
            description="The Table component displays data in a grid format with rows and columns.",
        ),
        get_component_preview_section(
            preview=c.Table(
                datasets=[
                    TableExampleModel(
                        column1="Value 1",
                        column2="Value 2",
                        column3="Value 3",
                    ),
                    TableExampleModel(
                        column1="Value 4",
                        column2="Value 5",
                        column3="Value 6",
                    ),
                ]
            )
        ),
        get_api_reference_section(component=c.Table),
    ],
    "text": [
        get_component_description_section(
            title="Text",
            description="The Text component displays a string of text.",
        ),
        get_component_preview_section(
            preview=c.Text(
                text="Text",
            )
        ),
        get_api_reference_section(component=c.Text),
    ],
}


async def sitemap(dynamic_url: str) -> list[Sitemap]:
    return [
        Sitemap(
            url=dynamic_url.format(component_type=component_type),
            last_modified=None,
            change_frequency=None,
            priority=None,
        )
        for component_type in COMPONENT_DOCS_MAP
    ]


async def page(
    request: Request,
    component_type: Annotated[str, Path(..., description="The component type to render")],
) -> PageResponse:
    component_elements = COMPONENT_DOCS_MAP.get(component_type, c.Text(text="Unknown component type"))
    return PageResponse(
        head=Head(
            title=f"{component_type} component",
            description=f"{component_type} component",
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
