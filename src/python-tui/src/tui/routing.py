import pathlib
from collections.abc import Awaitable
from contextlib import AsyncExitStack
from importlib import machinery
from types import ModuleType
from typing import Callable

from fastapi import APIRouter
from fastapi.dependencies.utils import solve_dependencies
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel, ConfigDict, Field, field_serializer
from starlette._utils import get_route_path
from starlette.types import Scope

from tui import components as c
from tui.render import get_prebuild_html, render_components_to_html

ROUTE_ROOT_FOLDER_NAME = "app"
ROUTE_INDEX_FILENAME = "page.py"
ROUTE_LAYOUT_FILENAME = "layout.py"
ROUTE_DEFAULT_SEGMENT = ""

ROOT_ROUTER_PREFIX = "/tui"
ROUTE_ROUTER_PREFIX = "/_route"
LAYOUT_ROUTER_SUFFIX = "_layout"


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
    endpoint: Callable[[Request], Awaitable[c.AnyComponents]] = Field(
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
    parent_pathname: str = "",
) -> list[Route]:
    routes = []
    segment = ROUTE_DEFAULT_SEGMENT if folder.stem == ROUTE_ROOT_FOLDER_NAME else folder.stem
    pathname = parent_pathname + segment + "/"

    layout_file = folder / ROUTE_LAYOUT_FILENAME
    page_file = folder / ROUTE_INDEX_FILENAME

    if page_file.is_file():
        routes.append(
            Route(
                segment=segment,
                pathname=pathname,
                endpoint=load_module(page_file, pathname).page,
                index=layout_file.is_file(),
            )
        )

    for child_folder in folder.iterdir():
        if child_folder.is_dir():
            routes.extend(get_routes(child_folder, pathname))

    if layout_file.is_file():
        routes = [
            Route(
                segment=segment, pathname=pathname, endpoint=load_module(layout_file, pathname).layout, children=routes
            )
        ]

    return routes


def get_routes_router(routes: list[Route]) -> APIRouter:
    router = APIRouter(prefix=ROOT_ROUTER_PREFIX)

    @router.get(ROUTE_ROUTER_PREFIX, response_model=list[Route])
    async def get_root_routes() -> list[Route]:
        return routes

    return router


def get_loader_router(routes: list[Route], router: APIRouter = APIRouter(prefix=ROOT_ROUTER_PREFIX)) -> APIRouter:
    for route in routes:
        path = route.pathname if route.index else route.pathname + LAYOUT_ROUTER_SUFFIX
        router.add_api_route(
            path,
            route.endpoint,
            response_model=c.AnyComponents,
        )
        if route.children:
            get_loader_router(route.children, router)
    return router


async def get_route_response(route: APIRoute, request: Request) -> c.AnyComponents:
    async with AsyncExitStack() as async_exit_stack:
        solved_result = await solve_dependencies(
            request=request,
            dependant=route.dependant,
            async_exit_stack=async_exit_stack,
        )
        values, errors, background_tasks, sub_response, _ = solved_result
    components = await route.dependant.call(**values)
    return components


def get_related_routes(routes: list[APIRoute], scope: Scope) -> list[APIRoute]:
    related_routes = []
    for route in routes:
        if route.name == "prebuild":
            continue
        route_path = ROOT_ROUTER_PREFIX + get_route_path(scope)
        match = route.path_regex.match(route_path)
        if match:
            related_routes.append(route)
    return related_routes


def get_prebuild_router(routes: list[APIRoute]) -> APIRouter:
    router = APIRouter()

    @router.get("/{path:path}")
    async def prebuild(request: Request) -> HTMLResponse:
        if request.method == "GET":
            related_routes = get_related_routes(routes, request.scope)
            if related_routes:
                components = await get_route_response(related_routes[0], request)
                html = render_components_to_html(components)
                return HTMLResponse(get_prebuild_html("tui", server_html=html))
        return HTMLResponse(get_prebuild_html("tui"))

    return router


def get_router(app: ModuleType) -> APIRouter:
    app_folder = pathlib.Path(app.__file__).parent
    root_router = APIRouter()

    routes = get_routes(app_folder)
    root_router.include_router(get_routes_router(routes))
    root_router.include_router(get_loader_router(routes))
    root_router.include_router(get_prebuild_router(root_router.routes))
    return root_router
