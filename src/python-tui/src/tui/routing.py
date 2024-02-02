import pathlib
from collections.abc import Awaitable
from importlib import machinery
from types import ModuleType
from typing import Callable

from fastapi import APIRouter
from fastapi.requests import Request
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from tui import components as c

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
    router = APIRouter()

    @router.get(ROUTE_ROUTER_PREFIX, response_model=list[Route])
    async def get_root_routes() -> list[Route]:
        return routes

    return router


def get_loader_router(
    routes: list[Route],
    router: APIRouter = APIRouter(),
) -> APIRouter:
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


def get_router(app: ModuleType) -> APIRouter:
    app_folder = pathlib.Path(app.__file__).parent
    root_router = APIRouter(prefix=ROOT_ROUTER_PREFIX)

    routes = get_routes(app_folder)
    root_router.include_router(get_routes_router(routes))
    root_router.include_router(get_loader_router(routes))
    return root_router
