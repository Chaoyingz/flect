from typing import Optional

from fastapi import APIRouter
from pydantic import BaseModel
from tui import apply_layout
from tui import components as c

from docs.layouts.docs_layout import docs_layout

components_router = APIRouter(prefix="/components")


class ComponentProps(BaseModel):
    prop: str
    type: str
    default: Optional[str]
    description: Optional[str]


async def get_component_prop_preview(
    name: str,
    examples: c.AnyComponents,
) -> c.AnyComponent:
    return c.Container(
        tag="section",
        children=[
            c.Heading(
                level=3,
                text=name,
            ),
            c.Container(tag="div", className="flex gap-4 mt-3", children=examples),
        ],
    )


async def get_component_api_reference_table(component: c.AnyComponent) -> c.Table:
    props = []
    for field, filed_info in component.model_fields.items():
        if field == "ctype":
            continue
        if field == "children":
            filed_info.annotation = "tui.components.AnyComponents"
            filed_info.default = "[]"
            filed_info.description = "The children of the component."
        props.append(
            ComponentProps(
                prop=field,
                type=str(filed_info.annotation),
                default=filed_info.default or "-",
                description=filed_info.description,
            )
        )
    return c.Table(
        datasets=props,
    )


async def get_component_page(
    title: str,
    description: str,
) -> c.AnyComponents:
    return [
        c.Container(
            tag="div",
            className="flex gap-12 flex-col",
            children=[
                c.Container(
                    tag="section",
                    children=[
                        c.Heading(
                            level=1,
                            text=title,
                            className="text-3xl mb-3",
                        ),
                        c.Text(text=description),
                    ],
                ),
                c.Container(
                    tag="section",
                    children=[
                        c.Heading(
                            level=2,
                            text="Preview",
                            className="text-2xl mb-6 border-b pb-2",
                        ),
                        c.Container(
                            tag="section",
                            className="flex flex-col gap-10",
                            children=[
                                await get_component_prop_preview(
                                    name="Variants",
                                    examples=[
                                        c.Button(
                                            children=variant,
                                            variant=variant,
                                        )
                                        for variant in c.Button.__annotations__["variant"].__args__
                                    ],
                                ),
                                await get_component_prop_preview(
                                    name="Size",
                                    examples=[
                                        c.Button(
                                            children=size,
                                            size=size,
                                        )
                                        for size in c.Button.__annotations__["size"].__args__
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
                c.Container(
                    tag="section",
                    children=[
                        c.Heading(
                            level=2,
                            text="API Reference",
                            className="text-2xl mb-6 border-b pb-2",
                        ),
                        await get_component_api_reference_table(c.Button),
                    ],
                ),
            ],
        )
    ]


@components_router.get("/button")
@apply_layout(docs_layout)
async def button_page() -> c.AnyComponents:
    return await get_component_page(
        title="Button",
        description="A control that triggers an action. Button labels should express what action will occur when the "
        "user interacts with it.",
    )
