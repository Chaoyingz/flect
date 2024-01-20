from tui import components as c


async def landing_page() -> list[c.AnyComponent]:
    return [
        c.Container(
            tag="section",
            className="container",
            children=[
                c.Heading(
                    level=1,
                    text="Turning ideas into web app fast.",
                )
            ],
        )
    ]
