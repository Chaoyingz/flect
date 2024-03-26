from typing import Annotated, Any, Literal, Optional

from fastapi import Path, Request
from flect import PageResponse, display, form
from flect import components as c
from flect.actions import DispatchEvent
from flect.component import data_grid
from flect.constants import ROOT_ROUTE_PREFIX
from flect.head import Head
from flect.sitemap import Sitemap
from pydantic import BaseModel, Field

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
    column1: Annotated[str, display.TextDisplay(title="Column 1")]
    column2: str
    column3: str
    is_active: Annotated[bool, display.BooleanDisplay()]


class FormExampleModel(BaseModel):
    username: str = form.Input(
        placeholder="Enter your username", default="", pattern=r"^[a-zA-Z0-9]+$", min_items=2, max_items=10
    )
    gender: Literal["male", "female"] = form.Select(default="male", description="The gender of the user.")
    password: str = form.Input(type="password", default="", placeholder="Enter your password")
    hobby: Optional[str] = form.Textarea(
        placeholder="Type your hobby", default=None, description="The hobby of the user."
    )
    terms_accepted: bool = form.Checkbox(
        class_name="ml-3", default=False, description="The terms accepted by the user."
    )


class DataGridExampleRowModel(BaseModel):
    company_name: str = data_grid.Input(editable=False, default="flect", class_name="col-span-2")
    country: Literal[
        "Albania",
        "Andorra",
        "Armenia",
        "Austria",
        "Azerbaijan",
        "Belarus",
        "Belgium",
        "Bosnia and Herzegovina",
        "Bulgaria",
        "Croatia",
        "Cyprus",
        "Czech Republic",
        "Denmark",
        "Estonia",
        "Finland",
        "France",
        "Georgia",
        "Germany",
        "Greece",
        "Hungary",
        "Iceland",
        "Ireland",
        "Italy",
        "Kazakhstan",
        "Kosovo",
        "Latvia",
        "Liechtenstein",
        "Lithuania",
        "Luxembourg",
        "Malta",
        "Moldova",
        "Monaco",
        "Montenegro",
        "Netherlands",
        "North Macedonia",
        "Norway",
        "Poland",
        "Portugal",
        "Romania",
        "Russia",
        "San Marino",
        "Serbia",
        "Slovakia",
        "Slovenia",
        "Spain",
        "Sweden",
        "Switzerland",
        "Turkey",
        "Ukraine",
        "United Kingdom",
        "Vatican City",
    ] = data_grid.Combobox(class_name="col-span-3")
    gender: Literal["male", "female"] = data_grid.Select(class_name="col-span-2")
    name: str = data_grid.Input(pattern=r"^[a-zA-Z0-9]+$", min_items=2, max_items=10, class_name="col-span-4")


class DataGridExampleModel(BaseModel):
    rows: list[DataGridExampleRowModel] = Field(max_length=10)


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
    "data-grid": [
        get_component_description_section(
            title="DataGrid",
            description="The DataGrid component displays data in tabular format.",
        ),
        get_component_preview_section(
            preview=c.DataGrid(
                model=DataGridExampleModel, datasets=[], submit_url="/flect/components/data_grid/", class_name="p-3"
            ),
        ),
        get_api_reference_section(component=c.DataGrid),
    ],
    "deferred-fetch": [
        get_component_description_section(
            title="DeferredFetch",
            description="The DeferredFetch component provides an asynchronous API call.",
        ),
        get_component_preview_section(
            preview=c.Container(
                children=[
                    c.Text(text="This is a sample text in deferred fetch."),
                    c.Button(
                        children=[c.Text(text="Click me")],
                        on_click_action=DispatchEvent(event="deferred-fetch-button:click"),
                    ),
                    c.DeferredFetch(
                        path="/flect/components/deferred_fetch/",
                        trigger=DispatchEvent(event="deferred-fetch-button:click"),
                    ),
                ]
            )
        ),
    ],
    "dialog": [
        get_component_description_section(
            title="Dialog",
            description="A window overlaid on either the primary window or another dialog window, rendering the "
            "content underneath inert.",
        ),
        get_component_preview_section(
            preview=c.Container(
                tag="div",
                children=[
                    c.Text(text="This is a sample text in dialog."),
                    c.Button(
                        children=[c.Text(text="Open dialog")],
                        on_click_action=DispatchEvent(event="dialog:open"),
                    ),
                    c.Dialog(
                        title="Dialog",
                        children=[
                            c.Text(text="This is a sample text in dialog."),
                        ],
                        trigger=DispatchEvent(event="dialog:open"),
                    ),
                ],
            ),
        ),
        get_api_reference_section(component=c.Container),
    ],
    "display": [
        get_component_description_section(
            title="Display",
            description="The Display component displays other components.",
        ),
        get_component_preview_section(
            preview=c.Display(
                value='{"b": 1}',
            ),
        ),
        get_api_reference_section(component=c.Display),
    ],
    "form": [
        get_component_description_section(
            title="Form",
            description="The Form component collects user inputs through various form elements such as input fields, checkboxes, radio buttons, and dropdowns.",
        ),
        get_component_preview_section(
            preview=c.Form(model=FormExampleModel, submit_url="/flect/components/form/"),
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
    "paragraph": [
        get_component_description_section(
            title="Paragraph",
            description="The Paragraph component displays text.",
        ),
        get_component_preview_section(
            preview=c.Paragraph(
                text="Text, you can also use markdown link syntax here. example: [example](https://example.com).",
            )
        ),
        get_api_reference_section(component=c.Text),
    ],
    "table": [
        get_component_description_section(
            title="Table",
            description="The Table component displays data in a grid format with rows and columns.",
        ),
        get_component_preview_section(
            preview=c.Table(
                model=TableExampleModel,
                datasets=[
                    TableExampleModel(
                        column1="Value 1",
                        column2="Value 2",
                        column3="Value 3",
                        is_active=True,
                    ),
                    TableExampleModel(
                        column1="Value 4",
                        column2="Value 5",
                        column3="Value 6",
                        is_active=False,
                    ),
                ],
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
    component_elements = COMPONENT_DOCS_MAP.get(component_type, [c.Text(text="Unknown component type")])
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
                get_docs_pager(current_link=request.url.path.replace(ROOT_ROUTE_PREFIX, "")),
            ],
        ),
    )
