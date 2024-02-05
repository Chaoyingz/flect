from tui import components as c


async def page() -> c.AnyComponent:
    return c.Container(
        tag="div",
        children=[
            c.Heading(
                level=1,
                text="Introduction",
                class_name="text-3xl mb-3",
            ),
            c.Container(
                class_name="mt-3",
                children=[
                    c.Text(
                        text="Use Pydantic models in the backend that correspond to the properties of React components "
                        "in the frontend. This enables you to quickly develop interactive and beautiful UIs using "
                        "Python.",
                        class_name="text-lg mt-3",
                    )
                ],
            ),
        ],
    )
