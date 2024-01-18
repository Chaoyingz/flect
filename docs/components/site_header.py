from tui import components as c


def site_header() -> c.AnyComponent:
    return c.Container(
                tag="header",
                className="flex justify-between container h-14 border-b items-center",
        components=[
            c.Link(
                href="/",
                components=[
                    c.Logo(
                        text="Tui",
                    )
                ],
            )
        ],
    )
