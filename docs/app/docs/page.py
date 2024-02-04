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
                        text="tui is a project inspired by FastUI, designed to simplify and accelerate web application "
                        "development. It is built on the powerful combination of FastAPI for backend efficiency and "
                        "Shadcn UI for creating stylish and responsive user interfaces.",
                        class_name="text-lg mt-3",
                    )
                ],
            ),
        ],
    )
