from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from tui import components as c
from tui.prebuild import get_prebuild_html

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def layout(components: list[c.AnyComponent]) -> list[c.AnyComponent]:
    return [
        c.Container(
            tag="header",
            className="flex justify-between container h-14 border-b items-center",
            components=[
                c.Link(
                    href="/",
                    text="Tui",
                )
            ],
        ),
        c.Container(
            tag="main",
            className="container flex gap-6",
            components=[
                c.Container(
                    tag="aside",
                    className="py-6 pr-6 w-56",
                    components=[
                        c.Container(
                            tag="nav",
                            components=[
                                c.Heading(level=2, text="Components"),
                                c.Container(
                                    tag="section",
                                    className="flex flex-col gap-3 mt-4",
                                    components=[
                                        c.Link(
                                            href="/components/button",
                                            text="Button",
                                        ),
                                        c.Link(
                                            href="/components/avatar",
                                            text="Avatar",
                                        ),
                                        c.Link(
                                            href="/components/container",
                                            text="Container",
                                        ),
                                        c.Link(
                                            href="/components/logo",
                                            text="Logo",
                                        ),
                                        c.Link(
                                            href="/components/heading",
                                            text="Heading",
                                        ),
                                        c.Link(
                                            href="/components/link",
                                            text="Link",
                                        ),
                                    ],
                                ),
                            ],
                        )
                    ],
                ),
                c.Container(tag="section", className="w-full p-6", components=components),
            ],
        ),
    ]


@app.get("/api/")
async def home():
    return layout([c.Heading(level=1, text="Tui")])


@app.get("/api/components/button")
async def button():
    buttons = [
        c.Button(children=variant, variant=variant)
        for variant in ["default", "destructive", "outline", "secondary", "ghost", "link"]
    ]
    return layout([c.Container(tag="div", className="flex gap-2", components=buttons)])


@app.get("/api/components/avatar")
async def avatar():
    return layout([c.Avatar(fallback="Avatar")])


@app.get("/api/components/container")
async def container():
    return layout(
        [
            c.Container(
                tag="div",
            )
        ]
    )


@app.get("/api/components/logo")
async def logo():
    return layout([c.Logo(text="Logo")])


@app.get("/api/components/heading")
async def heading():
    return layout([c.Heading(level=1, text="Heading")])


@app.get("/api/components/link")
async def link():
    return layout([c.Link(href="/components/button", text="Link")])


@app.get("/{path:path}")
async def prebuild():
    return HTMLResponse(get_prebuild_html("tui", "https://cdn.jsdelivr.net/npm/@chaoying/npm-tui@0.1.2/dist"))
