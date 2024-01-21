from tui import components as c


async def site_header() -> c.AnyComponent:
    return c.Container(
        tag="header",
        className="flex justify-between container h-14 border-b items-center",
        children=[
            c.Container(
                tag="nav",
                className="flex items-center gap-6",
                children=[
                    c.Link(
                        href="/",
                        children=[
                            c.Text(
                                text="tui",
                            )
                        ],
                    ),
                    c.Link(
                        href="/docs",
                        children=[
                            c.Text(
                                text="Docs",
                            )
                        ],
                    ),
                    c.Link(
                        href="/components",
                        children=[
                            c.Text(
                                text="Components",
                            )
                        ],
                    ),
                ],
            ),
        ],
    )
