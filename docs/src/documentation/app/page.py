from tui import PageResponse
from tui import components as c


async def page() -> PageResponse:
    return PageResponse(
        element=c.Container(
            tag="section",
            class_name="container",
            children=[
                c.Container(
                    tag="section",
                    class_name="flex justify-center py-32 flex-col items-center",
                    children=[
                        c.Heading(
                            level=1, text="Turning ideas into web app fast", class_name="text-center text-5xl font-bold"
                        ),
                        c.Text(
                            text="tui enables you to quickly create full-stack web applications using Python.",
                            class_name="text-center text-xl mt-8 w-1/2",
                        ),
                        c.Container(
                            tag="div",
                            class_name="flex gap-4 mt-8",
                            children=[
                                c.Link(
                                    href="/docs/introduction/",
                                    children=[
                                        c.Button(
                                            children="Get Started",
                                        )
                                    ],
                                ),
                                c.Link(
                                    href="https://github.com/Chaoyingz/tui",
                                    children=[
                                        c.Button(
                                            children="GitHub",
                                            variant="outline",
                                        )
                                    ],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )
    )
