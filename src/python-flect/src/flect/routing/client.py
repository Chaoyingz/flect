import pathlib
from collections import namedtuple
from collections.abc import Awaitable
from typing import Any, Callable, Optional

from pydantic import BaseModel, ConfigDict, Field

from flect.constants import (
    DYNAMIC_ROUTE_PREFIX,
    EXCLUDED_FOLDER_NAMES,
    GROUP_ROUTE_PREFIX,
    LAYOUT_ROUTE_FILENAME,
    LAYOUT_ROUTE_SUFFIX,
    PAGE_ROUTE_FILENAME,
    ROOT_ROUTE_PREFIX,
)
from flect.response import PageResponse
from flect.routing.sort import path_priority
from flect.sitemap import Sitemap
from flect.utils import load_module


class ClientRoute(BaseModel):
    model_config = ConfigDict(extra="forbid")

    segment: str = Field(
        ...,
        description="A specific segment of the route, often a single directory or identifier.",
    )
    path: str = Field(
        ...,
        description="The path of the route relative to its parent. This corresponds to the 'path' in react-router.",
    )
    absolute_path: str = Field(
        ...,
        description="The complete path of the route from the root, useful for matching group route.",
    )
    loader_path: str = Field(
        ...,
        description="Specifies the path to load the layout or page components, analogous to the 'loader' feature in react-router for fetching page data before rendering.",
    )
    index: bool = Field(
        default=False,
        description="Indicates whether the route serves as an index route, rendering at the parent's URL within an Outlet. analogous to the 'index' in react-router",
    )
    children: list["ClientRoute"] = Field(
        default=[],
        description="Nested routes under this route, enabling hierarchical routing structures.",
    )

    endpoint: Callable[[Any], Awaitable[PageResponse]] = Field(
        ...,
        exclude=True,
        description="The async function to handle client route requests, returning a page response.",
    )
    sitemap: Optional[Callable[[str], Awaitable[list[Sitemap]]]] = Field(
        default=None,
        exclude=True,
        description="An optional async function to generate sitemap entries for the route.",
    )

    @property
    def is_page(self) -> bool:
        """
        Returns True if the route is a page route (i.e., has no child routes), facilitating easier checks on routing structure.
        """
        return not self.children

    @property
    def is_dynamic(self) -> bool:
        """
        Evaluates if the route is dynamic, characterized by the presence of placeholders (e.g., '{userId}') in the path, enabling parameterized routing.
        """
        return "{" in self.path


ClientRoute.model_rebuild()


RouteInfo = namedtuple("RouteInfo", ["segment", "path", "absolute_path", "loader_path"])


def parse_route_info_from_folder(
    folder: pathlib.Path,
    is_root_folder: bool,
    parent_path: str,
    absolute_path: str = f"{ROOT_ROUTE_PREFIX}/",
) -> RouteInfo:
    """
    Parses the route information from the given folder.

    Parameters
    ----------
    folder : pathlib.Path
        The folder from which to parse the route information.
    is_root_folder : bool
        Whether the folder is the root folder.
    parent_path : str
        The parent path of the route.
    absolute_path : str
        The absolute path of the route.

    Returns
    -------
    RouteInfo
        The parsed route information.
    """
    if not is_root_folder and folder.stem.startswith(DYNAMIC_ROUTE_PREFIX):
        segment = "{" + folder.stem[len(DYNAMIC_ROUTE_PREFIX) :] + "}"
    elif not is_root_folder and not folder.stem.startswith(GROUP_ROUTE_PREFIX):
        segment = folder.stem
    else:
        segment = ""

    path = f"{parent_path.rstrip('/')}/{segment}/" if segment else parent_path

    loader_path = ROOT_ROUTE_PREFIX + (f"{path}{folder.stem}/" if folder.stem.startswith(GROUP_ROUTE_PREFIX) else path)

    absolute_path = f"{absolute_path}{folder.stem}/" if not is_root_folder else absolute_path
    return RouteInfo(segment=segment, path=path, absolute_path=absolute_path, loader_path=loader_path)


def parse_client_routes(
    folder: pathlib.Path,
    is_root_folder: bool = True,
    parent_path: str = "/",
    absolute_path: str = f"{ROOT_ROUTE_PREFIX}/",
) -> list[ClientRoute]:
    """
    Gets a list of ClientRoute objects from the given folder.

    Parameters
    ----------
    folder : pathlib.Path
        The folder from which to start building routes.
    is_root_folder : bool, optional
        Flag indicating if the folder is the root of the routing structure, by default True.
    parent_path : str
        The path of the parent route, by default "/".
    absolute_path : str
        The absolute path of the parent route, by default "/".

    Returns
    -------
    list[Route]
        A list of Route objects built from the folder structure.
    """
    routes = []
    route_info = parse_route_info_from_folder(folder, is_root_folder, parent_path, absolute_path)

    layout_file = folder / LAYOUT_ROUTE_FILENAME
    page_file = folder / PAGE_ROUTE_FILENAME

    for child_folder in folder.iterdir():
        if child_folder.is_dir() and child_folder.name not in EXCLUDED_FOLDER_NAMES:
            routes.extend(parse_client_routes(child_folder, False, route_info.path, route_info.absolute_path))

    if page_file.is_file():
        page_module = load_module(page_file)
        routes.append(
            ClientRoute(
                segment=route_info.segment,
                path=route_info.path,
                absolute_path=route_info.absolute_path,
                loader_path=route_info.loader_path,
                index=layout_file.is_file(),
                children=[],
                endpoint=page_module.page,
                sitemap=getattr(page_module, "sitemap", None),
            )
        )

    if layout_file.is_file():
        routes = [
            ClientRoute(
                segment=route_info.segment,
                loader_path=route_info.loader_path + LAYOUT_ROUTE_SUFFIX,
                path=route_info.path,
                absolute_path=route_info.absolute_path,
                index=False,
                children=routes,
                endpoint=load_module(layout_file).layout,
                sitemap=None,
            )
        ]

    return routes


def sort_client_routes(routes: list[ClientRoute]) -> list[ClientRoute]:
    for route in routes:
        if route.children:
            route.children = sort_client_routes(route.children)
    return sorted(routes, key=lambda r: path_priority(r.loader_path))


def get_client_routes(folder: pathlib.Path) -> list[ClientRoute]:
    return sort_client_routes(parse_client_routes(folder))
