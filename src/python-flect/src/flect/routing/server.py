import pathlib
from collections.abc import Generator
from itertools import chain
from types import ModuleType
from typing import Optional, cast

from fastapi import APIRouter
from fastapi.requests import Request
from fastapi.responses import HTMLResponse, Response
from fastapi.routing import APIRoute

from flect.constants import (
    API_ROUTE_FILENAME,
    API_ROUTE_METHODS,
    EXCLUDED_FOLDER_NAMES,
    NAVIGATION_ROUTE_PATH,
    ROOT_ROUTE_PREFIX,
)
from flect.render import generate_html, render_server_side_html
from flect.response import PageResponse
from flect.routing.client import ClientRoute, get_client_routes, parse_route_info_from_folder
from flect.routing.sort import path_priority
from flect.sitemap import generate_sitemap_xml
from flect.utils import load_module


def generate_navigation_routes(client_routes: list[ClientRoute]) -> Generator[APIRoute, None, None]:
    """
    Generates a list of APIRoute objects from the given list of ClientRoute objects.

    Parameters
    ----------
    client_routes : list[ClientRoute]
        The list of ClientRoute objects to convert to APIRoute objects.

    Returns
    -------
    Generator[APIRoute, None, None]
        A generator of APIRoute objects from the given list of ClientRoute objects.
    """

    async def get_navigation_route() -> list[ClientRoute]:
        return client_routes

    yield APIRoute(path=f"{ROOT_ROUTE_PREFIX}{NAVIGATION_ROUTE_PATH}", endpoint=get_navigation_route)


def generate_loader_routes(routes: list[ClientRoute]) -> Generator[APIRoute, None, None]:
    """
    Generates a list of APIRoute objects from the given list of ClientRoute objects.

    Parameters
    ----------
    routes : list[ClientRoute]
        The list of ClientRoute objects to convert to APIRoute objects.

    Returns
    -------
    Generator[APIRoute, None, None]
        A generator of APIRoute objects from the given list of ClientRoute objects.
    """
    for route in routes:
        yield APIRoute(
            path=route.loader_path,
            endpoint=route.endpoint,
            response_model=PageResponse,
            methods=["GET"],
        )
        if route.children:
            yield from generate_loader_routes(route.children)


def generate_api_routes(
    folder: pathlib.Path,
    is_root_folder: bool = True,
    parent_path: str = "/",
) -> Generator[APIRoute, None, None]:
    """
    Generates a list of APIRoute objects from the given folder.

    Parameters
    ----------
    folder : pathlib.Path
        The folder from which to start building routes.
    is_root_folder : bool, optional
        Flag indicating if the folder is the root of the routing structure, by default True.
    parent_path : str
        The path of the parent route, by default "/".

    Returns
    -------
    Generator[APIRoute, None, None]
        A generator of APIRoute objects from the given folder.
    """
    route_info = parse_route_info_from_folder(folder, is_root_folder, parent_path, absolute_path="/")
    route_file = folder / API_ROUTE_FILENAME
    if route_file.is_file():
        module = load_module(route_file)
        for method in API_ROUTE_METHODS:
            endpoint = getattr(module, method.lower(), None)
            if endpoint:
                yield APIRoute(path=f"{ROOT_ROUTE_PREFIX}{route_info.path}", endpoint=endpoint, methods=[method])

    for child_folder in folder.iterdir():
        if child_folder.is_dir() and child_folder.name not in EXCLUDED_FOLDER_NAMES:
            yield from generate_api_routes(child_folder, is_root_folder=False, parent_path=route_info.path)


def generate_server_side_render_routes(
    client_routes: list[ClientRoute],
    loader_routes: list[APIRoute],
    prebuilt_uri: Optional[str] = None,
) -> Generator[APIRoute, None, None]:
    """
    Generates a list of APIRoute objects from the given list of ClientRoute objects.

    Parameters
    ----------
    client_routes : list[ClientRoute]
        The list of ClientRoute objects to convert to APIRoute objects.
    loader_routes : list[APIRoute]
        The list of APIRoute objects to convert to APIRoute objects.
    prebuilt_uri : Optional[str], optional
        The prebuilt URI to use, by default None.

    Returns
    -------
    Generator[APIRoute, None, None]
        A generator of APIRoute objects from the given list of ClientRoute objects.
    """

    async def get_server_side_render_route(request: Request) -> HTMLResponse:
        head_html, element_html = await render_server_side_html(request, client_routes, loader_routes)
        return HTMLResponse(generate_html(head_html, element_html, prebuilt_uri))

    yield APIRoute(
        path="/{path:path}",
        endpoint=get_server_side_render_route,
        methods=["GET"],
    )


def generate_sitemap_routes(
    client_routes: list[ClientRoute],
) -> Generator[APIRoute, None, None]:
    """
    Generates a list of APIRoute objects from the given list of ClientRoute objects.

    Parameters
    ----------
    client_routes : list[ClientRoute]
        The list of ClientRoute objects to convert to APIRoute objects.

    Returns
    -------
    Generator[APIRoute, None, None]
        A generator of APIRoute objects from the given list of ClientRoute objects.
    """

    async def get_sitemap_route(request: Request) -> Response:
        base_url = f"{request.base_url.scheme}://{request.base_url.netloc}"
        return Response(await generate_sitemap_xml(client_routes, base_url), media_type="application/xml")

    yield APIRoute("/sitemap.xml", get_sitemap_route, methods=["GET"])


def get_app_router(
    app: ModuleType,
    prebuilt_uri: Optional[str] = None,
) -> APIRouter:
    """
    Constructs the main APIRouter for the application by loading routes from the app module.

    Parameters
    ----------
    app : ModuleType
        The main application module containing the file structure for routes.
    prebuilt_uri : Optional[str], optional
        The prebuilt URI to use for the app, by default None

    Returns
    -------
    APIRouter
        The main APIRouter for the application, configured with routes and pre-rendering.

    Raises
    ------
    RuntimeError
        If the '__file__' attribute of the app module is missing.
    """
    if not hasattr(app, "__file__"):
        raise RuntimeError("App module missing '__file__' attribute. Ensure it's a proper package or module.")
    app_folder = pathlib.Path(cast(str, app.__file__)).parent

    client_routes = get_client_routes(app_folder)
    navigation_routes = generate_navigation_routes(client_routes)
    api_routes = generate_api_routes(app_folder)
    loader_routes = list(generate_loader_routes(client_routes))
    server_side_render_routes = generate_server_side_render_routes(client_routes, loader_routes, prebuilt_uri)
    sitemap_routes = generate_sitemap_routes(client_routes)

    root_router = APIRouter()
    for route in sorted(
        chain(
            navigation_routes, api_routes, (route for route in loader_routes), server_side_render_routes, sitemap_routes
        ),
        key=lambda r: path_priority(r.path),
    ):
        root_router.routes.append(route)
    return root_router
