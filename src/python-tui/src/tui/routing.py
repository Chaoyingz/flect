import pathlib
from collections.abc import Awaitable
from importlib import machinery
from types import ModuleType
from typing import Any, Callable

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from tui import components as c
from tui.render import get_pre_render_html, get_prebuild_html

ROUTE_ROOT_FOLDER_NAME = "app"
ROUTE_INDEX_FILENAME = "page.py"
ROUTE_LAYOUT_FILENAME = "layout.py"
ROUTE_DEFAULT_SEGMENT = ""

ROOT_ROUTER_PREFIX = "/tui"
ROUTE_ROUTER_PATH = "/_route/"
LAYOUT_ROUTER_SUFFIX = "_layout/"


class Route(BaseModel):
    model_config = ConfigDict(extra="forbid")

    segment: str = Field(
        ...,
        description="The segment of the route.",
    )
    pathname: str = Field(
        ...,
        description="The pathname of the route.",
    )
    index: bool = Field(
        False,
        description="Determines if the route is an index route."
        "Index routes render into their parent's Outlet at their parent's URL.",
    )
    endpoint: Callable[[Any], Awaitable[c.AnyComponent]] = Field(
        ...,
        description="The endpoint of the route.",
    )
    children: list["Route"] = Field(
        [],
        description="The children of the route.",
    )

    @field_serializer("endpoint")
    def serialize_endpoint(self, value: Callable[[Request], Awaitable[c.AnyComponents]]) -> str:
        return value.__name__


Route.model_rebuild()


def load_module(file_path: pathlib.Path, route_pathname: str) -> ModuleType:
    module_name = f"{route_pathname}_{file_path.stem}"
    return machinery.SourceFileLoader(module_name, str(file_path)).load_module()


def get_routes(
    folder: pathlib.Path,
    parent_pathname: str = "/",
) -> list[Route]:
    routes = []
    segment = ROUTE_DEFAULT_SEGMENT if folder.stem == ROUTE_ROOT_FOLDER_NAME else folder.stem
    pathname = parent_pathname + segment
    if segment:
        pathname += "/"

    layout_file = folder / ROUTE_LAYOUT_FILENAME
    page_file = folder / ROUTE_INDEX_FILENAME

    if page_file.is_file():
        routes.append(
            Route(
                segment=segment,
                pathname=pathname,
                endpoint=load_module(page_file, pathname).page,
                index=layout_file.is_file(),
                children=[],
            )
        )

    for child_folder in folder.iterdir():
        if child_folder.is_dir():
            routes.extend(get_routes(child_folder, pathname))

    if layout_file.is_file():
        routes = [
            Route(
                segment=segment,
                pathname=pathname,
                index=False,
                endpoint=load_module(layout_file, pathname).layout,
                children=routes,
            )
        ]

    return routes


def get_routes_router(routes: list[Route]) -> APIRouter:
    router = APIRouter(prefix=ROOT_ROUTER_PREFIX)

    @router.get(ROUTE_ROUTER_PATH, response_model=list[Route])
    async def get_root_routes() -> list[Route]:
        return routes

    return router


def get_loader_router(routes: list[Route], router: APIRouter = APIRouter(prefix=ROOT_ROUTER_PREFIX)) -> APIRouter:
    for route in routes:
        path = route.pathname if route.index else route.pathname + LAYOUT_ROUTER_SUFFIX
        router.add_api_route(
            path,
            route.endpoint,
            response_model=c.AnyComponent,
        )
        if route.children:
            get_loader_router(route.children, router)
    return router


def get_pre_render_router(routes: list[APIRoute]) -> APIRouter:
    router = APIRouter()

    async def pre_render(request: Request) -> HTMLResponse:
        if request.method == "GET":
            html = await get_pre_render_html(request, routes)
            return HTMLResponse(get_prebuild_html("tui", server_html=html or ""))
        return HTMLResponse(get_prebuild_html("tui"))

    router.add_api_route("/{path:path}", pre_render, methods=["GET"])
    return router


def get_router(app: ModuleType) -> APIRouter:
    if app.__file__ is None:
        raise RuntimeError("The app module must have a __file__ attribute.")
    app_folder = pathlib.Path(app.__file__).parent

    routes = get_routes(app_folder)

    root_router = APIRouter()
    root_router.include_router(get_routes_router(routes))
    root_router.include_router(get_loader_router(routes))
    root_router.include_router(get_pre_render_router(root_router.routes))  # type: ignore
    return root_router
