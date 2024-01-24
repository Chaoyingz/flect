from typing import Any, Optional

from fastapi import APIRouter
from pydantic import BaseModel
from pydantic_core._pydantic_core import PydanticUndefined
from tui import apply_layout
from tui import components as c

from docs.layouts.docs_layout import docs_layout

components_router = APIRouter(prefix="/components")


async def get_component_description_section(
    title: str,
    description: str,
) -> c.Container:
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=1,
                text=title,
                className="text-3xl mb-3",
            ),
            c.Text(text=description),
        ],
    )


class ComponentProps(BaseModel):
    prop: str
    type: str
    default: Optional[str]
    description: Optional[str]


async def get_component_preview_literal_component(
    component_type: c.AnyComponent,
    literal_props: list[str],
    dynamic_props: list[str],
    default_props_values: dict[str, Any],
) -> c.Container:
    return c.Container(
        tag="div",
        className="flex flex-col gap-10",
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
                        className="flex gap-4 mt-3",
                        children=[
                            component_type(
                                **{
                                    literal_prop: literal_value,
                                    **{dp: literal_value for dp in dynamic_props},
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


async def get_component_preview_section(
    previews: c.AnyComponents,
) -> c.AnyComponent:
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=2,
                text="Preview",
                className="text-2xl mb-6 border-b pb-2",
            ),
            *previews,
        ],
    )


async def get_component_api_reference_section(component: c.AnyComponent) -> c.Container:
    props = []
    for field, filed_info in component.model_fields.items():
        if field == "ctype":
            continue
        if field == "children":
            filed_info.annotation = "tui.components.AnyComponents"
            filed_info.default = "[]"
            filed_info.description = "The children of the component."
        if filed_info.default == PydanticUndefined:
            filed_info.default = "-"
        props.append(
            ComponentProps(
                prop=field,
                type=str(filed_info.annotation),
                default=filed_info.default or "-",
                description=filed_info.description,
            )
        )
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=2,
                text="API Reference",
                className="text-2xl mb-6 border-b pb-2",
            ),
            c.Table(datasets=props),
        ],
    )


async def get_component_page(
    description_section: c.AnyComponent,
    preview_section: c.AnyComponent,
    api_reference_section: c.AnyComponent,
) -> c.AnyComponents:
    return [
        c.Container(
            tag="div",
            className="flex gap-12 flex-col",
            children=[description_section, preview_section, api_reference_section],
        )
    ]


@components_router.get("/avatar")
@apply_layout(docs_layout)
async def avatar_page() -> c.AnyComponents:
    return await get_component_page(
        description_section=await get_component_description_section(
            title="Avatar",
            description="An avatar is a visual representation of a user or a group of users.",
        ),
        preview_section=await get_component_preview_section(
            previews=[
                c.Container(
                    tag="div",
                    className="flex gap-3",
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
            ]
        ),
        api_reference_section=await get_component_api_reference_section(component=c.Avatar),
    )


@components_router.get("/button")
@apply_layout(docs_layout)
async def button_page() -> c.AnyComponents:
    return await get_component_page(
        description_section=await get_component_description_section(
            title="Button",
            description="A control that triggers an action. Button labels should express what action will occur when the ",
        ),
        preview_section=await get_component_preview_section(
            previews=[
                await get_component_preview_literal_component(
                    component_type=c.Button,
                    literal_props=["variant", "size"],
                    dynamic_props=["children"],
                    default_props_values={},
                )
            ]
        ),
        api_reference_section=await get_component_api_reference_section(component=c.Button),
    )


@components_router.get("/container")
@apply_layout(docs_layout)
async def container_page() -> c.AnyComponents:
    return await get_component_page(
        description_section=await get_component_description_section(
            title="Container",
            description="A container component.",
        ),
        preview_section=c.Container(
            tag="div",
        ),
        api_reference_section=await get_component_api_reference_section(component=c.Container),
    )


@components_router.get("/heading")
@apply_layout(docs_layout)
async def heading_page() -> c.AnyComponents:
    return await get_component_page(
        description_section=await get_component_description_section(
            title="Heading",
            description="A heading component.",
        ),
        preview_section=await get_component_preview_section(
            previews=[
                c.Heading(
                    level=2,
                    text="Heading",
                )
            ]
        ),
        api_reference_section=await get_component_api_reference_section(component=c.Heading),
    )


@components_router.get("/link")
@apply_layout(docs_layout)
async def link_page() -> c.AnyComponents:
    return await get_component_page(
        description_section=await get_component_description_section(
            title="Link",
            description="A link component.",
        ),
        preview_section=await get_component_preview_section(
            previews=[
                c.Link(
                    href="/",
                    children=[
                        c.Text(
                            text="Link",
                        )
                    ],
                )
            ]
        ),
        api_reference_section=await get_component_api_reference_section(component=c.Link),
    )


class TableExampleModel(BaseModel):
    column1: str
    column2: str
    column3: str


@components_router.get("/table")
@apply_layout(docs_layout)
async def table_page() -> c.AnyComponents:
    return await get_component_page(
        description_section=await get_component_description_section(
            title="Table",
            description="A table component.",
        ),
        preview_section=await get_component_preview_section(
            previews=[
                c.Table(
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
            ]
        ),
        api_reference_section=await get_component_api_reference_section(component=c.Table),
    )


@components_router.get("/text")
@apply_layout(docs_layout)
async def text_page() -> c.AnyComponents:
    return await get_component_page(
        description_section=await get_component_description_section(
            title="Text",
            description="A text component.",
        ),
        preview_section=await get_component_preview_section(
            previews=[
                c.Text(
                    text="Text",
                )
            ]
        ),
        api_reference_section=await get_component_api_reference_section(component=c.Text),
    )
