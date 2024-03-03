from tui import PageResponse
from tui import components as c
from tui import version


async def page() -> PageResponse:
    return PageResponse(
        element=c.Container(
            tag="section",
            children=[
                c.Container(
                    tag="header",
                    class_name="h-14 border-b text-sm flex items-center px-6 justify-between",
                    children=[
                        c.Link(
                            href="https://tui.celerforge.com/",
                            children=[
                                c.Text(
                                    text="tui",
                                    class_name="font-medium text-xl",
                                )
                            ],
                        ),
                        c.Text(
                            text=f"v{version.VERSION}",
                        ),
                    ]
                ),
                c.Container(
                    tag="main",
                    class_name="flex justify-center p-32 flex-col items-center",
                    children=[
                        c.Heading(
                            level=1, text="Welcome to tui framework",
                            class_name="flex items-center justify-center text-5xl font-bold mb-4"
                        ),
                        c.Text(
                            text="Get started by editing src/{{cookiecutter.project_slug}}/page.py",
                        ),
                        c.Container(
                            tag="div",
                            class_name="flex gap-4 mt-8",
                            children=[
                                c.Link(
                                    href="/",
                                    children=[
                                        c.Button(
                                            children="Go to docs",
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
                        )
                    ]
                ),
            ],
        ),
    )
