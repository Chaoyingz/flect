from flect import PageResponse
from flect import components as c


async def page() -> PageResponse:
    return PageResponse(
        body=c.Container(
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
                            text="flect enables you to quickly create full-stack web applications using Python.",
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
                                            children=[c.Text(text="Get Started")],
                                        )
                                    ],
                                ),
                                c.Link(
                                    href="https://github.com/Chaoyingz/flect",
                                    children=[
                                        c.Button(
                                            children=[c.Text(text="GitHub")],
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
