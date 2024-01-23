from fastapi import APIRouter
from tui import apply_layout
from tui import components as c

from docs.layouts.docs_layout import docs_layout

components_router = APIRouter(prefix="/components")


async def get_component_props_examples() -> c.AnyComponents:
    ...


async def get_component_props(
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


async def get_component_page(
    title: str,
    description: str,
) -> c.AnyComponents:
    return [
        c.Heading(
            level=1,
            text=title,
            className="text-3xl mb-3",
        ),
        c.Text(text=description),
        c.Container(
            tag="div",
            className="flex flex-col gap-10 mt-10",
            children=[
                await get_component_props(
                    name="Variants",
                    examples=[
                        c.Button(
                            children=variant,
                            variant=variant,
                        )
                        for variant in c.Button.__annotations__["variant"].__args__
                    ],
                ),
                await get_component_props(
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
    ]


@components_router.get("/button")
@apply_layout(docs_layout)
async def button_page() -> c.AnyComponents:
    return await get_component_page(
        title="Button",
        description="A control that triggers an action. Button labels should express what action will occur when the "
        "user interacts with it.",
    )
