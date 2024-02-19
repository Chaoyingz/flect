import importlib.util
import pathlib
from collections.abc import Awaitable
from functools import lru_cache
from types import ModuleType
from typing import Any, Callable, cast

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse
from fastapi.routing import APIRoute
from pydantic import BaseModel, ConfigDict, Field, field_serializer

from tui.render import generate_html, render_server_side_html
from tui.response import PageResponse

EXCLUDED_FOLDER_NAMES = {"__pycache__"}
DYNAMIC_ROUTE_PREFIX = "_"

CLIENT_ROUTE_INDEX_FILENAME = "page.py"
CLIENT_ROUTE_LAYOUT_FILENAME = "layout.py"
CLIENT_ROOT_ROUTER_PREFIX = "/tui"
CLIENT_ROUTE_ROUTER_PATH = "/_route/"
CLIENT_LAYOUT_ROUTER_SUFFIX = "_layout/"

SERVER_API_ROUTE_FILENAME = "route.py"
SERVER_API_ROUTE_METHODS = {"GET", "POST"}


class ClientRoute(BaseModel):
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
    endpoint: Callable[[Any], Awaitable[PageResponse]] = Field(
        ...,
        description="The endpoint of the route.",
    )
    children: list["ClientRoute"] = Field(
        [],
        description="The children of the route.",
    )

    @field_serializer("endpoint")
    def serialize_endpoint(self, value: Callable[[Request], Awaitable[PageResponse]]) -> str:
        return value.__name__


ClientRoute.model_rebuild()


@lru_cache
def load_module(file_path: pathlib.Path) -> ModuleType:
    """
    Loads a Python module from a given file path.

    Parameters
    ----------
    file_path : pathlib.Path
        The file path of the module to load.

    Returns
    -------
    ModuleType
        The loaded module.
    """
    spec = importlib.util.spec_from_file_location(file_path.stem, str(file_path))
    if spec and spec.loader:
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module
    raise ImportError(f"Could not load module from {file_path}")


def get_route_segment(folder: pathlib.Path, is_root: bool = True) -> str:
    """
    Gets the route segment based on the folder name.
    """
    if is_root:
        return ""
    if folder.stem.startswith(DYNAMIC_ROUTE_PREFIX):
        return "{" + folder.stem[len(DYNAMIC_ROUTE_PREFIX) :] + "}"
    return folder.stem


def get_route_pathname(parent_pathname: str, segment: str) -> str:
    """
    Constructs the route pathname based on the parent pathname and the segment.
    """
    return f"{parent_pathname.rstrip('/')}/{segment}/" if segment else parent_pathname


def get_client_route_objs(
    folder: pathlib.Path,
    parent_pathname: str = "/",
    is_root: bool = True,
) -> list[ClientRoute]:
    """
    Gets a list of ClientRoute objects from the given folder.

    Parameters
    ----------
    folder : pathlib.Path
        The folder from which to start building routes.
    parent_pathname : str, optional
        The pathname of the parent route, by default "/".
    is_root : bool, optional
        Flag indicating if the folder is the root of the routing structure, by default True.

    Returns
    -------
    list[Route]
        A list of Route objects built from the folder structure.
    """
    routes = []
    segment = get_route_segment(folder, is_root)
    pathname = get_route_pathname(parent_pathname, segment)
    layout_file = folder / CLIENT_ROUTE_LAYOUT_FILENAME
    page_file = folder / CLIENT_ROUTE_INDEX_FILENAME

    if page_file.is_file():
        routes.append(
            ClientRoute(
                segment=segment,
                pathname=pathname,
                endpoint=load_module(page_file).page,
                index=layout_file.is_file(),
                children=[],
            )
        )

    for child_folder in folder.iterdir():
        if child_folder.is_dir() and child_folder.name not in EXCLUDED_FOLDER_NAMES:
            routes.extend(get_client_route_objs(child_folder, pathname, False))

    if layout_file.is_file():
        routes = [
            ClientRoute(
                segment=segment,
                pathname=pathname,
                index=False,
                endpoint=load_module(layout_file).layout,
                children=routes,
            )
        ]

    return routes


def get_client_routes_router(routes: list[ClientRoute]) -> APIRouter:
    """
    Builds an APIRouter with the given routes.

    Parameters
    ----------
    routes : list[Route]
        The list of routes to be served.

    Returns
    -------
    APIRouter
        The APIRouter instance configured with the routes.
    """
    router = APIRouter(prefix=CLIENT_ROOT_ROUTER_PREFIX)

    async def get_root_routes() -> list[ClientRoute]:
        return routes

    router.add_api_route(CLIENT_ROUTE_ROUTER_PATH, get_root_routes, methods=["GET"])
    return router


def get_client_loader_router(
    routes: list[ClientRoute], router: APIRouter = APIRouter(prefix=CLIENT_ROOT_ROUTER_PREFIX)
) -> APIRouter:
    """
    Configures an APIRouter with endpoints for dynamically loading components based on the routes.

    Parameters
    ----------
    routes : list[Route]
        The list of routes to configure for component loading.
    router : APIRouter, optional
        An existing APIRouter instance to configure, by default a new router with CLIENT_ROOT_ROUTER_PREFIX.

    Returns
    -------
    APIRouter
        The configured APIRouter instance.
    """
    for route in routes:
        path = route.pathname if not route.children else route.pathname + CLIENT_LAYOUT_ROUTER_SUFFIX
        router.add_api_route(
            path,
            route.endpoint,
            response_model=PageResponse,
            methods=["GET"],
        )
        if route.children:
            get_client_loader_router(route.children, router)
    return router


def get_server_api_router(
    folder: pathlib.Path,
    parent_pathname: str = "/",
    is_root: bool = True,
) -> APIRouter:
    router = APIRouter()
    segment = get_route_segment(folder, is_root)
    pathname = get_route_pathname(parent_pathname, segment)
    route_file = folder / SERVER_API_ROUTE_FILENAME
    if route_file.is_file():
        module = load_module(route_file)
        for method in SERVER_API_ROUTE_METHODS:
            endpoint = getattr(module, method.lower(), None)
            if endpoint:
                router.add_api_route(pathname, endpoint, methods=[method])

    for child_folder in folder.iterdir():
        if child_folder.is_dir() and child_folder.name not in EXCLUDED_FOLDER_NAMES:
            router.include_router(get_server_api_router(child_folder, parent_pathname=pathname, is_root=False))
    return router


def get_server_pre_render_router(loader_routes: list[APIRoute]) -> APIRouter:
    """
    Creates an APIRouter for pre-rendering server-side HTML based on the routes.

    Parameters
    ----------
    loader_routes : list[APIRoute]
        The list of loader routes to use for pre-rendering.

    Returns
    -------
    APIRouter
        The APIRouter instance for server-side pre-rendering.
    """
    router = APIRouter()

    async def pre_render(request: Request) -> HTMLResponse:
        meta_html, element_html = await render_server_side_html(
            request, loader_routes, CLIENT_ROOT_ROUTER_PREFIX, CLIENT_LAYOUT_ROUTER_SUFFIX
        )
        return HTMLResponse(generate_html(meta_html, element_html))

    router.add_api_route("/{path:path}", pre_render, methods=["GET"])
    return router


def configure_app_router(app: ModuleType) -> APIRouter:
    """
    Constructs the main APIRouter for the application by loading routes from the app module.

    Parameters
    ----------
    app : ModuleType
        The main application module containing the file structure for routes.

    Returns
    -------
    APIRouter
        The main APIRouter for the application, configured with routes and pre-rendering.

    Raises
    ------
    RuntimeError
        If the app module does not have a __file__ attribute, indicating it cannot be used for route loading.
    """
    if not hasattr(app, "__file__"):
        raise RuntimeError("App module missing '__file__' attribute. Ensure it's a proper package or module.")
    app_folder = pathlib.Path(cast(str, app.__file__)).parent

    root_router = APIRouter()

    client_routes = get_client_route_objs(app_folder)
    root_router.include_router(get_client_routes_router(client_routes))
    loader_router = get_client_loader_router(client_routes)
    root_router.include_router(loader_router)

    root_router.include_router(get_server_api_router(app_folder))
    root_router.include_router(get_server_pre_render_router(cast(list[APIRoute], loader_router.routes)))
    return root_router
