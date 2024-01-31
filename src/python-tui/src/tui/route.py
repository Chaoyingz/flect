import pathlib
import typing as _t
from importlib import machinery
from types import ModuleType

import pydantic as _p
from fastapi.requests import Request

from tui import components as c

ROUTE_ROOT_FOLDER_NAME = "app"
ROUTE_INDEX_FILENAME = "page.py"
ROUTE_LAYOUT_FILENAME = "layout.py"
ROUTE_DEFAULT_SEGMENT = ""


class RouteComponent(_p.BaseModel):
    model_config = _p.ConfigDict(extra="forbid")

    segment: str = _p.Field(
        ...,
        description="The segment of the route.",
    )
    pathname: str = _p.Field(
        ...,
        description="The pathname of the route.",
    )
    index: _t.Optional[bool] = _p.Field(
        False,
        description="Whether the route is the index.",
    )
    children: _t.Optional[list["RouteComponent"]] = _p.Field(
        None,
        description="The children of the route.",
    )


class Route(RouteComponent):
    endpoint: _t.Callable[[Request], _t.Awaitable[c.AnyComponents]] = _p.Field(
        ...,
        description="The endpoint of the route.",
    )
    layout: _t.Optional[_t.Callable[[Request], _t.Awaitable[c.AnyComponents]]] = _p.Field(
        None,
        description="The layout of the route.",
    )
    children: _t.Optional[list["Route"]] = _p.Field(
        None,
        description="The children of the route.",
    )


RouteComponent.model_rebuild()
Route.model_rebuild()


def load_module(file_path: pathlib.Path, route_pathname: str) -> ModuleType:
    module_name = f"{route_pathname}_{file_path.stem}"
    return machinery.SourceFileLoader(module_name, str(file_path)).load_module()


def get_routes(
    folder: pathlib.Path,
    parent_pathname: str = "",
) -> list[Route]:
    """
    Get the routes from the folder.

    Parameters
    ----------
    folder
        The folder to get the routes from.
    parent_pathname
        The parent pathname of the routes.
    """
    routes = []
    page_file = folder / ROUTE_INDEX_FILENAME
    if not page_file.is_file():
        return routes

    segment = ROUTE_DEFAULT_SEGMENT if folder.stem == ROUTE_ROOT_FOLDER_NAME else folder.stem
    pathname = parent_pathname + segment + "/"
    endpoint = load_module(page_file, pathname).page

    layout_file = folder / ROUTE_LAYOUT_FILENAME
    layout = load_module(layout_file, pathname).layout if layout_file.is_file() else None

    route = Route(
        segment=segment,
        pathname=pathname,
        endpoint=endpoint,
        layout=layout,
        children=[],
    )
    for child in folder.iterdir():
        if child.is_dir():
            route.children.extend(get_routes(child, str(pathname)))

    route.index = not bool(route.children)
    if route.children:
        route.children.append(Route(segment=segment, pathname=pathname, endpoint=endpoint, layout=layout, index=True))
    print(route.children)
    routes.append(route)
    return routes
