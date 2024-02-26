from tui import Meta, PageResponse, TitleTemplate
from tui import components as c


async def layout(outlet: c.AnyComponent = c.Outlet()) -> PageResponse:
    return PageResponse(
        meta=Meta(title=TitleTemplate(template="{title} - tui framework", default="tui")),
        element=c.Container(
            tag="div",
            children=[
                c.Container(
                    tag="header",
                    class_name="h-14 border-b text-sm",
                    children=[
                        c.Container(
                            class_name="flex w-full justify-between container items-center h-full",
                            children=[
                                c.Container(
                                    tag="nav",
                                    class_name="flex items-center gap-6",
                                    children=[
                                        c.Link(
                                            href="/",
                                            children=[
                                                c.Text(
                                                    text="tui",
                                                    class_name="font-medium text-xl",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/docs/introduction/",
                                            children=[
                                                c.Text(
                                                    text="Docs",
                                                )
                                            ],
                                        ),
                                        c.Link(
                                            href="/components/avatar/",
                                            children=[
                                                c.Text(
                                                    text="Components",
                                                )
                                            ],
                                        ),
                                    ],
                                ),
                                c.Container(
                                    tag="div",
                                    children=[
                                        c.Link(
                                            href="https://github.com/Chaoyingz/tui",
                                            children=[
                                                c.Text(
                                                    text="GitHub",
                                                )
                                            ],
                                        )
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                c.Container(
                    tag="main",
                    class_name="container",
                    children=[outlet],
                ),
                c.Container(
                    tag="footer",
                    class_name="border-t text-sm container py-8 mt-8",
                    children=[
                        c.Text(text="Built by "),
                        c.Link(
                            href="https://github.com/Chaoyingz",
                            children=[
                                c.Text(
                                    text="Chaoying.",
                                    class_name="underline",
                                )
                            ],
                        ),
                        c.Text(
                            text=" The source code is available on ",
                        ),
                        c.Link(
                            href="https://github.com/Chaoyingz/tui/tree/main/docs",
                            children=[
                                c.Text(
                                    text="GitHub.",
                                    class_name="underline",
                                )
                            ],
                        ),
                    ],
                ),
            ],
        ),
    )
