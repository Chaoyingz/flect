from tui import components as c


async def layout(outlet: c.AnyComponent = c.Outlet()) -> c.AnyComponent:
    return c.Container(
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
                                        href="/docs/",
                                        children=[
                                            c.Text(
                                                text="Docs",
                                            )
                                        ],
                                    ),
                                    c.Link(
                                        href="/docs/components/avatar/",
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
        ],
    )
