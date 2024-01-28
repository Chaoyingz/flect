from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from tui import components as c
from tui import init_tui
from tui.route import Route

tui_router = APIRouter(prefix="/tui")
# tui_router.include_router(landing_router)
# tui_router.include_router(docs_router)
# tui_router.include_router(components_router)


@tui_router.get("/_route")
async def route():
    return Route(
        path="",
        children=[
            Route(
                path="",
                index=True,
            ),
            Route(
                path="hello",
                children=[
                    Route(
                        path="hello",
                        index=True,
                    ),
                    Route(
                        path="world",
                    ),
                ],
            ),
        ],
    )


@tui_router.get("/_layout")
async def index():
    return [
        c.Container(
            tag="header",
            children=[
                c.Link(
                    href="/",
                    children=[
                        c.Text(
                            text="index",
                        )
                    ],
                ),
                c.Link(
                    href="/hello",
                    children=[
                        c.Text(
                            text="hello",
                        )
                    ],
                ),
                c.Link(
                    href="/hello/world",
                    children=[
                        c.Text(
                            text="hello-world",
                        )
                    ],
                ),
            ],
        ),
        c.Container(tag="main", children=[c.Outlet()]),
    ]


@tui_router.get("/hello/_layout")
async def index1():
    return [
        c.Heading(
            level=1,
            text="hello",
        ),
        c.Outlet(),
    ]


@tui_router.get("/")
async def index():
    return [
        c.Heading(
            level=1,
            text="tui",
        )
    ]


@tui_router.get("/hello")
async def hello():
    return [
        c.Heading(
            level=1,
            text="hello",
        )
    ]


@tui_router.get("/hello/world")
async def hello_world():
    return [
        c.Heading(
            level=1,
            text="hello world",
        )
    ]


def get_application() -> FastAPI:
    application = FastAPI()
    application.include_router(tui_router)
    return application


app = get_application()
init_tui(app)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
